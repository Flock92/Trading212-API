import asyncio

import aiohttp
from PyQt6.QtCore import QSettings, Qt
from PyQt6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)


class SettingsView(QWidget):
    def __init__(self, client):
        super().__init__()

        self.client = client
        self.settings = QSettings("TradeDesk", "TradingApp")

        self.setObjectName("SettingsView")  # Linked to QWidget#SettingsView
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self.main_layout = QVBoxLayout(self)

        # --- Header ---
        header = QLabel("System Settings")
        header.setObjectName("SettingsHeader")  # Linked to QLabel#SettingsHeader
        self.main_layout.addWidget(header)

        # --- Scroll Area ---
        self.scroll = QScrollArea()
        self.scroll.setObjectName(
            "SettingsScrollArea"
        )  # Linked to QScrollArea#SettingsScrollArea
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.Shape.NoFrame)

        self.content = QWidget()
        self.content.setObjectName(
            "SettingsContents"
        )  # Linked to QWidget#SettingsContents
        self.layout = QVBoxLayout(self.content)
        self.layout.setContentsMargins(30, 20, 30, 30)
        self.layout.setSpacing(25)

        # --- Appearance ---
        self.section("Appearance")
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Dark", "Light", "System"])
        saved_theme = self.settings.value("theme", "Dark")
        self.theme_combo.setCurrentText(saved_theme)
        self.theme_combo.currentTextChanged.connect(self.apply_theme)
        self.layout.addWidget(self.theme_combo)

        # --- Trading Preferences ---
        self.section("Trading Preferences")
        trade_frame = QFrame()
        trade_frame.setObjectName(
            "SettingsGroupFrame"
        )  # Linked to QFrame#SettingsGroupFrame
        trade_layout = QVBoxLayout(trade_frame)

        self.default_size = self.spin_row(
            trade_layout,
            "Default Order Size",
            1,
            100000,
            int(self.settings.value("default_size", 1)),
        )

        self.confirm_orders = QCheckBox("Confirm before placing order")
        self.confirm_orders.setChecked(
            self.settings.value("confirm_orders", True, type=bool)
        )

        self.price_alerts = QCheckBox("Enable price alerts")
        self.price_alerts.setChecked(
            self.settings.value("price_alerts", True, type=bool)
        )

        trade_layout.addWidget(self.confirm_orders)
        trade_layout.addWidget(self.price_alerts)
        self.layout.addWidget(trade_frame)

        # --- API Refresh ---
        self.section("API Refresh Intervals (Seconds)")
        api_frame = QFrame()
        api_frame.setObjectName("SettingsGroupFrame")
        api_layout = QVBoxLayout(api_frame)

        self.portfolio_interval = self.spin_row(
            api_layout,
            "Portfolio Refresh",
            1,
            300,
            int(self.settings.value("portfolio_interval", 30)),
        )
        self.price_interval = self.spin_row(
            api_layout,
            "Price Updates",
            1,
            60,
            int(self.settings.value("price_interval", 5)),
        )
        self.layout.addWidget(api_frame)

        # --- Discord Alerts ---
        self.section("Discord Alerts")
        notif_frame = QFrame()
        notif_frame.setObjectName("SettingsGroupFrame")  # Added link to stylesheet
        notif_layout = QVBoxLayout(notif_frame)

        self.enable_discord = QCheckBox("Enable Discord Alerts")
        self.enable_discord.setChecked(
            self.settings.value("discord_enabled", False, type=bool)
        )

        self.discord_webhook = QLineEdit()
        self.discord_webhook.setObjectName(
            "DiscordInput"
        )  # Linked to QLineEdit#DiscordInput
        self.discord_webhook.setPlaceholderText("Discord Webhook URL")
        self.discord_webhook.setText(self.settings.value("discord_webhook", ""))

        self.alert_trades = QCheckBox("Send Trade Executions")
        self.alert_trades.setChecked(
            self.settings.value("discord_trade_alerts", True, type=bool)
        )

        self.alert_errors = QCheckBox("Send System Errors")
        self.alert_errors.setChecked(
            self.settings.value("discord_error_alerts", True, type=bool)
        )

        self.test_discord = QPushButton("Test Discord Notification")
        self.test_discord.setObjectName(
            "SecondaryBtn"
        )  # Added link to QPushButton#SecondaryBtn
        self.test_discord.clicked.connect(self.send_test_discord)

        notif_layout.addWidget(self.enable_discord)
        notif_layout.addWidget(QLabel("Discord Webhook URL"))
        notif_layout.addWidget(self.discord_webhook)
        notif_layout.addWidget(self.alert_trades)
        notif_layout.addWidget(self.alert_errors)
        notif_layout.addWidget(self.test_discord)
        self.layout.addWidget(notif_frame)

        # --- Connection Info ---
        self.section("Connection")
        conn_frame = QFrame()
        conn_frame.setObjectName("SettingsGroupFrame")
        conn_layout = QVBoxLayout(conn_frame)

        status = "Connected" if self.client else "Disconnected"
        self.status_label = QLabel(f"● {status}")
        self.status_label.setObjectName("ConnectionStatusLabel")
        self.status_label.setProperty("status", "online" if self.client else "offline")
        conn_layout.addWidget(self.status_label)
        self.layout.addWidget(conn_frame)

        # --- Session Controls ---
        self.section("Session")
        self.logout_btn = QPushButton("Logout")
        self.logout_btn.setObjectName("LogoutBtn")  # Linked to QPushButton#LogoutBtn
        self.logout_btn.clicked.connect(self.handle_logout)
        self.layout.addWidget(self.logout_btn)

        # --- Save ---
        self.save_btn = QPushButton("Save Settings")
        self.save_btn.setObjectName(
            "SaveSettingsBtn"
        )  # Linked to QPushButton#SaveSettingsBtn
        self.save_btn.clicked.connect(self.save_settings)
        self.layout.addWidget(self.save_btn)

        self.layout.addStretch()
        self.scroll.setWidget(self.content)
        self.main_layout.addWidget(self.scroll)

    def section(self, text):
        """Helper to create section headers linked to CSS."""
        label = QLabel(text)
        label.setObjectName("SettingsSectionLabel")
        self.layout.addWidget(label)

    def spin_row(self, parent_layout, label_text, min_val, max_val, value):
        row = QHBoxLayout()
        label = QLabel(label_text)
        spin = QSpinBox()
        spin.setObjectName("IntervalSpinBox")  # Linked to QSpinBox#IntervalSpinBox
        spin.setRange(min_val, max_val)
        spin.setValue(value)
        row.addWidget(label)
        row.addStretch()
        row.addWidget(spin)
        parent_layout.addLayout(row)
        return spin

    def apply_theme(self):
        # We assume the window has a reference to your global stylesheet loader
        theme = self.theme_combo.currentText()
        self.settings.setValue("theme", theme)

        # This triggers the parent window to reload the CSS across the whole app
        if self.window():
            from src.gui.styles import get_stylesheet

            self.window().setStyleSheet(get_stylesheet(theme))
            # Optional: ensure child widgets update immediately
            self.style().unpolish(self)
            self.style().polish(self)

    def save_settings(self):
        self.settings.setValue("theme", self.theme_combo.currentText())
        self.settings.setValue("default_size", self.default_size.value())
        self.settings.setValue("confirm_orders", self.confirm_orders.isChecked())
        self.settings.setValue("portfolio_interval", self.portfolio_interval.value())
        self.settings.setValue("price_interval", self.price_interval.value())
        self.settings.setValue("discord_enabled", self.enable_discord.isChecked())
        self.settings.setValue("discord_webhook", self.discord_webhook.text())
        self.settings.setValue("discord_trade_alerts", self.alert_trades.isChecked())
        self.settings.setValue("discord_error_alerts", self.alert_errors.isChecked())
        self.settings.sync()
        print("Settings saved")

    def handle_logout(self):
        """Clears session and tells the main window to lock the app."""
        print("Logging out...")

        # 1. Update local settings
        self.settings.setValue("session_active", False)
        self.settings.sync()

        # 2. Trigger the shutdown and UI reset
        async def perform_logout():
            try:
                # Close API connection if it exists
                if self.client:
                    await self.client.close()
            except Exception as e:
                print(f"Logout Error during client close: {e}")

            # 3. Tell the main window to hide sidebar and show login
            if self.window() and hasattr(self.window(), "lock_app"):
                self.window().lock_app()

        asyncio.create_task(perform_logout())

    def send_test_discord(self):
        webhook = self.discord_webhook.text().strip()
        if webhook:
            asyncio.create_task(self._send_test(webhook))

    async def _send_test(self, webhook):
        payload = {"content": "✅ Trading Terminal Test Message."}
        try:
            async with aiohttp.ClientSession() as session:
                await session.post(webhook, json=payload)
        except Exception as e:
            print("Discord error:", e)
