def get_stylesheet(theme="Dark"):
    """
    Returns the application stylesheet based on the selected theme.
    Supported themes: "Dark", "Light"
    """

    # Define Theme Variables
    if theme == "Light":
        bg_main = "#F5F5F5"
        bg_sidebar = "#E0E0E0"
        bg_card = "#FFFFFF"
        text_main = "#202020"
        text_muted = "#666666"
        border = "#CCCCCC"
        input_bg = "#FFFFFF"
        selection_bg = "#1F538D"
        selection_text = "#FFFFFF"
        # Specific for dropdown lists
        item_hover = "#E5E5E5"
    else:
        # Default Dark Theme
        bg_main = "#121212"
        bg_sidebar = "#1A1A1A"
        bg_card = "#1E1E1E"
        text_main = "#E2E2E2"
        text_muted = "#AAAAAA"
        border = "#333333"
        input_bg = "#252525"
        selection_bg = "#2A5C91"
        selection_text = "#FFFFFF"
        # Specific for dropdown lists
        item_hover = "#383838"

    return f"""
/* --- Global Settings --- */
/* Apply text color to EVERYTHING by default to prevent "invisible" text */
QWidget {{
    color: {text_main};
    font-family: "Segoe UI", "Roboto", "Arial";
    font-size: 14px;
}}

QMainWindow,
QWidget#CentralWidget,
QWidget#LoginView,
QWidget#DashboardView,
QWidget#PortfolioView,
QWidget#SettingsView,
QWidget#OrdersView {{
    background-color: {bg_main};
}}

QLabel, QCheckBox, QRadioButton {{
    background-color: transparent;
}}

/* --- Sidebar Styling --- */
QFrame#Sidebar {{
    background-color: {bg_sidebar};
    border-right: 1px solid {border};
}}

QLabel#SidebarLogo {{
    font-size: 22px;
    font-weight: bold;
    padding: 10px;
}}

/* --- Navigation Buttons --- */
QPushButton {{
    background-color: transparent;
    color: {text_muted};
    text-align: left;
    padding: 8px 20px;
    border: none;
    border-radius: 4px;
    font-weight: 500;
}}

QPushButton:hover {{
    background-color: {border};
    color: {text_main};
}}

QPushButton[active="true"] {{
    background-color: #1F538D;
    color: white;
    border-left: 3px solid #00FA9A;
}}

/* --- Specific Button Overrides --- */
QPushButton#PrimaryBtn,
QPushButton#SecondaryBtn,
QPushButton#LogoutBtn,
QPushButton#RefreshBtn,
QPushButton#SaveSettingsBtn {{
    text-align: center;
}}

QPushButton#PrimaryBtn {{
    background-color: #1F538D;
    color: white;
    font-weight: bold;
}}

QPushButton#SecondaryBtn {{
    background-color: {border};
}}

QPushButton#LogoutBtn {{
    background-color: #2A1A1A;
    color: #FF5252;
    border: 1px solid #442222;
}}

/* --- Dashboard & Stats --- */
QLabel#DashboardHeader, QLabel#SettingsHeader, QLabel#OrdersHeader {{
    font-size: 24px;
    font-weight: bold;
}}

QFrame[class="StatCard"] {{
    background-color: {bg_card};
    border: 1px solid {border};
    border-radius: 8px;
}}

QLabel#StatTitle {{
    color: {text_muted};
    font-size: 12px;
    text-transform: uppercase;
    font-weight: bold;
}}

QLabel#StatValue[status="profit"] {{ color: #00FA9A; }}
QLabel#StatValue[status="loss"] {{ color: #FF4500; }}

/* --- Tables --- */
QTableWidget {{
    background-color: {bg_sidebar};
    alternate-background-color: {bg_card};
    gridline-color: {border};
    border: 1px solid {border};
    selection-background-color: {selection_bg};
    selection-color: {selection_text};
}}

QHeaderView::section {{
    background-color: {input_bg};
    padding: 8px;
    border: none;
    border-bottom: 2px solid {border};
}}

/* --- Inputs & Dropdowns --- */
QLineEdit, QComboBox, QSpinBox {{
    background-color: {input_bg};
    border: 1px solid {border};
    border-radius: 4px;
    padding: 6px;
    color: {text_main};
}}

QLineEdit:focus, QComboBox:focus, QSpinBox:focus {{
    border: 1px solid #1F538D;
}}

/* 🔥 FIX: Dropdown Menu (The Popup List) 🔥 */
QComboBox QAbstractItemView {{
    background-color: {input_bg};
    border: 1px solid {border};
    selection-background-color: {selection_bg};
    selection-color: {selection_text};
    outline: none;
}}

/* Items inside the dropdown */
QComboBox QAbstractItemView::item {{
    padding: 8px;
    background-color: {input_bg};
    color: {text_main};
}}

QComboBox QAbstractItemView::item:hover {{
    background-color: {item_hover};
    color: {text_main};
}}

/* --- Settings Page --- */
QFrame#SettingsGroupFrame, QFrame#StatusCard {{
    background-color: {bg_sidebar};
    border: 1px solid {border};
    border-radius: 8px;
    padding: 15px;
}}

QLabel#SettingsSectionLabel {{
    color: {text_muted};
    font-size: 11px;
    text-transform: uppercase;
    font-weight: bold;
}}

QSpinBox#IntervalSpinBox, QLineEdit#DiscordInput {{
    color: #00FA9A;
    font-family: "Consolas", monospace;
}}

/* --- Scrollbars --- */
QScrollBar:vertical, QScrollBar:horizontal {{
    border: none;
    background: {bg_sidebar};
    width: 10px;
    height: 10px;
    margin: 0px;
}}

QScrollBar::handle:vertical, QScrollBar::handle:horizontal {{
    background: {border};
    border-radius: 5px;
}}

/* --- Scroll Area Fixes --- */
QScrollArea#SettingsScrollArea {{
    border: none;
    background-color: transparent;
}}

QWidget#SettingsContents {{
    background-color: {bg_main};
}}

QFrame#TradePanel {{
    background-color: {bg_card};
    border: 1px solid {border};
    border-radius: 8px;
}}

/* --- Connection Status --- */
QLabel#ConnectionStatusLabel[status="online"] {{ color: #00FA9A; font-weight: bold; }}
QLabel#ConnectionStatusLabel[status="offline"] {{ color: #FF5252; font-weight: bold; }}
"""