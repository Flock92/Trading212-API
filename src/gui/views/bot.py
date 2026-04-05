import asyncio
import hashlib
import json
from datetime import datetime

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QDoubleSpinBox,
    QFormLayout,
    QFrame,
    QGroupBox,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QPushButton,
    QSpinBox,
    QTableWidget,
    QTableWidgetItem,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)
from qasync import asyncSlot


class ConfigDialog(QDialog):
    """Deep configuration dialog for trading parameters."""

    def __init__(self, parent=None, ticker=""):
        super().__init__(parent, Qt.WindowType.Dialog)
        self.setWindowTitle(f"Configure Bot: {ticker}")
        self.setMinimumWidth(500)

        layout = QVBoxLayout(self)
        tabs = QTabWidget()

        # --- Tab 1: Connection & Entry ---
        entry_tab = QWidget()
        entry_layout = QFormLayout(entry_tab)

        self.price_api = QComboBox()
        self.price_api.addItems(
            ["Binance WS", "Coinbase Pro", "Kraken REST", "AlphaVantage"]
        )

        self.interval = QComboBox()
        self.interval.addItems(["1m", "5m", "15m", "1h", "4h", "1d"])

        self.target_price = QDoubleSpinBox()
        self.target_price.setRange(0, 1000000)

        self.spread_tol = QDoubleSpinBox()
        self.spread_tol.setSuffix("%")
        self.spread_tol.setValue(0.05)

        self.slippage = QDoubleSpinBox()
        self.slippage.setSuffix("%")
        self.slippage.setValue(0.1)

        self.order_type = QComboBox()
        self.order_type.addItems(["Market", "Limit", "Post-Only"])

        self.direction = QComboBox()
        self.direction.addItems(["Long", "Short"])

        self.auto_price_btn = QPushButton("Auto-Fill Current Price")
        self.auto_price_btn.clicked.connect(self.fill_current_price)

        self.auto_spread = QCheckBox("Auto-Calculate Spread from Order Book")

        entry_layout.addRow(self.auto_spread)
        entry_layout.addRow(self.auto_price_btn)
        entry_layout.addRow("Trade Direction:", self.direction)
        entry_layout.addRow("Max Slippage:", self.slippage)
        entry_layout.addRow("Order Type:", self.order_type)
        entry_layout.addRow("Price API Source:", self.price_api)
        entry_layout.addRow("Chart Interval:", self.interval)
        entry_layout.addRow("Target Entry Price:", self.target_price)
        entry_layout.addRow("Max Spread Tolerance:", self.spread_tol)
        tabs.addTab(entry_tab, "Connection/Entry")

        # --- Tab 2: Technical Indicators ---
        tech_tab = QWidget()
        tech_layout = QFormLayout(tech_tab)

        self.use_rsi = QCheckBox("Enable RSI Filter")
        self.rsi_period = QSpinBox()
        self.rsi_period.setValue(14)

        self.use_ema = QCheckBox("Enable EMA Trend Follow")
        self.ema_fast = QSpinBox()
        self.ema_fast.setValue(12)
        self.ema_slow = QSpinBox()
        self.ema_slow.setValue(26)
        self.use_macd = QCheckBox("Enable MACD")
        self.macd_fast = QSpinBox()
        self.macd_fast.setValue(12)
        self.macd_slow = QSpinBox()
        self.macd_slow.setValue(26)
        self.macd_signal = QSpinBox()
        self.macd_signal.setValue(9)

        tech_layout.addRow(self.use_rsi)
        tech_layout.addRow("RSI Period:", self.rsi_period)
        tech_layout.addRow(self.use_ema)
        tech_layout.addRow("Fast EMA:", self.ema_fast)
        tech_layout.addRow("Slow EMA:", self.ema_slow)
        tech_layout.addRow(self.use_macd)
        tech_layout.addRow("MACD Fast:", self.macd_fast)
        tech_layout.addRow("MACD Slow:", self.macd_slow)
        tech_layout.addRow("MACD Signal:", self.macd_signal)
        tabs.addTab(tech_tab, "Indicators")

        # --- Tab 3: Risk & Failsafes ---
        risk_tab = QWidget()
        risk_layout = QFormLayout(risk_tab)

        # Take Profit Setup
        self.take_profit = QDoubleSpinBox()
        self.take_profit.setSuffix("%")
        self.take_profit.setRange(0, 1000)
        self.tp_preview = QLabel("Exit Price: £0.00")
        self.tp_preview.setStyleSheet("color: #2e7d32; font-weight: bold;")  # Green

        # Stop Loss Setup
        self.stop_loss = QDoubleSpinBox()
        self.stop_loss.setSuffix("%")
        self.stop_loss.setRange(0, 100)
        self.sl_preview = QLabel("Exit Price: £0.00")
        self.sl_preview.setStyleSheet("color: #c62828; font-weight: bold;")  # Red

        # Connect signals for live updates
        self.take_profit.valueChanged.connect(self.update_risk_previews)
        self.stop_loss.valueChanged.connect(self.update_risk_previews)
        self.target_price.valueChanged.connect(self.update_risk_previews)
        self.direction.currentTextChanged.connect(self.update_risk_previews)

        self.max_trades_day = QSpinBox()
        self.max_trades_day.setValue(3)

        self.portfolio_exposre = QDoubleSpinBox()
        self.portfolio_exposre.setSuffix("% of Balance")
        self.portfolio_exposre.setValue(5.0)

        self.trailing_stop = QDoubleSpinBox()
        self.trailing_stop.setSuffix("%")

        self.max_drawdown = QDoubleSpinBox()
        self.max_drawdown.setSuffix("%")

        self.cooldown_minutes = QSpinBox()
        self.cooldown_minutes.setValue(5)

        risk_layout.addRow("Take Profit Target:", self.take_profit)
        risk_layout.addRow("", self.tp_preview)  # Readout row
        risk_layout.addRow("Stop Loss Limit:", self.stop_loss)
        risk_layout.addRow("", self.sl_preview)  # Readout row
        risk_layout.addRow("Max Daily Trades:", self.max_trades_day)
        risk_layout.addRow("Portfolio Exposure:", self.portfolio_exposre)
        risk_layout.addRow("Trailing Stop:", self.trailing_stop)
        risk_layout.addRow("Max Drawdown:", self.max_drawdown)
        risk_layout.addRow("Cooldown (minutes):", self.cooldown_minutes)
        tabs.addTab(risk_tab, "Risk Management")

        layout.addWidget(tabs)

        # --- Action Buttons ---
        btn_layout = QHBoxLayout()
        self.backtest_btn = QPushButton("Open Backtester")
        self.backtest_btn.setStyleSheet("background-color: #6200ee; color: white;")
        self.backtest_btn.clicked.connect(self.open_backtester)

        self.save_btn = QPushButton("Save & Deploy")
        self.save_btn.clicked.connect(self.accept)

        btn_layout.addWidget(self.backtest_btn)
        btn_layout.addStretch()
        btn_layout.addWidget(self.save_btn)
        layout.addLayout(btn_layout)

    def update_risk_previews(self):
        """Calculates and displays the actual price targets based on %."""
        base_price = self.target_price.value()
        tp_percent = self.take_profit.value() / 100
        sl_percent = self.stop_loss.value() / 100
        is_long = self.direction.currentText() == "Long"

        if base_price <= 0:
            self.tp_preview.setText("Exit Price: (Set Target Price First)")
            self.sl_preview.setText("Exit Price: (Set Target Price First)")
            return

        if is_long:
            tp_price = base_price * (1 + tp_percent)
            sl_price = base_price * (1 - sl_percent)
        else:  # Short
            tp_price = base_price * (1 - tp_percent)
            sl_price = base_price * (1 + sl_percent)

        self.tp_preview.setText(f"Target Exit: £{tp_price:,.2f}")
        self.sl_preview.setText(f"Stop Exit: £{sl_price:,.2f}")

    async def calculate_spread(self, ticker):
        try:
            data = await self.parent().client.get_ticker(ticker)
            bid = data["bid"]
            ask = data["ask"]

            spread = ((ask - bid) / ask) * 100
            self.spread_tol.setValue(round(spread, 4))

            print(f"Spread auto-calculated: {spread:.4f}%")

        except Exception as e:
            print(f"Spread calculation error: {e}")

    def fill_current_price(self):
        if not self.parent() or not hasattr(self.parent(), "client"):
            print("Client unavailable")
            return

        ticker = self.windowTitle().split(":")[-1].strip()

        async def fetch_price():
            try:
                data = await self.parent().client.get_ticker(ticker)
                self.target_price.setValue(data["last"])
                print("Target price auto-filled")
            except Exception as e:
                print(f"Price fetch error: {e}")

        asyncio.create_task(fetch_price())

    def open_backtester(self):
        # Logic to open a new window would go here
        print("Opening Backtesting Environment...")

    def get_config(self):
        if self.auto_spread.isChecked():
            ticker = self.windowTitle().split(":")[-1].strip()
            asyncio.create_task(self.calculate_spread(ticker))

        return {
            "connection": {
                "api": self.price_api.currentText(),
                "interval": self.interval.currentText(),
                "order_type": self.order_type.currentText(),
                "direction": self.direction.currentText(),
                "slippage": self.slippage.value(),
                "spread_tolerance": self.spread_tol.value(),
                "target_price": self.target_price.value(),
            },
            "indicators": {
                "rsi": {
                    "enabled": self.use_rsi.isChecked(),
                    "period": self.rsi_period.value(),
                },
                "ema": {
                    "enabled": self.use_ema.isChecked(),
                    "fast": self.ema_fast.value(),
                    "slow": self.ema_slow.value(),
                },
                "macd": {
                    "enabled": self.use_macd.isChecked(),
                    "fast": self.macd_fast.value(),
                    "slow": self.macd_slow.value(),
                    "signal": self.macd_signal.value(),
                },
            },
            "risk": {
                "take_profit": self.take_profit.value(),
                "stop_loss": self.stop_loss.value(),
                "trailing_stop": self.trailing_stop.value(),
                "max_trades_day": self.max_trades_day.value(),
                "exposure": self.portfolio_exposre.value(),
                "max_drawdown": self.max_drawdown.value(),
                "cooldown_minutes": self.cooldown_minutes.value(),
            },
        }


