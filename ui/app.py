"""
Interface Gráfica Flutuante Always-on-Top do MasterEditor.
Projetada para DaVinci Resolve Free / Studio.
"""

import re
import sys
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QTextEdit, QFrame, QMessageBox, QApplication
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer

from ui.theme import DARK_THEME_QSS
from ui.settings_dialog import SettingsDialog
from core.resolve_client import ResolveBridgeClient
from core.llm_router import get_config, call_llm_stream, extract_code_blocks

class LLMWorkerThread(QThread):
    token_received = pyqtSignal(str)
    stream_finished = pyqtSignal(str)
    stream_error = pyqtSignal(str)

    def __init__(self, messages, config, timeline_state):
        super().__init__()
        self.messages = messages
        self.config = config
        self.timeline_state = timeline_state

    def run(self):
        full_text = ""
        try:
            for token in call_llm_stream(self.messages, self.config, self.timeline_state):
                full_text += token
                self.token_received.emit(token)
            self.stream_finished.emit(full_text)
        except Exception as e:
            self.stream_error.emit(str(e))

class ExecuteCodeThread(QThread):
    execution_done = pyqtSignal(dict)

    def __init__(self, client, code):
        super().__init__()
        self.client = client
        self.code = code

    def run(self):
        res = self.client.execute_code(self.code)
        self.execution_done.emit(res)

class MasterEditorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MasterEditor — Assistente de Direção DaVinci Resolve")
        self.resize(560, 780)
        self.setMinimumSize(480, 600)

        # Flag Always-on-Top para flutuar sobre a tela do DaVinci
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
        self.setStyleSheet(DARK_THEME_QSS)

        self.resolve_client = ResolveBridgeClient()
        self.conversation_history = []
        self.pending_execution_code = ""
        self.current_stream_raw = ""
        self.active_timeline_state = None

        self.init_ui()

        # Timer para checar conexao inicial e manter status atualizado
        self.status_timer = QTimer(self)
        self.status_timer.timeout.connect(self.check_resolve_connection)
        self.status_timer.start(5000)
        self.check_resolve_connection()

    def init_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(12, 12, 12, 12)
        main_layout.setSpacing(10)

        # 1. Header de Conexão
        header_frame = QFrame()
        header_frame.setObjectName("headerFrame")
        header_layout = QVBoxLayout(header_frame)
        header_layout.setContentsMargins(8, 8, 8, 8)
        header_layout.setSpacing(3)

        self.lbl_status = QLabel("🔴 DaVinci Desconectado")
        self.lbl_status.setObjectName("statusLabel")
        header_layout.addWidget(self.lbl_status)

        self.lbl_substatus = QLabel("Para conectar: Abra o DaVinci e execute Workspace > Scripts > MasterEditorBridge")
        self.lbl_substatus.setObjectName("subStatusLabel")
        header_layout.addWidget(self.lbl_substatus)

        main_layout.addWidget(header_frame)

        # 2. Barra de Ações Rápidas do Diretor
        action_bar = QHBoxLayout()
        action_bar.setSpacing(8)

        self.btn_scanner = QPushButton("🎯 Varrer Marcadores")
        self.btn_scanner.setObjectName("btnScanner")
        self.btn_scanner.clicked.connect(self.on_scan_markers_clicked)
        action_bar.addWidget(self.btn_scanner)

        self.btn_refresh = QPushButton("🔄 Atualizar")
        self.btn_refresh.clicked.connect(self.check_resolve_connection)
        action_bar.addWidget(self.btn_refresh)

        action_bar.addStretch()

        self.btn_settings = QPushButton("⚙️ Configurar IA")
        self.btn_settings.setObjectName("btnSettings")
        self.btn_settings.clicked.connect(self.open_settings)
        action_bar.addWidget(self.btn_settings)

        main_layout.addLayout(action_bar)

        # 3. Área de Chat / Histórico de Direção
        self.chat_log = QTextEdit()
        self.chat_log.setObjectName("chatLog")
        self.chat_log.setReadOnly(True)
        self.chat_log.setAcceptRichText(True)
        main_layout.addWidget(self.chat_log)

        # Mensagem de Boas-Vindas inicial
        self.append_system_msg(
            "<b>🎬 Bem-vindo ao MasterEditor (Modo 100% Free)!</b><br>"
            "Fale comigo como um Diretor. Você pode pedir títulos, animações, efeitos, "
            "ou usar o botão <b>🎯 Varrer Marcadores</b> para inspecionar os marcadores da timeline."
        )

        # 4. Painel de Aprovação do Diretor (visível apenas quando há código pendente)
        self.approval_panel = QFrame()
        self.approval_panel.setObjectName("approvalPanel")
        approval_layout = QVBoxLayout(self.approval_panel)
        approval_layout.setContentsMargins(10, 8, 10, 8)
        approval_layout.setSpacing(6)

        self.approval_label = QLabel("📋 <b>Plano Pronto:</b> Deseja aplicar as alterações no DaVinci?")
        self.approval_label.setObjectName("approvalLabel")
        approval_layout.addWidget(self.approval_label)

        btn_app_layout = QHBoxLayout()
        self.btn_approve = QPushButton("✅ Aprovar e Executar no DaVinci")
        self.btn_approve.setObjectName("btnApprove")
        self.btn_approve.clicked.connect(self.on_approve_clicked)
        btn_app_layout.addWidget(self.btn_approve)

        self.btn_reject = QPushButton("❌ Descartar")
        self.btn_reject.setObjectName("btnReject")
        self.btn_reject.clicked.connect(self.on_reject_clicked)
        btn_app_layout.addWidget(self.btn_reject)

        approval_layout.addLayout(btn_app_layout)
        self.approval_panel.setVisible(False)
        main_layout.addWidget(self.approval_panel)

        # 5. Barra Inferior de Entrada
        input_layout = QHBoxLayout()
        input_layout.setSpacing(8)

        self.prompt_input = QLineEdit()
        self.prompt_input.setObjectName("promptInput")
        self.prompt_input.setPlaceholderText("Diga como um Diretor... (ex: 'crie um título neon no clipe do marcador')")
        self.prompt_input.returnPressed.connect(self.on_send_prompt)
        input_layout.addWidget(self.prompt_input)

        self.btn_send = QPushButton("Enviar")
        self.btn_send.setObjectName("btnSend")
        self.btn_send.clicked.connect(self.on_send_prompt)
        input_layout.addWidget(self.btn_send)

        main_layout.addLayout(input_layout)

    def append_system_msg(self, html_text):
        self.chat_log.append(f"<div style='margin-bottom: 8px; color: #a0a0a0;'>{html_text}</div>")
        self.scroll_to_bottom()

    def append_user_msg(self, text):
        escaped = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\n", "<br>")
        self.chat_log.append(
            f"<div style='margin-top: 10px; margin-bottom: 6px;'>"
            f"<b style='color: #f05a28;'>Diretor:</b> {escaped}"
            f"</div>"
        )
        self.scroll_to_bottom()

    def scroll_to_bottom(self):
        cursor = self.chat_log.textCursor()
        cursor.movePosition(cursor.MoveOperation.End)
        self.chat_log.setTextCursor(cursor)

    def check_resolve_connection(self):
        info = self.resolve_client.ping()
        if info and info.get("connected"):
            version = info.get("resolve_version") or "Ativo"
            proj = info.get("project_name") or "Nenhum projeto aberto"
            tl = info.get("timeline_name") or "Nenhuma timeline"
            self.lbl_status.setText(f"🟢 DaVinci Resolve Conectado ({version})")
            self.lbl_status.setStyleSheet("color: #4cd964;")
            self.lbl_substatus.setText(f"Projeto: <b>{proj}</b> | Timeline: <b>{tl}</b>")
            self.active_timeline_state = self.resolve_client.get_state()
        else:
            self.lbl_status.setText("🔴 DaVinci Desconectado")
            self.lbl_status.setStyleSheet("color: #ff3b30;")
            self.lbl_substatus.setText("Execute no DaVinci: Workspace > Scripts > MasterEditorBridge")
            self.active_timeline_state = None

    def on_scan_markers_clicked(self):
        self.check_resolve_connection()
        if not self.active_timeline_state or not self.active_timeline_state.get("connected"):
            QMessageBox.warning(self, "Aviso", "O DaVinci Resolve não está conectado.\nInicie a ponte em Workspace > Scripts > MasterEditorBridge.")
            return

        markers = self.active_timeline_state.get("markers", [])
        if not markers:
            self.append_system_msg("ℹ️ <i>Nenhum marcador encontrado na timeline ativa.</i>")
            return

        summary = f"<b>🎯 Varredura da Timeline:</b> {len(markers)} marcador(es) identificado(s):<br>"
        for m in markers:
            rel_f = m.get("relative_frame")
            abs_f = m.get("absolute_frame")
            name = m.get("name") or "Sem Nome"
            note = m.get("note") or ""
            color = m.get("color")
            matched = m.get("matched_clip")
            clip_name = f"no clipe <b>'{matched['name']}'</b>" if matched else "<i>(sem clipe sob o ponto)</i>"
            summary += f"• [{color}] Frame {rel_f} (Abs: {abs_f}): <b>{name}</b> {clip_name}"
            if note:
                summary += f" — <i>'{note}'</i>"
            summary += "<br>"

        summary += "<br><i>O que você gostaria de aplicar nesses marcadores?</i>"
        self.append_system_msg(summary)

    def open_settings(self):
        dlg = SettingsDialog(self)
        dlg.exec()

    def on_send_prompt(self):
        text = self.prompt_input.text().strip()
        if not text:
            return

        self.prompt_input.clear()
        self.append_user_msg(text)

        # Ocultar painel de aprovação anterior
        self.approval_panel.setVisible(False)
        self.pending_execution_code = ""
        self.current_stream_raw = ""

        # Montar mensagens de conversa
        self.conversation_history.append({"role": "user", "content": text})

        self.btn_send.setEnabled(False)
        self.prompt_input.setEnabled(False)

        # Atualizar estado fresco da timeline antes do envio
        self.active_timeline_state = self.resolve_client.get_state()

        # Iniciar thread do streaming
        cfg = get_config()
        self.llm_thread = LLMWorkerThread(self.conversation_history, cfg, self.active_timeline_state)
        self.llm_thread.token_received.connect(self.on_token_received)
        self.llm_thread.stream_finished.connect(self.on_stream_finished)
        self.llm_thread.stream_error.connect(self.on_stream_error)
        self.llm_thread.start()

    def on_token_received(self, token):
        self.current_stream_raw += token
        # Clean UX: Não renderiza enquanto estiver dentro de blocos ``` de código
        if "```" not in self.current_stream_raw:
            cursor = self.chat_log.textCursor()
            cursor.movePosition(cursor.MoveOperation.End)
            cursor.insertText(token)
            self.chat_log.setTextCursor(cursor)

    def on_stream_finished(self, full_response):
        self.btn_send.setEnabled(True)
        self.prompt_input.setEnabled(True)
        self.prompt_input.setFocus()

        self.conversation_history.append({"role": "assistant", "content": full_response})

        # Extrair código Python gerado
        code = extract_code_blocks(full_response)
        
        # Limpar texto visual se o streaming foi parcialmente suprimido por blocos de código
        # Separar a parte explicativa visual do bloco técnico
        text_parts = re.split(r"```(?:python)?.*?```", full_response, flags=re.DOTALL)
        clean_explanation = "\n".join([p.strip() for p in text_parts if p.strip()])

        # Se o streaming teve blocos de código suprimidos, renderiza a explicação limpa
        if "```" in full_response:
            # Atualiza o log com a explicacao visual limpa
            escaped_explanation = clean_explanation.replace("\n", "<br>")
            self.chat_log.append(f"<div style='margin-bottom: 8px;'>{escaped_explanation}</div>")

        if code:
            self.pending_execution_code = code
            self.append_system_msg(
                "<span style='color: #4a90e2; font-size: 11px;'>"
                "⚙️ <i>[Plano técnico formulado em segundo plano e pronto para execução]</i>"
                "</span>"
            )
            self.approval_label.setText("📋 <b>Plano de Ação Pronto:</b> Deseja executar as alterações no DaVinci Resolve?")
            self.approval_panel.setVisible(True)
        
        self.scroll_to_bottom()

    def on_stream_error(self, err_msg):
        self.btn_send.setEnabled(True)
        self.prompt_input.setEnabled(True)
        self.append_system_msg(f"❌ <b>Erro na IA:</b> {err_msg}")
        self.scroll_to_bottom()

    def on_approve_clicked(self):
        if not self.pending_execution_code:
            return

        self.btn_approve.setEnabled(False)
        self.btn_approve.setText("⏳ Executando...")

        self.exec_thread = ExecuteCodeThread(self.resolve_client, self.pending_execution_code)
        self.exec_thread.execution_done.connect(self.on_execution_finished)
        self.exec_thread.start()

    def on_execution_finished(self, result):
        self.btn_approve.setEnabled(True)
        self.btn_approve.setText("✅ Aprovar e Executar no DaVinci")
        self.approval_panel.setVisible(False)

        if result.get("success"):
            out = result.get("stdout", "").strip()
            msg = "✅ <b>Executado com sucesso no DaVinci Resolve!</b>"
            if out:
                msg += f"<br><pre style='color: #8ac0ff; font-size: 11px;'>{out}</pre>"
            self.append_system_msg(msg)
        else:
            err = result.get("stderr", "").strip()
            self.append_system_msg(f"❌ <b>Falha na execução:</b><br><pre style='color: #ff8080; font-size: 11px;'>{err}</pre>")

        self.pending_execution_code = ""
        self.scroll_to_bottom()

    def on_reject_clicked(self):
        self.approval_panel.setVisible(False)
        self.pending_execution_code = ""
        self.append_system_msg("❌ <i>Plano descartado pelo Diretor. Diga quais ajustes deseja fazer.</i>")
        self.prompt_input.setFocus()

def run_app():
    app = QApplication(sys.argv)
    window = MasterEditorApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    run_app()
