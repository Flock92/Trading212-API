import asyncio
from datetime import datetime

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import (
    QAbstractItemView,
    QFrame,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)


class DashboardView(QWidget):
    def __init__(self, client):
        super().__init__()
        self.client = client
        self.setObjectName("DashboardView")
        self.monitored_tickers = {}  # Map Symbol -> Row Index
        self.last_prices = {}  # Track previous price for color flashes

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(30, 30, 30, 30)
        self.layout.setSpacing(20)

        # --- Header & Stats (Unchanged) ---
        self._setup_header()
        self._setup_stats()

        # --- Live Market Monitor ---
        self.ticker_header = QLabel("Live Market Monitor")
        self.ticker_header.setStyleSheet(
            "font-size: 18px; font-weight: bold; margin-top: 10px; color: #90A4AE;"
        )
        self.layout.addWidget(self.ticker_header)

        self.ticker_table = self.create_ticker_table()
        self.layout.addWidget(self.ticker_table)

    def create_ticker_table(self):
        table = QTableWidget()
        # Increased to 5 columns to include Spread and high-res Timestamp
        table.setColumnCount(5)
        table.setHorizontalHeaderLabels(
            ["Symbol", "Bid / Ask", "Spread", "Last Sync", "Actions"]
        )
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        table.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        table.setShowGrid(False)
        table.setAlternatingRowColors(True)
        # Custom styling for the table rows
        table.verticalHeader().setVisible(False)
        return table

    def set_current_price(self, raw_data):
        """
        Parses: "QR|#QMAPR26|66.90|66.93|1772219477928"
        """
        try:
            parts = raw_data.split("|")
            if len(parts) < 5:
                return

            symbol = parts[1]
            bid = float(parts[2])
            ask = float(parts[3])
            ts_ms = int(parts[4])

            # Convert milliseconds timestamp to readable time
            last_sync = datetime.fromtimestamp(ts_ms / 1000.0).strftime("%H:%M:%S.%f")[
                :-3
            ]
            spread = ask - bid

            if symbol not in self.monitored_tickers:
                self._add_new_ticker_row(symbol)

            row = self.monitored_tickers[symbol]

            # 1. Update Bid/Ask Column
            ba_item = QTableWidgetItem(f"{bid:.2f} / {ask:.2f}")
            ba_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            # Price Direction Flash Logic
            mid = (bid + ask) / 2
            if symbol in self.last_prices:
                if mid > self.last_prices[symbol]:
                    ba_item.setForeground(Qt.GlobalColor.green)
                elif mid < self.last_prices[symbol]:
                    ba_item.setForeground(Qt.GlobalColor.red)
            self.last_prices[symbol] = mid

            self.ticker_table.setItem(row, 1, ba_item)

            # 2. Update Spread Column
            spread_item = QTableWidgetItem(f"{spread:.3f}")
            spread_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            spread_item.setForeground(Qt.GlobalColor.gray)
            self.ticker_table.setItem(row, 2, spread_item)

            # 3. Update Last Sync Column
            sync_item = QTableWidgetItem(last_sync)
            sync_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.ticker_table.setItem(row, 3, sync_item)

        except Exception as e:
            print(f"[Dashboard Update Error] {e}")

    def _add_new_ticker_row(self, symbol):
        row_pos = self.ticker_table.rowCount()
        self.ticker_table.insertRow(row_pos)
        self.monitored_tickers[symbol] = row_pos

        sym_item = QTableWidgetItem(symbol)
        sym_item.setForeground(Qt.GlobalColor.white)
        sym_item.setFlags(sym_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        self.ticker_table.setItem(row_pos, 0, sym_item)

        self.setup_action_buttons(row_pos, symbol)

    def setup_action_buttons(self, row, symbol):
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(5, 2, 5, 2)
        layout.setSpacing(8)

        # Style matches your "Deep Night" theme
        btn_style = (
            "font-weight: bold; border-radius: 4px; padding: 5px; min-width: 60px;"
        )

        buy_btn = QPushButton("BUY")
        buy_btn.setStyleSheet(f"background-color: #00FA9A; color: #121416; {btn_style}")
        buy_btn.clicked.connect(lambda: self.handle_quick_order(symbol, "BUY"))

        sell_btn = QPushButton("SELL")
        sell_btn.setStyleSheet(f"background-color: #FF4500; color: white; {btn_style}")
        sell_btn.clicked.connect(lambda: self.handle_quick_order(symbol, "SELL"))

        layout.addWidget(buy_btn)
        layout.addWidget(sell_btn)
        self.ticker_table.setCellWidget(row, 4, container)

    def handle_quick_order(self, symbol, side):
        print(f"[Order Executed] {side} {symbol} at Market")

    # --- UI Boilerplate ---
    def _setup_header(self):
        header_layout = QHBoxLayout()
        header = QLabel("Account Overview")
        header.setObjectName("DashboardHeader")
        self.last_updated_label = QLabel("Waiting for live data...")
        header_layout.addWidget(header)
        header_layout.addStretch()
        header_layout.addWidget(self.last_updated_label)
        self.layout.addLayout(header_layout)

    def _setup_stats(self):
        self.stats_layout = QHBoxLayout()
        self.card_total, self.val_total = self.create_stat_card(
            "Total Equity", "£0.00", "CardTotal"
        )
        self.card_free, self.val_free = self.create_stat_card(
            "Free Funds", "£0.00", "CardFree"
        )
        self.card_ppl, self.val_ppl = self.create_stat_card(
            "Live P/L", "£0.00", "CardPPL"
        )
        self.card_blocked, self.val_blocked = self.create_stat_card(
            "Margin", "£0.00", "CardBlocked"
        )
        for card in [self.card_total, self.card_free, self.card_ppl, self.card_blocked]:
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

    def update_ui(self, total, free, ppl, margin):
        self.val_total.setText(f"£{total:,.2f}")
        self.val_free.setText(f"£{free:,.2f}")
        self.val_ppl.setText(f"£{ppl:,.2f}")
        self.val_blocked.setText(f"£{margin:,.2f}")

        # --- P/L Dynamic Coloring ---
        # Determines if the value is profit (green), loss (red), or neutral
        if ppl > 0:
            status = "profit"
        elif ppl < 0:
            status = "loss"
        else:
            status = "neutral"

        # Apply the property for the stylesheet to pick up
        self.val_ppl.setProperty("status", status)

        # Force a style refresh (required for dynamic properties in Qt)
        self.val_ppl.style().unpolish(self.val_ppl)
        self.val_ppl.style().polish(self.val_ppl)

        now = datetime.now().strftime("%H:%M:%S")
        self.last_updated_label.setText(f"Last update: {now}")
