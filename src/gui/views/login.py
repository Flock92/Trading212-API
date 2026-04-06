import asyncio
import json
import os
import sys
import keyring
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QFrame,
    QLabel,
    QLineEdit,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
from qasync import asyncSlot

# New Event Architecture Imports
from src.apitConnect.event import event_bus, EventType, Event, Listener
from src.apitConnect.core.network.api import Api
from src.apitConnect.core.network.supervisor import ApiSupervisor

SERVICE_NAME = "Apit212_Trading_Bot"

class LoadingView(QFrame):
    def __init__(self):
        super().__init__()
        self.setFixedWidth(400)
        self.setStyleSheet("""
            QFrame {
                background-color: #1A1A1A;
                border: 1px solid #333333;
                border-radius: 12px;
                padding: 30px;
            }
        """)

        layout = QVBoxLayout(self)
        self.status_label = QLabel("Initializing...")
        self.status_label.setStyleSheet("color: #0078d7; font-size: 16px; font-weight: bold; border: none;")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.detail_label = QLabel("Please wait...")
        self.detail_label.setStyleSheet("color: #AAAAAA; font-size: 12px; border: none;")
        self.detail_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.progress = QProgressBar()
        self.progress.setRange(0, 0) # Set to indeterminate (pulsing) by default
        self.progress.setFixedHeight(8)
        self.progress.setStyleSheet("""
            QProgressBar { background-color: #2A2A2A; border-radius: 4px; border: none; }
            QProgressBar::chunk { background-color: #0078d7; border-radius: 4px; }
        """)

        layout.addWidget(self.status_label)
        layout.addSpacing(5)
        layout.addWidget(self.detail_label)
        layout.addSpacing(20)
        layout.addWidget(self.progress)

    def update_status(self, message: str):
        self.status_label.setText("Authenticating...")
        self.detail_label.setText(message)


class LoginView(QWidget):
    def __init__(self, client, on_login_success):
        super().__init__()
        self.client = client
        self.on_login_success = on_login_success
        self.config_file = "user_settings.json"
        
        self._progress_task = None
        self.init_ui()
        self.load_remembered_user()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.card = QFrame()
        self.card.setFixedWidth(350)
        self.card.setObjectName("LoginCard")
        self.card.setStyleSheet("""
            QFrame#LoginCard {
                background-color: #1A1A1A;
                border: 1px solid #333333;
                border-radius: 12px;
                padding: 20px;
            }
            QLabel { color: #AAAAAA; font-size: 12px; }
            QLineEdit, QComboBox {
                background-color: #2A2A2A; border: 1px solid #444;
                color: white; padding: 8px; border-radius: 4px; margin-bottom: 10px;
            }
        """)

        card_layout = QVBoxLayout(self.card)
        header = QLabel("Login to Apit212")
        header.setStyleSheet("font-size: 20px; font-weight: bold; color: white; margin-bottom: 10px;")
        card_layout.addWidget(header)

        card_layout.addWidget(QLabel("Email Address"))
        self.email_input = QLineEdit()
        card_layout.addWidget(self.email_input)

        card_layout.addWidget(QLabel("Password"))
        self.pass_input = QLineEdit()
        self.pass_input.setEchoMode(QLineEdit.EchoMode.Password)
        card_layout.addWidget(self.pass_input)

        self.remember_check = QCheckBox("Remember Me (Encrypted)")
        card_layout.addWidget(self.remember_check)

        self.login_btn = QPushButton("Connect Session")
        self.login_btn.setFixedHeight(40)
        self.login_btn.clicked.connect(self.handle_login)
        card_layout.addWidget(self.login_btn)

        layout.addWidget(self.card)

        self.loading_overlay = LoadingView()
        layout.addWidget(self.loading_overlay)
        self.loading_overlay.hide()

    

    @asyncSlot()
    async def handle_login(self):
        email = self.email_input.text()
        password = self.pass_input.text()

        if not email or not password:
            QMessageBox.warning(self, "Error", "Credentials required.")
            return

        if self.remember_check.isChecked():
            with open(self.config_file, "w") as f:
                json.dump({"last_email": email}, f)
            keyring.set_password(SERVICE_NAME, email, password)

        await self.perform_authentication(email, password)

    async def perform_authentication(self, email, password):
        self.card.hide()
        self.loading_overlay.show()

        # Create a listener for SYSTEM events to update the UI message
        progress_listener = Listener(
            event_type=EventType.SYSTEM,
            handler=self.on_progress_event
        )
        self._progress_task = asyncio.create_task(progress_listener.start(event_bus))

        try:
            # Use the new authenticate method from your PlaywrightConnect
            # and ensure credentials are set first
            self.client.with_credentials(email, password)
            _client_obj = await self.client.authenticate(email, password)

            if _client_obj:
                if self._progress_task: self._progress_task.cancel()
                self.on_login_success(_client_obj)

        except Exception as e:
            if self._progress_task: self._progress_task.cancel()
            self.show_error(f"Auth Failed: {str(e)}")

        

    async def on_progress_event(self, event: Event):
        """Updates the loading UI based on System Events."""
        print(event)
        # Since we are on the QEventLoop, we can update UI directly
        # Use QTimer.singleShot for thread-safe insurance if needed
        self.loading_overlay.update_status(event.message)

    def show_error(self, message):
        self.loading_overlay.hide()
        self.card.show()
        QMessageBox.critical(self, "Login Error", message)

    def load_remembered_user(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r") as f:
                    settings = json.load(f)
                    email = settings.get("last_email")
                    self.email_input.setText(email)
                    self.remember_check.setChecked(True)
                    saved_pw = keyring.get_password(SERVICE_NAME, email)
                    if saved_pw: self.pass_input.setText(saved_pw)
            except: pass

    def reset_ui(self):
        self.loading_overlay.hide()
        self.card.show()
