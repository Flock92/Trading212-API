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
    else:
        # Default Dark Theme
        bg_main = "#121212"
        bg_sidebar = "#1A1A1A"
        bg_card = "#1E1E1E"
        text_main = "#E2E2E2"
        text_muted = "#AAAAAA"  # Brightened from #888888 for better contrast
        border = "#333333"
        input_bg = "#252525"
        selection_bg = "#2A5C91"
        selection_text = "#FFFFFF"

    return f"""
/* --- Global Settings --- */
QMainWindow,
QWidget#CentralWidget,
QWidget#LoginView,
QWidget#DashboardView,
QWidget#PortfolioView,
QWidget#SettingsView,
QWidget#OrdersView {{
    background-color: {bg_main};
    color: {text_main};
    font-family: "Segoe UI", "Roboto", "Arial";
    font-size: 14px;
}}

QLabel, QCheckBox, QRadioButton {{
    background-color: transparent;
    color: {text_main};
}}

/* --- Sidebar Styling --- */
QFrame#Sidebar {{
    background-color: {bg_sidebar};
    border-right: 1px solid {border};
}}

QLabel#SidebarLogo {{
    color: {text_main};
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
    color: {text_main};
}}

QPushButton#CloseOrderBtn {{
    background-color: #332222;
    color: #FF5252;
    border: 1px solid #553333;
    font-size: 11px;
}}

QPushButton#CloseOrderBtn:hover {{
    background-color: #FF5252;
    color: white;
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
    color: {text_main};
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
    color: {text_main};
}}

QHeaderView::section {{
    background-color: {input_bg};
    color: {text_main}; /* Changed from text_muted to main for visibility */
    padding: 8px;
    border: none;
    border-bottom: 2px solid {border};
}}

/* --- Inputs --- */
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
    background: {bg_sidebar}; /* Slightly offset from main bg */
    width: 10px;
    height: 10px;
    margin: 0px;
}}

QScrollBar::handle:vertical, QScrollBar::handle:horizontal {{
    background: {border};
    border-radius: 5px;
    min-height: 20px;
}}

QScrollBar::handle:vertical:hover, QScrollBar::handle:horizontal:hover {{
    background: #1F538D; /* Primary color on hover */
}}

/* --- Settings Page Specifics (The Fix) --- */
QScrollArea#SettingsScrollArea {{
    border: none;
    background-color: transparent;
}}

/* This targets the internal container of the scroll area */
QScrollArea#SettingsScrollArea > QWidget > QWidget {{
    background-color: transparent;
}}

/* This ensures the viewport doesn't default to white */
QScrollArea#SettingsScrollArea QWidget#qt_scrollarea_viewport {{
    background-color: transparent;
}}

/* The container inside the scroll area often needs an explicit background if transparent fails */
QWidget#SettingsContents {{
    background-color: {bg_main};
}}

QFrame#SettingsGroupFrame, QFrame#StatusCard {{
    background-color: {bg_sidebar};
    border: 1px solid {border};
    border-radius: 8px;
    padding: 15px;
    margin-bottom: 10px;
}}

QFrame#TradePanel {{
        background - color: {bg_card};
    border: 1px solid {border};
    border-radius: 8px;
}}

QPushButton#CloseOrderBtn {{
    margin: 2px 5px;
    padding: 4px;
}}

/* --- Connection Status --- */
QLabel#ConnectionStatusLabel[status="online"] {{ color: #00FA9A; font-weight: bold; }}
QLabel#ConnectionStatusLabel[status="offline"] {{ color: #FF5252; font-weight: bold; }}
"""
