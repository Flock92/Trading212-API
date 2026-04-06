import asyncio
import uuid
from dataclasses import dataclass, field

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)


class PortfolioView(QWidget):
    def __init__(self, client):
        super().__init__()
        self.client = client
        self.setObjectName("PortfolioView")

        layout = QVBoxLayout(self)
        self.setLayout(layout)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(10)

        # --- Header ---
        self.header_layout = QHBoxLayout()
        
        # Container for Title + Badge
        title_container = QVBoxLayout()
        self.header = QLabel("Open Positions")
        self.header.setObjectName("OrdersHeader")
        
        # NEW: Trade Count Badge
        self.count_badge = QLabel("0 Active Trades")
        self.count_badge.setStyleSheet("color: #AAAAAA; font-size: 11px; font-weight: normal;")
        
        title_container.addWidget(self.header)
        title_container.addWidget(self.count_badge)
        self.header_layout.addLayout(title_container)

        self.header_layout.addStretch()
        
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("🔍 Search ticker...")
        self.search_bar.setFixedWidth(200)
        self.search_bar.textChanged.connect(self.filter_table)

        self.header_layout.addWidget(self.search_bar)
        layout.addLayout(self.header_layout)

        # --- Main Table ---
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(
            ["Order ID", "Ticker", "Qty", "Avg Price", "Current", "P/L", "Actions"]
        )
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setVisible(False)
        layout.addWidget(self.table)

        # --- Summary Bar ---
        self.summary_bar = QFrame()
        self.summary_bar.setObjectName("StatusCard")
        self.summary_layout = QHBoxLayout(self.summary_bar)

        self.total_label = QLabel("TOTAL PORTFOLIO P/L:")
        self.total_label.setObjectName("SettingsSectionLabel")

        self.pl_value_label = QLabel("£0.00")
        self.pl_value_label.setObjectName("StatValue")
        self.pl_value_label.setProperty("status", "neutral")

        self.summary_layout.addWidget(self.total_label)
        self.summary_layout.addWidget(self.pl_value_label)
        self.summary_layout.addStretch()

        layout.addWidget(self.summary_bar)

    def update_table_data(self, account: AccountModel):
        """
        Updates the UI table using the full AccountModel.
        """
        # 1. Guard against empty data
        if not account or not hasattr(account, 'open_items'):
            return
    
        # 2. Update Header Badge (Using AccountModel stats)
        if hasattr(self, 'count_badge'):
            self.count_badge.setText(
                f"{account.open_trades_count} Active | {account.pending_orders_count} Pending"
            )
    
        # 3. Process Positions
        positions = account.open_items
        self.table.setRowCount(len(positions))
    
        for row, pos in enumerate(positions):
            # Since we updated the parser, pos is now a PositionModel instance
            pos_id = pos.id
            symbol = pos.symbol.replace("#", "")
            qty = pos.quantity
            avg_price = pos.averagePrice
            # Note: If currentPrice isn't in your PositionModel yet, 
            # you might use pos.value / pos.quantity or 0.0
            current_price = getattr(pos, 'currentPrice', 0.0) 
            ppl = pos.ppl
    
            # Set table items
            self.table.setItem(row, 0, QTableWidgetItem(str(pos_id)))
            self.table.setItem(row, 1, QTableWidgetItem(symbol))
            
            # Quantity and Prices
            qty_item = QTableWidgetItem(f"{qty:.4f}")
            qty_item.setForeground(QColor("#00fa9a" if qty > 0 else "#ff4500"))
            self.table.setItem(row, 2, qty_item)
            
            self.table.setItem(row, 3, QTableWidgetItem(f"£{avg_price:,.2f}"))
            self.table.setItem(row, 4, QTableWidgetItem(f"£{current_price:,.2f}"))
    
            # P/L Column with dynamic coloring
            pl_text = f"£{ppl:,.2f}"
            pl_item = QTableWidgetItem(pl_text)
            pl_color = "#00fa9a" if ppl >= 0 else "#ff4500"
            pl_item.setForeground(QColor(pl_color))
            pl_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 5, pl_item)
    
            # Close Button Action
            close_btn = QPushButton("Close")
            close_btn.setObjectName("CloseOrderBtn")
            # pid=pos_id freezes the ID for this specific row's lambda
            close_btn.clicked.connect(lambda chk, pid=pos_id: self.confirm_close(pid))
            self.table.setCellWidget(row, 6, close_btn)
    
        # Update footer summary if it exists
        if hasattr(self, 'calculate_summary'):
            self.calculate_summary()

    def calculate_summary(self):
        """Calculates total P/L based on visible rows only (respects filtering)."""
        total_pl = 0.0
        for row in range(self.table.rowCount()):
            if not self.table.isRowHidden(row):
                pl_item = self.table.item(row, 5)
                if pl_item:
                    try:
                        clean_text = (
                            pl_item.text().replace("£", "").replace(",", "").strip()
                        )
                        total_pl += float(clean_text)
                    except ValueError:
                        continue

        self.pl_value_label.setText(f"£{total_pl:,.2f}")
        status = "profit" if total_pl >= 0 else "loss"
        self.pl_value_label.setProperty("status", status)
        
        self.pl_value_label.style().unpolish(self.pl_value_label)
        self.pl_value_label.style().polish(self.pl_value_label)

    def filter_table(self, text):
        search_term = text.lower()
        for row in range(self.table.rowCount()):
            item = self.table.item(row, 1)
            if item:
                should_show = search_term in item.text().lower()
                self.table.setRowHidden(row, not should_show)
        self.calculate_summary()

    def confirm_close(self, order_id):
        reply = QMessageBox.question(
            self,
            "Confirm Close",
            f"Are you sure you want to close order {order_id}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            asyncio.create_task(self.execute_close(order_id))

    async def execute_close(self, order_id):
        try:
            # Note: Ensure the API path matches your current client implementation
            await self.client.api().positions.close_position(order_id)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to close: {e}")