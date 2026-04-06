import asyncio
from datetime import datetime

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import (
    QAbstractItemView,
    QFrame,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
    QScrollArea
)
from src.apitConnect.models.websocket import TickerModel, AccountModel, ScheduleBatchModel
from src.apitConnect.event import Event, event_bus, EventType


class DashboardView(QWidget):
    def __init__(self, client):
        super().__init__()
        self.client = client
        self.setObjectName("DashboardView")
        self.monitored_tickers = {}  # Map Symbol -> Row Index
        self.last_prices = {}  # Track previous price for color flashes
        self.market_badges = {}

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(30, 30, 30, 30)
        self.layout.setSpacing(20)

        # --- Header & Stats ---
        self._setup_header()
        self._setup_stats()

        # --- Live Market Monitor Header + Add Bar ---
        ticker_header_layout = QHBoxLayout()
        self._setup_market_monitor_section()
        
        self.ticker_header = QLabel("Live Market Monitor")
        self.ticker_header.setStyleSheet(
            "font-size: 18px; font-weight: bold; color: #90A4AE;"
        )
        
        # NEW: Add Ticker Input
        self.add_ticker_input = QLineEdit()
        self.add_ticker_input.setPlaceholderText("Add Ticker (e.g. AAPL)...")
        self.add_ticker_input.setFixedWidth(200)
        self.add_ticker_input.returnPressed.connect(self._handle_manual_add)
        self.add_ticker_input.setStyleSheet("""
            QLineEdit {
                background: #1E2225; border: 1px solid #333; 
                color: white; padding: 5px; border-radius: 4px;
            }
        """)

        ticker_header_layout.addWidget(self.header) # Account Overview Label
        ticker_header_layout.addStretch()
        ticker_header_layout.addWidget(self.add_ticker_input)
        
        # Note: We replace the old header call with this layout
        self.layout.addLayout(ticker_header_layout)

        # --- Market Monitor Table ---
        self.ticker_table = self.create_ticker_table()
        self.layout.addWidget(self.ticker_table)

        # --- Footer Market Status (Needed for update_market_status) ---
        self._setup_footer()

        self.monitored_tickers = {} 
        self.market_schedule_cache = None  # NEW: Store the latest batch here
        self.latest_ticker_data = {}

    # --- NEW FEATURE: Get Active Tickers ---
    def get_monitored_symbols(self) -> list:
        """Returns a list of all ticker symbols currently in the table."""
        return list(self.monitored_tickers.keys())

    # --- NEW FEATURE: Check Market Status ---
    def is_market_open(self, market_id: int) -> bool:
        """Checks if a specific market ID is currently tradable."""
        if not self.market_schedule_cache:
            return False
        
        market = self.market_schedule_cache.lookup.get(market_id)
        return market.is_tradable if market else False

    def _setup_market_monitor_section(self):
        """Creates a horizontal scroll area for all market statuses."""
        section_label = QLabel("Global Market Status")
        section_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #607D8B; margin-top: 5px;")
        self.layout.addWidget(section_label)

        self.market_scroll = QScrollArea()
        self.market_scroll.setWidgetResizable(True)
        self.market_scroll.setFixedHeight(60)
        self.market_scroll.setStyleSheet("background: transparent; border: none;")
        
        self.market_container = QWidget()
        self.market_container_layout = QHBoxLayout(self.market_container)
        self.market_container_layout.setContentsMargins(0, 0, 0, 0)
        self.market_container_layout.setSpacing(15)
        self.market_container_layout.addStretch() # Push everything to the left
        
        self.market_scroll.setWidget(self.market_container)
        self.layout.addWidget(self.market_scroll)

    def update_market_status(self, batch: ScheduleBatchModel):
        """Updates both the badge bar and the footer labels."""
        self.market_schedule_cache = batch 

        # Update/Create Badges
        for item in batch.items:
            market_id = item.id
            if market_id not in self.market_badges:
                self._create_market_badge(item)
            
            badge_label = self.market_badges[market_id]
            dot_color = "#00fa9a" if item.is_tradable else "#ff4500"
            badge_label.setText(f"● {market_id}: {item.status}")
            badge_label.setStyleSheet(f"color: {dot_color}; font-weight: bold; font-size: 11px;")

        # Update Footer
        us_market = batch.lookup.get(2) 
        if us_market:
            color = "#00fa9a" if us_market.is_tradable else "#ff4500"
            self.us_status_dot.setStyleSheet(f"background-color: {color}; border-radius: 5px;")
            self.us_status_label.setText(f"US: {us_market.status}")

        open_count = sum(1 for item in batch.items if item.is_tradable)
        self.footer_status.setText(f"Global Markets: {open_count} Open / {batch.count} Total")

    def _create_market_badge(self, item):
        """Helper to create a single market status widget."""
        badge = QLabel()
        # We use a stretch-friendly layout, so we insert BEFORE the stretch
        self.market_container_layout.insertWidget(self.market_container_layout.count() - 1, badge)
        self.market_badges[item.id] = badge

    def _setup_footer(self):
        self.footer_layout = QHBoxLayout()
        self.us_status_dot = QFrame()
        self.us_status_dot.setFixedSize(10, 10)
        self.us_status_dot.setStyleSheet("background-color: gray; border-radius: 5px;")
        
        self.us_status_label = QLabel("US Market: Unknown")
        self.footer_status = QLabel("Global Markets: 0 Open")
        
        self.footer_layout.addWidget(self.us_status_dot)
        self.footer_layout.addWidget(self.us_status_label)
        self.footer_layout.addStretch()
        self.footer_layout.addWidget(self.footer_status)
        self.layout.addLayout(self.footer_layout)

    def _handle_manual_add(self):
        symbol = self.add_ticker_input.text().strip().upper()
        if symbol and symbol not in self.monitored_tickers:
            self._add_new_ticker_row(symbol)
            self.add_ticker_input.clear()
            # If your client has a subscription method, call it here:
            # self.client.subscribe_ticker(symbol)

    def create_ticker_table(self):
        table = QTableWidget()
        table.setColumnCount(5)
        table.setHorizontalHeaderLabels(["Symbol", "Bid / Ask", "Spread", "Last Sync", "Actions"])
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        table.setShowGrid(False)
        table.setAlternatingRowColors(True)
        table.verticalHeader().setVisible(False)
        return table

    def set_current_price(self, ticker: TickerModel):
        if not ticker or not isinstance(ticker, TickerModel):
            return

        try:
            symbol = ticker.symbol
            self.latest_ticker_data[symbol] = ticker
            last_sync = datetime.fromtimestamp(ticker.timestamp / 1000.0).strftime("%H:%M:%S.%f")[:-3]

            if symbol not in self.monitored_tickers:
                # Only add if we have space (optional safety check)
                if len(self.monitored_tickers) >= 50: 
                    return 
                self._add_new_ticker_row(symbol)

            row = self.monitored_tickers[symbol]

            # Price Direction Flash Logic
            ba_item = QTableWidgetItem(f"{ticker.bid:.2f} / {ticker.ask:.2f}")
            ba_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            
            if symbol in self.last_prices:
                if ticker.mid_price > self.last_prices[symbol]:
                    ba_item.setForeground(Qt.GlobalColor.green)
                elif ticker.mid_price < self.last_prices[symbol]:
                    ba_item.setForeground(Qt.GlobalColor.red)

            self.last_prices[symbol] = ticker.mid_price
            self.ticker_table.setItem(row, 1, ba_item)

            # Spread & Sync Update
            self.ticker_table.setItem(row, 2, QTableWidgetItem(f"{ticker.spread:.3f}"))
            self.ticker_table.setItem(row, 3, QTableWidgetItem(last_sync))
            
            # Align spread and sync
            self.ticker_table.item(row, 2).setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.ticker_table.item(row, 3).setTextAlignment(Qt.AlignmentFlag.AlignCenter)

        except Exception as e:
            print(f"[Dashboard UI Error] {e}")

    def _add_new_ticker_row(self, symbol):
        row_pos = self.ticker_table.rowCount()
        self.ticker_table.insertRow(row_pos)
        self.monitored_tickers[symbol] = row_pos

        sym_item = QTableWidgetItem(symbol)
        sym_item.setForeground(Qt.GlobalColor.white)
        self.ticker_table.setItem(row_pos, 0, sym_item)
        self.setup_action_buttons(row_pos, symbol)

    def setup_action_buttons(self, row, symbol):
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(5, 2, 5, 2)
        layout.setSpacing(5)
        
        btn_style = "font-weight: bold; border-radius: 4px; padding: 5px; min-width: 50px;"

        # --- Buy Button ---
        buy_btn = QPushButton("BUY")
        buy_btn.setStyleSheet(f"background-color: #00FA9A; color: #121416; {btn_style}")
        buy_btn.clicked.connect(lambda: self.handle_quick_order(symbol, "BUY"))

        # --- Sell Button ---
        sell_btn = QPushButton("SELL")
        sell_btn.setStyleSheet(f"background-color: #FF4500; color: white; {btn_style}")
        sell_btn.clicked.connect(lambda: self.handle_quick_order(symbol, "SELL"))

        # --- NEW: Remove from Monitor Button ---
        # This keeps the monitor clean without closing actual positions
        remove_btn = QPushButton("×")
        remove_btn.setToolTip("Remove from monitor")
        remove_btn.setStyleSheet("color: #555; font-size: 16px; background: transparent;")
        remove_btn.clicked.connect(lambda: self._remove_ticker_from_ui(symbol))

        layout.addWidget(buy_btn)
        layout.addWidget(sell_btn)
        layout.addWidget(remove_btn)
        self.ticker_table.setCellWidget(row, 4, container)

    def handle_quick_order(self, symbol: str, side: str):
        """
        Triggers a market value order via the EventBus.
        """

        ticker = self.latest_ticker_data.get(symbol)

        if not ticker:
            print(f"[Quick Trade] Error: No price data yet for {symbol}")
            return

        target_price = ticker.mid_price

        # 1. Define the trade parameters
        # Adjust 'value' based on your risk management (e.g., £100 per quick trade)
        # For CFD Market Value orders, 'side' is usually handled by positive/negative quantity 
        # or specific payload keys. Based on your endpoint:
        trade_payload = {
            "ticker": symbol,
            "value": 3,       # Example: £100 position
            "targetPrice": target_price,     # 0 for Market Order
        }

        # 2. Create the API Request Event
        # 'command' must match a key in APPROVED_CALLS (ApiSupervisor)
        event = Event.api_request(
            command="market_order",
            data=trade_payload
        )

        print(f"[GUI -> API] Requesting {side} {symbol} (CorrID: {event.correlation_id})")

        # 3. Emit the event asynchronously
        # We use asyncio.create_task because we are in a synchronous QPipe/Qt slot
        asyncio.create_task(event_bus.emit(event))

    def _remove_ticker_from_ui(self, symbol):
        """Removes the ticker from the table and the tracking dict."""
        if symbol in self.monitored_tickers:
            row = self.monitored_tickers[symbol]
            self.ticker_table.removeRow(row)
            del self.monitored_tickers[symbol]
            # Re-index remaining rows
            for i in range(self.ticker_table.rowCount()):
                sym = self.ticker_table.item(i, 0).text()
                self.monitored_tickers[sym] = i

    def update_ui(self, account: AccountModel):
        if not account: return
        self.val_total.setText(f"£{account.total:,.2f}")
        self.val_free.setText(f"£{account.free:,.2f}")
        self.val_ppl.setText(f"£{account.ppl:,.2f}")
        self.val_blocked.setText(f"£{account.margin:,.2f}")

        status = "profit" if account.ppl > 0 else "loss" if account.ppl < 0 else "neutral"
        self.val_ppl.setProperty("status", status)
        self.val_ppl.style().unpolish(self.val_ppl)
        self.val_ppl.style().polish(self.val_ppl)

        now = datetime.now().strftime("%H:%M:%S")
        self.last_updated_label.setText(f"Last update: {now}")

    def _setup_header(self):
        # Header is now handled in __init__ ticker_header_layout for better alignment
        self.header = QLabel("Account Overview")
        self.header.setObjectName("DashboardHeader")
        self.last_updated_label = QLabel("Waiting for live data...")

    def _setup_stats(self):
        self.stats_layout = QHBoxLayout()
        cards = [
            ("Total Equity", "£0.00", "CardTotal"),
            ("Free Funds", "£0.00", "CardFree"),
            ("Live P/L", "£0.00", "CardPPL"),
            ("Margin", "£0.00", "CardBlocked")
        ]
        for title, val, cid in cards:
            card, label = self.create_stat_card(title, val, cid)
            setattr(self, f"val_{cid.lower().replace('card', '')}", label)
            self.stats_layout.addWidget(card)
        self.layout.addLayout(self.stats_layout)

    def create_stat_card(self, title, value, card_id):
        card = QFrame()
        card.setObjectName(card_id)
        card.setProperty("class", "StatCard")
        l = QVBoxLayout(card)
        t = QLabel(title)
        t.setObjectName("StatTitle")
        v = QLabel(value)
        v.setObjectName("StatValue")
        l.addWidget(t)
        l.addWidget(v)
        return card, v
    
    def _setup_search_logic(self):
        # Connect your existing add_ticker_input to a filter method instead
        self.add_ticker_input.textChanged.connect(self.filter_ticker_table)

    def filter_ticker_table(self, text):
        search_term = text.lower()
        for row in range(self.ticker_table.rowCount()):
            item = self.ticker_table.item(row, 0) # Symbol column
            if item:
                self.ticker_table.setRowHidden(row, search_term not in item.text().lower())
