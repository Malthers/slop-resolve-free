"""
Tema escuro e estilos inspirados no DaVinci Resolve oficial para a interface PyQt6.
"""

DARK_THEME_QSS = """
QMainWindow {
    background-color: #181818;
    color: #e0e0e0;
    font-family: 'Segoe UI', 'Inter', -apple-system, sans-serif;
}

QWidget {
    background-color: #181818;
    color: #e0e0e0;
    font-size: 13px;
    font-family: 'Segoe UI', 'Inter', -apple-system, sans-serif;
}

/* Header & Status */
#headerFrame {
    background-color: #202020;
    border-bottom: 1px solid #2d2d2d;
    padding: 10px 14px;
}

#statusLabel {
    font-size: 13px;
    font-weight: 600;
}

#subStatusLabel {
    font-size: 11px;
    color: #8c8c8c;
}

/* Action Buttons Bar */
#actionBar {
    background-color: #1e1e1e;
    border-bottom: 1px solid #282828;
    padding: 6px 12px;
}

QPushButton {
    background-color: #2c2c2c;
    color: #e0e0e0;
    border: 1px solid #3c3c3c;
    border-radius: 5px;
    padding: 6px 12px;
    font-weight: 500;
}

QPushButton:hover {
    background-color: #383838;
    border-color: #4a4a4a;
}

QPushButton:pressed {
    background-color: #222222;
}

QPushButton:disabled {
    background-color: #202020;
    color: #555555;
    border-color: #2a2a2a;
}

/* Accent Buttons */
#btnScanner {
    background-color: #252b33;
    border: 1px solid #35475e;
    color: #5ea8ff;
    font-weight: 600;
}

#btnScanner:hover {
    background-color: #2e3a47;
    border-color: #4c6a8f;
    color: #8ac0ff;
}

#btnSettings {
    background-color: #282828;
    border: 1px solid #3a3a3a;
}

/* Chat & Histórico */
QTextEdit#chatLog {
    background-color: #1a1a1a;
    border: 1px solid #282828;
    border-radius: 8px;
    padding: 12px;
    color: #dedede;
    selection-background-color: #f05a28;
    selection-color: #ffffff;
    line-height: 1.5;
}

/* Painel de Aprovação do Diretor */
#approvalPanel {
    background-color: #222622;
    border: 1px solid #2d4532;
    border-radius: 8px;
    padding: 10px 14px;
    margin-top: 4px;
    margin-bottom: 4px;
}

#approvalLabel {
    font-size: 13px;
    font-weight: 600;
    color: #c9f5d1;
}

#btnApprove {
    background-color: #236b3f;
    color: #ffffff;
    font-weight: bold;
    border: 1px solid #2a7b4c;
    border-radius: 5px;
    padding: 8px 16px;
}

#btnApprove:hover {
    background-color: #2a7b4c;
    border-color: #389e63;
}

#btnReject {
    background-color: #382424;
    color: #ff9d9d;
    border: 1px solid #542b2b;
    border-radius: 5px;
    padding: 8px 14px;
}

#btnReject:hover {
    background-color: #4a2d2d;
    color: #ffb8b8;
}

/* Input Area */
QLineEdit#promptInput {
    background-color: #222222;
    border: 1px solid #363636;
    border-radius: 6px;
    padding: 8px 12px;
    color: #ffffff;
    font-size: 13px;
}

QLineEdit#promptInput:focus {
    border: 1px solid #f05a28;
    background-color: #262626;
}

#btnSend {
    background-color: #f05a28;
    color: #ffffff;
    font-weight: bold;
    border: none;
    border-radius: 6px;
    padding: 8px 18px;
}

#btnSend:hover {
    background-color: #ff6a38;
}

#btnSend:pressed {
    background-color: #d84a1a;
}

/* Scrollbars */
QScrollBar:vertical {
    border: none;
    background: #181818;
    width: 8px;
    margin: 0px;
}

QScrollBar::handle:vertical {
    background: #333333;
    min-height: 25px;
    border-radius: 4px;
}

QScrollBar::handle:vertical:hover {
    background: #484848;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}
"""
