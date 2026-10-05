"""
Diálogo de Configuração de IA e Provedores do MasterEditor.
Permite selecionar provedor, chave de API e buscar modelos online filtrados.
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QComboBox, QPushButton, QMessageBox, QFrame
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from core.llm_router import get_config, save_config
from core.model_fetcher import fetch_available_models

class ModelFetcherThread(QThread):
    models_ready = pyqtSignal(list)
    fetch_failed = pyqtSignal(str)

    def __init__(self, provider, api_key, api_base):
        super().__init__()
        self.provider = provider
        self.api_key = api_key
        self.api_base = api_base

    def run(self):
        try:
            models = fetch_available_models(self.provider, self.api_key, self.api_base)
            self.models_ready.emit(models)
        except Exception as e:
            self.fetch_failed.emit(str(e))

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Configurações do MasterEditor IA")
        self.setFixedSize(480, 380)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint)
        self.setStyleSheet("""
            QDialog { background-color: #202020; color: #e0e0e0; font-family: 'Segoe UI', sans-serif; }
            QLabel { color: #cccccc; font-size: 12px; }
            QLineEdit, QComboBox { background-color: #2b2b2b; color: #ffffff; border: 1px solid #3d3d3d; border-radius: 5px; padding: 6px; }
            QLineEdit:focus, QComboBox:focus { border: 1px solid #f05a28; }
            QPushButton { background-color: #333333; color: #ffffff; border: 1px solid #444444; border-radius: 5px; padding: 7px 14px; font-weight: 500; }
            QPushButton:hover { background-color: #404040; }
            #btnSave { background-color: #f05a28; border: none; font-weight: bold; }
            #btnSave:hover { background-color: #ff6a38; }
            #btnFetch { background-color: #252b33; border: 1px solid #35475e; color: #5ea8ff; }
            #btnFetch:hover { background-color: #2e3a47; color: #8ac0ff; }
        """)

        self.cfg = get_config()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(20, 20, 20, 20)

        # Provedor
        layout.addWidget(QLabel("Provedor de IA:"))
        self.provider_combo = QComboBox()
        self.provider_combo.addItems([
            "Google Gemini",
            "OpenAI (ChatGPT)",
            "OpenRouter",
            "Ollama",
            "LM Studio"
        ])
        current_prov = self.cfg.get("provider", "Google Gemini")
        idx = self.provider_combo.findText(current_prov)
        if idx >= 0:
            self.provider_combo.setCurrentIndex(idx)
        self.provider_combo.currentTextChanged.connect(self.on_provider_changed)
        layout.addWidget(self.provider_combo)

        # API Key
        self.lbl_api_key = QLabel("Chave de API (API Key):")
        layout.addWidget(self.lbl_api_key)
        self.key_input = QLineEdit()
        self.key_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.key_input.setText(self.cfg.get("api_key", ""))
        self.key_input.setPlaceholderText("Cole sua chave de API aqui...")
        layout.addWidget(self.key_input)

        # Base URL (opcional para Ollama / proxies)
        self.lbl_api_base = QLabel("URL Base / Endpoint (Opcional):")
        layout.addWidget(self.lbl_api_base)
        self.base_input = QLineEdit()
        self.base_input.setText(self.cfg.get("api_base", ""))
        self.base_input.setPlaceholderText("Ex: http://localhost:11434")
        layout.addWidget(self.base_input)

        # Linha de busca de modelos
        model_header = QHBoxLayout()
        model_header.addWidget(QLabel("Modelo de IA:"))
        model_header.addStretch()
        self.btn_fetch = QPushButton("🔍 Buscar Modelos Online")
        self.btn_fetch.setObjectName("btnFetch")
        self.btn_fetch.clicked.connect(self.fetch_models_online)
        model_header.addWidget(self.btn_fetch)
        layout.addLayout(model_header)

        # Combo de modelos
        self.model_combo = QComboBox()
        self.model_combo.setEditable(True)
        current_model = self.cfg.get("model", "gemini/gemini-3.8-flash")
        self.model_combo.addItem(current_model)
        self.model_combo.setCurrentText(current_model)
        layout.addWidget(self.model_combo)

        layout.addStretch()

        # Botões de Ação
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        self.btn_cancel = QPushButton("Cancelar")
        self.btn_cancel.clicked.connect(self.reject)
        btn_layout.addWidget(self.btn_cancel)

        self.btn_save = QPushButton("Salvar Configurações")
        self.btn_save.setObjectName("btnSave")
        self.btn_save.clicked.connect(self.save_and_close)
        btn_layout.addWidget(self.btn_save)

        layout.addLayout(btn_layout)

    def on_provider_changed(self, provider_text):
        if provider_text in ["Ollama", "LM Studio"]:
            self.key_input.setPlaceholderText("Geralmente não é necessária para servidores locais")
        else:
            self.key_input.setPlaceholderText("Cole sua chave de API aqui...")

    def fetch_models_online(self):
        provider = self.provider_combo.currentText()
        key = self.key_input.text().strip()
        base = self.base_input.text().strip()

        self.btn_fetch.setEnabled(False)
        self.btn_fetch.setText("⏳ Buscando...")

        self.thread = ModelFetcherThread(provider, key, base)
        self.thread.models_ready.connect(self.on_models_received)
        self.thread.fetch_failed.connect(self.on_fetch_failed)
        self.thread.start()

    def on_models_received(self, models):
        self.btn_fetch.setEnabled(True)
        self.btn_fetch.setText("🔍 Buscar Modelos Online")
        
        if not models:
            QMessageBox.information(self, "Modelos", "Nenhum modelo compatível foi retornado pelo provedor.")
            return

        current_text = self.model_combo.currentText()
        self.model_combo.clear()
        self.model_combo.addItems(models)
        
        if current_text in models:
            self.model_combo.setCurrentText(current_text)
        else:
            self.model_combo.setCurrentIndex(0)

        QMessageBox.information(self, "Sucesso", f"{len(models)} modelo(s) filtrado(s) com sucesso!")

    def on_fetch_failed(self, err_msg):
        self.btn_fetch.setEnabled(True)
        self.btn_fetch.setText("🔍 Buscar Modelos Online")
        QMessageBox.warning(self, "Aviso", f"Não foi possível buscar modelos online:\n{err_msg}")

    def save_and_close(self):
        self.cfg["provider"] = self.provider_combo.currentText()
        self.cfg["api_key"] = self.key_input.text().strip()
        self.cfg["api_base"] = self.base_input.text().strip()
        self.cfg["model"] = self.model_combo.currentText().strip()
        save_config(self.cfg)
        self.accept()