class RiskEngine:
    def __init__(self):
        self.global_exposure = 0.0
        self.max_global_exposure = 100.0
        self.max_drawdown = 20.0
        self.current_drawdown = 0.0
        self.kill_switch_triggered = False

    def approve_trade(self, config):
        if self.kill_switch_triggered:
            print("🚨 Kill switch active")
            return False

        exposure = config["risk"]["exposure"]
        if self.global_exposure + exposure > self.max_global_exposure:
            print("⚠ Global exposure limit exceeded")
            return False

        if self.current_drawdown > self.max_drawdown:
            self.kill_switch_triggered = True
            print("🚨 Max drawdown exceeded. Trading halted.")
            return False

        return True

    def register_position(self, exposure):
        self.global_exposure += exposure

    def unregister_position(self, exposure):
        self.global_exposure -= exposure


class BotView(QWidget):
    def __init__(self, client):
        super().__init__()
        self.client = client
        self.active_bots = {}  # config_hash -> task
        self.bot_registry = {}  # config_hash -> metadata
        self.risk_engine = RiskEngine()

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(30, 30, 30, 30)
        self.layout.setSpacing(20)

        # --- Header ---
        self.header = QLabel("Trading Bot Manager")
        self.layout.addWidget(self.header)

        # --- Setup Panel ---
        self.setup_frame = QFrame()
        setup_layout = QHBoxLayout(self.setup_frame)

        self.ticker_input = QLineEdit()
        self.ticker_input.setPlaceholderText("Ticker (e.g. BTCUSDT)")

        self.config_btn = QPushButton("Set Strategy Config")
        self.config_btn.clicked.connect(self.open_config)

        self.start_btn = QPushButton("Deploy Bot")
        self.start_btn.setObjectName("PrimaryBtn")
        self.start_btn.clicked.connect(self.deploy_bot)

        setup_layout.addWidget(self.ticker_input)
        setup_layout.addWidget(self.config_btn)
        setup_layout.addWidget(self.start_btn)
        self.layout.addWidget(self.setup_frame)

        # --- Table ---
        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(
            ["Ticker", "Strategy", "Exposure", "Status", "Actions"]
        )
        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.layout.addWidget(self.table)

        self.current_config = None

    def generate_bot_hash(self, ticker, config):
        payload = {
            "ticker": ticker,
            "config": config,
        }
        serialized = json.dumps(payload, sort_keys=True)
        return hashlib.sha256(serialized.encode()).hexdigest()

    def open_config(self):
        ticker = self.ticker_input.text().upper() or "Unknown"
        dialog = ConfigDialog(self, ticker)
        if dialog.exec():
            self.current_config = dialog.get_config()
            print(f"Config Saved: {self.current_config}")

    @asyncSlot()
    async def deploy_bot(self):
        ticker = self.ticker_input.text().upper()

        if not ticker or not self.current_config:
            print("Please set ticker and configuration first")
            return

        bot_hash = self.generate_bot_hash(ticker, self.current_config)

        # 🚨 DUPLICATE PREVENTION
        if bot_hash in self.active_bots:
            print("⚠ Identical bot already running.")
            return

        # 🚨 RISK APPROVAL
        if not self.risk_engine.approve_trade(self.current_config):
            print("Trade rejected by Risk Engine")
            return

        row = self.table.rowCount()
        self.table.insertRow(row)

        self.table.setItem(row, 0, QTableWidgetItem(ticker))
        self.table.setItem(
            row,
            1,
            QTableWidgetItem(
                f"{self.current_config['connection']['direction']} | "
                f"{self.current_config['connection']['api']}"
            ),
        )
        self.table.setItem(
            row, 2, QTableWidgetItem(f"{self.current_config['risk']['exposure']}%")
        )
        self.table.setItem(row, 3, QTableWidgetItem("Running"))

        stop_btn = QPushButton("Stop")
        stop_btn.clicked.connect(lambda: self.stop_bot(bot_hash))
        self.table.setCellWidget(row, 4, stop_btn)

        task = asyncio.create_task(
            self.bot_logic(ticker, self.current_config, row, bot_hash)
        )

        self.active_bots[bot_hash] = task
        self.bot_registry[bot_hash] = {
            "ticker": ticker,
            "config": self.current_config,
            "row": row,
            "started": datetime.utcnow().isoformat(),
        }

        self.risk_engine.register_position(self.current_config["risk"]["exposure"])

        print(f"✅ Bot deployed | Hash: {bot_hash[:8]}")

    async def bot_logic(self, ticker, config, row_index, bot_hash):
        try:
            cooldown = config["risk"]["cooldown_minutes"] * 60

            while True:
                await asyncio.sleep(5)

                # status_item = self.table.item(row_index, 3)
                # status_item.setText("Monitoring Market")
                direction = config["connection"]["direction"]
                target_price = config["connection"]["target_price"]

                # Simulated price
                price = target_price  # Replace with live price

                if direction == "Long":
                    if price <= target_price:
                        status_item.setText("LONG Entry Triggered")
                elif direction == "Short":
                    if price >= target_price:
                        status_item.setText("SHORT Entry Triggered")

                # Example simulated logic
                if config["indicators"]["rsi"]["enabled"]:
                    status_item.setText("RSI Strategy Active")

                await asyncio.sleep(cooldown)

        except asyncio.CancelledError:
            print(f"Bot for {ticker} stopped.")
        except Exception as e:
            print(f"Bot Error: {e}")

    def stop_bot(self, bot_hash):
        if bot_hash in self.active_bots:
            exposure = self.bot_registry[bot_hash]["config"]["risk"]["exposure"]

            self.active_bots[bot_hash].cancel()
            del self.active_bots[bot_hash]

            self.risk_engine.unregister_position(exposure)

            print("🛑 Bot stopped")
