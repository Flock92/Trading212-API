import asyncio
import sys
from datetime import datetime

import darkdetect
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QStackedWidget,
    QStatusBar,
    QVBoxLayout,
    QWidget,
)
from qasync import QEventLoop

# Corrected Imports
from src.gui.styles import get_stylesheet
from src.apitConnect.event import event_bus, EventType, Event, Listener # Added Listener
from src.apitConnect.core.network.supervisor import ApiSupervisor
from src.apitConnect.models.websocket import TickerModel, ScheduleBatchModel, AccountModel

from .views.bot import BotView
from .views.dashboard import DashboardView
from .views.login import LoginView
from .views.portfolio import PortfolioView
from .views.settings import SettingsView

class TickerDataManager:
    def __init__(self, dashboard_view):
        self.dashboard_view = dashboard_view
        self.latest_prices = {}

    async def on_tick_received(self, event: Event):
        # The 'processed' key now contains our Data Class objects
        data = event.data.get("processed")

        if not data:
            return

        # --- Case 1: Live Price Tickers ---
        if isinstance(data, TickerModel):
            symbol = data.symbol

            if hasattr(self.dashboard_view, "symbol_input"):
                current_input = self.dashboard_view.symbol_input.text().strip().upper()
                # TickerModel already handles the '#' stripping in our model definition
                if symbol == current_input:
                    QTimer.singleShot(0, lambda: self.dashboard_view.set_current_price(data))

        # --- Case 2: Market Schedules (The batch sync you received) ---
        elif isinstance(data, ScheduleBatchModel):

            # Update a local cache of market statuses
            for item in data.items:
                # item is a MarketScheduleItem object
                market_id = item.id
                status = item.status # 'OPEN' or 'CLOSED'

                # Example: Update a 'Market Status' indicator on the dashboard
                if hasattr(self.dashboard_view, "update_market_status"):
                    QTimer.singleShot(0, lambda: self.dashboard_view.update_market_status(item))

        # --- Case 3: Fallback for raw strings (Internal safety) ---
        elif isinstance(data, str):

            try:
                parts = data.split("|")
                if len(parts) >= 3:
                    symbol, price = parts[1].replace("#", ""), float(parts[2])
                    self.latest_prices[symbol] = price
            except Exception:
                pass

