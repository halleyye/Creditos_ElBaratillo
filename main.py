# main.py

import sys
from PyQt6.QtWidgets import QApplication
from dataDB.db_connection import create_tables_if_not_exists
from UI.dashboard_window import DashboardWindow

def main():
    create_tables_if_not_exists()

    app = QApplication(sys.argv)
    window = DashboardWindow()
    window.showMaximized()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
