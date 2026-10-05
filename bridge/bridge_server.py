#!/usr/bin/env python3
"""
MasterEditorBridge - Servidor de Ponte HTTP para DaVinci Resolve Free / Studio.
Este script deve ser executado de dentro do DaVinci Resolve:
Menu: Workspace > Scripts > MasterEditorBridge (ou Utility)

Ele roda um servidor HTTP leve em 127.0.0.1:8955 para receber instruções do MasterEditor.
"""

import sys
import io
import json
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

BRIDGE_PORT = 8955
BRIDGE_VERSION = "2.0.0"

def get_resolve_objects():
    """Obtém os objetos nativos do DaVinci Resolve no ambiente interno."""
    global resolve, fusion
    res = globals().get("resolve")
    fus = globals().get("fusion")
    
    if not res:
        try:
            import fusionscript as bmd
            res = bmd.scriptapp("Resolve")
        except Exception:
            try:
                import DaVinciResolveScript as bmd
                res = bmd.scriptapp("Resolve")
            except Exception:
                res = None

    if not fus and res:
        fus = res.Fusion()
        
    pm = res.GetProjectManager() if res else None
    proj = pm.GetCurrentProject() if pm else None
    tl = proj.GetCurrentTimeline() if proj else None
    mp = proj.GetMediaPool() if proj else None
    ms = res.GetMediaStorage() if res else None

    return {
        "resolve": res,
        "fusion": fus,
        "project_manager": pm,
        "project": proj,
        "timeline": tl,
        "media_pool": mp,
        "media_storage": ms
    }

def gather_full_state():
    """Coleta o estado completo da timeline ativa, resolvendo marcadores matematicamente."""
    objs = get_resolve_objects()
    res = objs["resolve"]
    proj = objs["project"]
    tl = objs["timeline"]

    state = {
        "connected": bool(res),
        "resolve_version": res.GetVersionString() if res else "Unknown",
        "project_name": proj.GetName() if proj else None,
        "timeline_name": tl.GetName() if tl else None,
        "timeline_start_frame": 0,
        "timeline_start_timecode": "01:00:00:00",
        "frame_rate": 24.0,
        "video_tracks": 0,
        "audio_tracks": 0,
        "clips": [],
        "markers": []
    }

    if not tl:
        return state

    try:
        state["timeline_start_frame"] = tl.GetStartFrame() or 0
        state["timeline_start_timecode"] = tl.GetStartTimecode() or "01:00:00:00"
        state["video_tracks"] = tl.GetTrackCount("video")
        state["audio_tracks"] = tl.GetTrackCount("audio")
    except Exception as e:
        state["error_metadata"] = str(e)

    # Coletar clipes de vídeo
    video_clips = []
    try:
        for track_idx in range(1, state["video_tracks"] + 1):
            items = tl.GetItemListInTrack("video", track_idx) or []
            for it in items:
                start_f = it.GetStart()
                end_f = it.GetEnd()
                name = it.GetName()
                dur = it.GetDuration()
                video_clips.append({
                    "name": name,
                    "track": track_idx,
                    "start": start_f,
                    "end": end_f,
                    "duration": dur
                })
        state["clips"] = video_clips
    except Exception as e:
        state["error_clips"] = str(e)

    # Coletar e resolver marcadores dinamicamente
    try:
        raw_markers = tl.GetMarkers() or {}
        resolved_markers = []
        tl_start = state["timeline_start_frame"]

        for frame_rel_str, marker in raw_markers.items():
            rel_frame = int(frame_rel_str)
            abs_frame = tl_start + rel_frame

            matched_clip = None
            for clip in video_clips:
                if clip["start"] <= abs_frame < clip["end"]:
                    matched_clip = {
                        "name": clip["name"],
                        "track": clip["track"],
                        "offset_in_clip": abs_frame - clip["start"]
                    }
                    break

            resolved_markers.append({
                "relative_frame": rel_frame,
                "absolute_frame": abs_frame,
                "name": marker.get("name", ""),
                "note": marker.get("note", ""),
                "color": marker.get("color", "Blue"),
                "duration": marker.get("duration", 1),
                "matched_clip": matched_clip
            })

        # Ordenar marcadores cronologicamente
        resolved_markers.sort(key=lambda m: m["relative_frame"])
        state["markers"] = resolved_markers
    except Exception as e:
        state["error_markers"] = str(e)

    return state

class BridgeRequestHandler(BaseHTTPRequestHandler):
    def _send_json(self, status_code, data):
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        if self.path == "/ping":
            objs = get_resolve_objects()
            res = objs["resolve"]
            proj = objs["project"]
            tl = objs["timeline"]
            self._send_json(200, {
                "status": "online",
                "bridge_version": BRIDGE_VERSION,
                "connected": bool(res),
                "resolve_version": res.GetVersionString() if res else None,
                "project_name": proj.GetName() if proj else None,
                "timeline_name": tl.GetName() if tl else None
            })
        elif self.path == "/state":
            state = gather_full_state()
            self._send_json(200, state)
        else:
            self._send_json(404, {"error": "Not Found"})

    def do_POST(self):
        if self.path == "/execute":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            try:
                req_data = json.loads(body)
                code = req_data.get("code", "")
            except Exception as e:
                self._send_json(400, {"error": f"JSON inválido: {e}"})
                return

            objs = get_resolve_objects()
            scope = {
                "resolve": objs["resolve"],
                "fusion": objs["fusion"],
                "project_manager": objs["project_manager"],
                "project": objs["project"],
                "timeline": objs["timeline"],
                "media_pool": objs["media_pool"],
                "media_storage": objs["media_storage"]
            }

            stdout_capture = io.StringIO()
            stderr_capture = io.StringIO()
            old_stdout = sys.stdout
            old_stderr = sys.stderr
            success = False

            try:
                sys.stdout = stdout_capture
                sys.stderr = stderr_capture
                exec(code, scope)
                success = True
            except Exception as e:
                import traceback
                traceback.print_exc(file=stderr_capture)
                success = False
            finally:
                sys.stdout = old_stdout
                sys.stderr = old_stderr

            self._send_json(200, {
                "success": success,
                "stdout": stdout_capture.getvalue(),
                "stderr": stderr_capture.getvalue()
            })
        else:
            self._send_json(404, {"error": "Not Found"})

    def log_message(self, format, *args):
        # Silencia logs HTTP comuns no terminal
        pass

def start_server():
    server = HTTPServer(("127.0.0.1", BRIDGE_PORT), BridgeRequestHandler)
    print(f"\n=======================================================")
    print(f" 🟢 MasterEditorBridge ATIVO na porta {BRIDGE_PORT}")
    print(f" Versão: {BRIDGE_VERSION} (100% Compatível com DaVinci Free)")
    print(f" Aguardando comandos da interface gráfica...")
    print(f"=======================================================\n")
    server.serve_forever()

if __name__ == "__main__":
    start_server()