class TradingApp(QMainWindow):
    def __init__(self, client):
        super().__init__(flags=Qt.WindowType.Window)
        self.client = client
        self.event_bus = event_bus 

        self.setWindowTitle("Apit212")
        self.resize(1150, 650)

        # Main Layout Setup
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.main_layout = QHBoxLayout(self.main_widget)

        # Sidebar setup
        self.sidebar = QFrame()
        self.sidebar.setFixedWidth(200)
        self.sidebar_layout = QVBoxLayout(self.sidebar)
        
        # Navigation
        self.btn_dash = self.create_nav_btn("Dashboard", lambda: self.show_view(1))
        self.btn_port = self.create_nav_btn("Portfolio", lambda: self.show_view(2))
        self.btn_bots = self.create_nav_btn("Bots", lambda: self.show_view(3))
        self.btn_sett = self.create_nav_btn("Settings", lambda: self.show_view(4))

        self.sidebar_layout.addWidget(self.btn_dash)
        self.sidebar_layout.addWidget(self.btn_port)
        self.sidebar_layout.addWidget(self.btn_bots)
        self.sidebar_layout.addStretch()
        self.sidebar_layout.addWidget(self.btn_sett)

        # View Stack
        self.content_stack = QStackedWidget()
        self.view_login = LoginView(self.client, on_login_success=self.unlock_app)
        self.view_dash = DashboardView(self.client)
        self.view_port = PortfolioView(self.client)
        self.view_bots = BotView(self.client)
        self.view_sett = SettingsView(self.client)

        self.content_stack.addWidget(self.view_login)
        self.content_stack.addWidget(self.view_dash)
        self.content_stack.addWidget(self.view_port)
        self.content_stack.addWidget(self.view_bots)
        self.content_stack.addWidget(self.view_sett)

        self.main_layout.addWidget(self.sidebar)
        self.main_layout.addWidget(self.content_stack)

        # Status Bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_ping = QLabel("API: Offline")
        self.status_bar.addPermanentWidget(self.status_ping)

        self.sidebar.hide()
        self.status_bar.hide()
        
        self.ticker_manager = TickerDataManager(self.view_dash)
        self._active_listeners = []

    def create_nav_btn(self, text, callback):
        btn = QPushButton(text)
        btn.setFixedHeight(45)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.clicked.connect(callback)
        return btn

    def show_view(self, index):
        self.content_stack.setCurrentIndex(index)

    async def _register_event_handlers(self):
        # 1. Ticker Listener
        ticker_listener = Listener(
            event_type=EventType.PIPELINE,
            handler=self.ticker_manager.on_tick_received
        )
        
        # 2. Account/Response Listener
        response_listener = Listener(
            event_type=EventType.API_RESPONSE,
            handler=self.on_account_update
        )

        self._active_listeners.append(asyncio.create_task(ticker_listener.start(self.event_bus)))
        self._active_listeners.append(asyncio.create_task(response_listener.start(self.event_bus)))

    def unlock_app(self, api_instance=None):
        self.sidebar.show()
        self.status_bar.show()
        asyncio.create_task(self._register_event_handlers())
        self.show_view(1)

    async def on_account_update(self, event: Event):
        """
        Handles incoming account data using the pre-parsed AccountModel.
        Expects event.data to contain the 'processed' AccountModel instance.
        """
        try:
            # 1. Update Global Status Bar
            last_sync = event.timestamp.strftime("%H:%M:%S")
            # Thread-safe UI update for the status ping
            QTimer.singleShot(0, lambda: self.status_ping.setText(f"API: LIVE ({last_sync})"))

            # 2. Extract the AccountModel from the event
            # Assuming your parser puts the model in event.data['processed']
            account: AccountModel = event.data.get("processed")

            if not account or not isinstance(account, AccountModel):
                # Log a warning if the data is malformed to avoid 'zeroing' the UI
                print("[Account Update] Received empty or invalid model. Skipping UI refresh.")
                return

            # 3. Update Dashboard View
            # We pass the full object so the dashboard can show Total, Free, and Trade Counts
            if hasattr(self.view_dash, "update_ui"):
                QTimer.singleShot(0, lambda: self.view_dash.update_ui(account))

            # 4. Update Portfolio/Positions View
            # We pass the list of items stored in the model
            if hasattr(self.view_port, "update_table_data"):
                QTimer.singleShot(0, lambda: self.view_port.update_table_data(account.open_items))

        except Exception as e:
            print(f"[Account Update Error] {e}")

async def ui_event_listener(window):
    system_queue = await event_bus.subscribe(EventType.SYSTEM)
    error_queue = await event_bus.subscribe(EventType.ERROR)

    while True:
        try:
            # Create tasks for the queues
            s_task = asyncio.create_task(system_queue.get())
            e_task = asyncio.create_task(error_queue.get())

            done, pending = await asyncio.wait(
                [s_task, e_task],
                return_when=asyncio.FIRST_COMPLETED
            )

            for task in done:
                event: Event = task.result()
                if event.type == EventType.SYSTEM:
                    msg = event.message
                    QTimer.singleShot(0, lambda: window.status_ping.setText(f"API: {msg}"))
                elif event.type == EventType.ERROR:
                    print(f"[GUI ERROR] {event.message}")

            for task in pending:
                task.cancel()

        except asyncio.CancelledError:
            break
        except Exception:
            await asyncio.sleep(1)

def run_gui(client):
    app = QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    window = TradingApp(client)
    window.show()

    # CRITICAL: Start the listener task
    loop.create_task(ui_event_listener(window))

    try:
        loop.run_forever()
    finally:
        loop.close()