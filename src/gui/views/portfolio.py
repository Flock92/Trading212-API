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
        self.setObjectName("PortfolioView")  # Linked to QWidget#PortfolioView in CSS

        layout = QVBoxLayout(self)
        self.setLayout(layout)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(10)

        # --- Header ---
        self.header_layout = QHBoxLayout()
        self.header = QLabel("Open Positions")
        self.header.setObjectName("OrdersHeader")  # Uses the 24px bold font from CSS

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("🔍 Search ticker...")
        self.search_bar.setFixedWidth(200)
        self.search_bar.textChanged.connect(self.filter_table)

        self.header_layout.addWidget(self.header)
        self.header_layout.addStretch()
        self.header_layout.addWidget(self.search_bar)
        layout.addLayout(self.header_layout)

        # --- Main Table ---
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(
            ["Order ID", "Ticker", "Qty", "Avg Price", "Current", "P/L", "Actions"]
        )
        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.table.verticalHeader().setVisible(False)
        layout.addWidget(self.table)

        # --- Summary Bar ---
        self.summary_bar = QFrame()
        self.summary_bar.setObjectName(
            "StatusCard"
        )  # Linked to QFrame#StatusCard in CSS
        self.summary_layout = QHBoxLayout(self.summary_bar)

        self.total_label = QLabel("TOTAL PORTFOLIO P/L:")
        self.total_label.setObjectName(
            "SettingsSectionLabel"
        )  # Uses the muted uppercase style

        self.pl_value_label = QLabel("£0.00")
        self.pl_value_label.setObjectName(
            "StatValue"
        )  # Links to the dashboard value font
        self.pl_value_label.setProperty("status", "neutral")

        self.summary_layout.addWidget(self.total_label)
        self.summary_layout.addWidget(self.pl_value_label)
        self.summary_layout.addStretch()

        layout.addWidget(self.summary_bar)

    def update_table_data(self, positions):
        """Primary target for EventBus live data updates."""
        self.table.setRowCount(len(positions))

        for row, pos in enumerate(positions):
            symbol = pos.get("code", "N/A")
            pos_id = pos.get("positionId", "N/A")
            qty = pos.get("quantity", 0)
            avg_price = pos.get("averagePrice", 0)
            current_price = pos.get("currentPrice", 0)
            ppl = pos.get("ppl", 0)

            self.table.setItem(row, 0, QTableWidgetItem(pos_id))
            self.table.setItem(row, 1, QTableWidgetItem(symbol))
            self.table.setItem(row, 2, QTableWidgetItem(f"{qty:.4f}"))
            self.table.setItem(row, 3, QTableWidgetItem(f"£{avg_price:,.2f}"))
            self.table.setItem(row, 4, QTableWidgetItem(f"£{current_price:,.2f}"))

            # P/L Column
            pl_item = QTableWidgetItem(f"£{ppl:,.2f}")
            # Note: QTableWidgetItem colors aren't directly CSS-linked,
            # so we use your primary color palette here
            color_hex = "#00fa9a" if ppl >= 0 else "#ff4500"
            pl_item.setForeground(QColor(color_hex))
            self.table.setItem(row, 5, pl_item)

            # Close Button
            close_btn = QPushButton("Close")
            close_btn.setObjectName(
                "CloseOrderBtn"
            )  # Linked to QPushButton#CloseOrderBtn
            close_btn.clicked.connect(lambda chk, pid=pos_id: self.confirm_close(pid))
            self.table.setCellWidget(row, 6, close_btn)

        self.calculate_summary()

    def calculate_summary(self):
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

        # Apply CSS property for P/L color
        status = "profit" if total_pl >= 0 else "loss"
        self.pl_value_label.setProperty("status", status)

        # Force a style refresh
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
            await self.client.api().positions.close_position(order_id)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to close: {e}")
