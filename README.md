Apit212 🚀

Apit212 is a modern, Playwright-based Python wrapper for the Trading 212 platform. Since the official API currently lacks support for CFD trade execution, this library fills the gap by enabling automated trading, data scraping, and custom bot development via browser automation.

    [!WARNING]

    Disclaimer: This project is not affiliated with, maintained, or endorsed by Trading 212. Use this API at your own risk. The developers are not responsible for any financial losses or account actions resulting from the use of this software.

✨ Features

    CFD Support: Execute trades where the official API cannot.

    Playwright Powered: Robust browser automation that handles modern web updates.

    Multiple Interfaces: Support for CLI, TUI, and GUI interactions.

    Data Scraping: Easily extract real-time market data for analysis.

🛠 Installation

Install the package via pip:
Bash

pip install apit212

Because this library uses Playwright, you will also need to install the browser binaries:
Bash

playwright install chromium

🚀 Quick Start

To begin using the API, initialize the core and log in to your account. You can then use the built-in functions to build your own trading logic.
Python

from apit212 import Apit212

# Initialize and Login
api = Apit212()
api.login(username="your_email", password="your_password")

# Example: Fetch market data
data = api.get_market_data("VUSA")
print(data)

📂 Project Structure

This project follows a modular "Source Layout" to keep the core logic separate from the user interfaces:

    core/: The main API logic and Playwright controllers.

    gui/: Graphical interface for visual monitoring.

    tui/: Lightweight terminal-based interface.

    main.py: The central entry point for the application.

📋 Requirements

    Python 3.8+

    Playwright

    Requests

🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the issues page.
