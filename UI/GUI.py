# ui/main_window.py

import sys
from PyQt6.QtWidgets import (
    QMainWindow, QApplication, QWidget, QVBoxLayout,
    QPushButton, QMessageBox
)
from business.credit_service import CreditService
from dataDB.credit_repo import CreditRepository
# from models.credit import Credit  # Only needed if you want to create credits here
# from datetime import datetime, timedelta

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Administración de Créditos")

        # Initialize repositories and services
        self.credit_repository = CreditRepository()
        self.credit_service = CreditService(self.credit_repository)

        # UI Layout
        main_widget = QWidget()
        layout = QVBoxLayout()

        self.btnCheckDue = QPushButton("Revisar Créditos Próximos a Vencer")
        self.btnCheckDue.clicked.connect(self.check_due_credits)
        layout.addWidget(self.btnCheckDue)

        # If you want to manually add a credit via a different form/dialog, implement that separately.
        # We remove the "Agregar Crédito (Ejemplo)" to avoid creating a sample credit automatically.

        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

    def check_due_credits(self):
        due_soon = self.credit_service.get_credits_due_soon(7)
        if not due_soon:
            QMessageBox.information(self, "Créditos", "No hay créditos que venzan en los próximos 7 días.")
        else:
            msg = "\n".join([f"Crédito {c.credit_id} vence el {c.due_date}" for c in due_soon])
            QMessageBox.warning(self, "Créditos Próximos a Vencer", msg)
