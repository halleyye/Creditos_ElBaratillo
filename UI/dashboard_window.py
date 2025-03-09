# ui/dashboard_window.py

import sys
from PyQt6.QtWidgets import (
    QMainWindow, QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTableWidget, QTableWidgetItem,
    QAbstractItemView, QMessageBox, QFrame
)
from PyQt6.QtCore import Qt, QTimer
from business.credit_service import CreditService
from dataDB.credit_repo import CreditRepository

from models.credit import Credit
from datetime import datetime

class DashboardWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simple Admin Dashboard")

        # Initialize repositories & services
        self.credit_repo = CreditRepository()
        self.credit_service = CreditService(self.credit_repo)

        # Main container widget
        container = QWidget()
        self.setCentralWidget(container)

        # Main horizontal layout (sidebar on the left, content on the right)
        main_layout = QHBoxLayout(container)

        # 1. SIDEBAR
        sidebar = self.create_sidebar()
        main_layout.addWidget(sidebar)

        # 2. DASHBOARD / CONTENT
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        main_layout.addWidget(self.content_widget, stretch=1)

        # In this example, we’ll have a top “cards” row and a bottom area
        self.create_top_cards()
        self.create_table_section()

        # 3. Start a timer or call a method to check due credits automatically
        #    (Optional) For instance, every minute:
        self.timer = QTimer(self)
        self.timer.setInterval(60_000)  # 60 seconds
        self.timer.timeout.connect(self.check_due_credits)
        self.timer.start()

        #refresh for top cards
        self.refresh_timer = QTimer(self)
        self.refresh_timer.setInterval(20_000)  # 20 seconds
        self.refresh_timer.timeout.connect(self.refresh_top_cards)
        self.refresh_timer.start()

        # Or call it once on startup:
        self.check_due_credits()

        # Load initial data
        self.load_credits_into_table()

    def create_sidebar(self) -> QWidget:
        """
        Creates a teal-like sidebar with simple navigation buttons.
        """
        sidebar = QWidget()
        sidebar.setStyleSheet("background-color: #292C2C;")  # approximate teal
        sidebar_layout = QVBoxLayout(sidebar)

        # Title / Logo
        title_label = QLabel("Simple Admin")
        title_label.setStyleSheet("font-size: 18px; color: white; font-weight: bold;")
        sidebar_layout.addWidget(title_label, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

        # Dashboard Button
        dashboard_btn = QPushButton("Dashboard")
        dashboard_btn.setStyleSheet("color: white;")
        dashboard_btn.clicked.connect(lambda: self.show_dashboard())
        sidebar_layout.addWidget(dashboard_btn)

        # Add more buttons (Forms, Data Table, etc.) if needed
        # e.g. forms_btn = QPushButton("Form")
        # etc.

        # Spacer
        sidebar_layout.addStretch()

        # Footer
        logout_btn = QPushButton("Cerrar Sesion")
        logout_btn.setStyleSheet("color: white;")
        # Connect to your logout or exit if you wish
        logout_btn.clicked.connect(self.close)
        sidebar_layout.addWidget(logout_btn, alignment=Qt.AlignmentFlag.AlignBottom)

        return sidebar

    def create_top_cards(self):
        """
        Creates a row of "cards" to show quick stats, like total credits, active credits, and near due dates.
        """
        # Store a reference to the cards container
        self.cards_container = QWidget()
        cards_layout = QHBoxLayout(self.cards_container)

        # Fetch data from the repository
        all_credits = self.credit_repo.get_all_credits()
        active_credits = [credit for credit in all_credits if credit.status == "Activo"]
        today = datetime.now()
        near_due_credits = [credit for credit in all_credits if (credit.due_date - today).days <= 30]

        # Card: Total Credits
        total_credits_card = self.create_info_card(str(len(all_credits)), "Creditos Totales")
        cards_layout.addWidget(total_credits_card)

        # Card: Active Credits
        active_credits_card = self.create_info_card(str(len(active_credits)), "Creditos Activos")
        cards_layout.addWidget(active_credits_card)

        # Card: Near Due Dates
        near_dates_card = self.create_info_card(str(len(near_due_credits)), "Fechas cercanas (menor a 1 mes)")
        cards_layout.addWidget(near_dates_card)

        # Add the cards container to the main layout
        self.content_layout.addWidget(self.cards_container)

    def refresh_top_cards(self):
        """
        Refreshes the data in the top cards without affecting the rest of the UI.
        """
        if not hasattr(self, 'cards_container'):
            return  # Ensure the cards container exists

        # Clear the existing cards
        for i in reversed(range(self.cards_container.layout().count())):
            widget = self.cards_container.layout().itemAt(i).widget()
            if widget:
                widget.deleteLater()

        # Fetch updated data from the repository
        all_credits = self.credit_repo.get_all_credits()
        active_credits = [credit for credit in all_credits if credit.status == "Activo"]
        today = datetime.now()
        near_due_credits = [credit for credit in all_credits if (credit.due_date - today).days <= 30]

        # Card: Total Credits
        total_credits_card = self.create_info_card(str(len(all_credits)), "Creditos Totales")
        self.cards_container.layout().addWidget(total_credits_card)

        # Card: Active Credits
        active_credits_card = self.create_info_card(str(len(active_credits)), "Creditos Activos")
        self.cards_container.layout().addWidget(active_credits_card)

        # Card: Near Due Dates
        near_dates_card = self.create_info_card(str(len(near_due_credits)), "Fechas cercanas (menor a 1 mes)")
        self.cards_container.layout().addWidget(near_dates_card)


    def create_info_card(self, main_text: str, sub_text: str) -> QWidget:
        """
        Helper to create a "card" with a main text and sub text.
        """
        card = QFrame()
        card.setFrameShape(QFrame.Shape.Box)
        card.setStyleSheet("background-color: #ADAAA8; border-radius: 5px;")

        layout = QVBoxLayout(card)
        main_label = QLabel(main_text)
        main_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        sub_label = QLabel(sub_text)

        layout.addWidget(main_label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(sub_label, alignment=Qt.AlignmentFlag.AlignCenter)
        return card

    def create_table_section(self):
        """
        Bottom section: Table of Credits + Buttons (Add, Update, Delete).
        """
        # Title
        table_title = QLabel("Creditos registrados")
        table_title.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.content_layout.addWidget(table_title)

        # Table
        self.credits_table = QTableWidget()
        self.credits_table.setColumnCount(7)
        self.credits_table.setHorizontalHeaderLabels(["Credit ID", "Nombre Cliente", "Monto", "Fecha Inicial",
                                                      "Fecha Final", "Estado", "Notas"])
        self.credits_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.credits_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.content_layout.addWidget(self.credits_table)

        # Buttons row
        buttons_container = QWidget()
        buttons_layout = QHBoxLayout(buttons_container)

        add_btn = QPushButton("Añadir Credito")
        add_btn.clicked.connect(self.add_credit_dialog)
        buttons_layout.addWidget(add_btn)

        update_btn = QPushButton("Actualizar Credito")
        update_btn.clicked.connect(self.update_credit_dialog)
        buttons_layout.addWidget(update_btn)

        delete_btn = QPushButton("Eliminar Credito")
        delete_btn.clicked.connect(self.delete_credit)
        buttons_layout.addWidget(delete_btn)

        self.content_layout.addWidget(buttons_container)

    def load_credits_into_table(self):
        """
        Loads all credits from DB into the QTableWidget.
        """
        credits = self.credit_repo.get_all_credits()
        self.credits_table.setRowCount(len(credits))

        for row_idx, c in enumerate(credits):
            self.credits_table.setItem(row_idx, 0, QTableWidgetItem(str(c.credit_id)))
            self.credits_table.setItem(row_idx, 1, QTableWidgetItem(str(c.client_name)))
            self.credits_table.setItem(row_idx, 2, QTableWidgetItem(str(c.monto)))
            self.credits_table.setItem(row_idx, 3, QTableWidgetItem(c.start_date.isoformat()))
            self.credits_table.setItem(row_idx, 4, QTableWidgetItem(c.due_date.isoformat()))
            self.credits_table.setItem(row_idx, 5, QTableWidgetItem(c.status))

    def show_dashboard(self):
        # If you had multiple pages in a QStackedWidget, you’d switch to the Dashboard index
        # For now, everything is just one layout, so this is a placeholder.
        pass

    def check_due_credits(self):
        """
        Called by timer or manually, shows a pop-up if any 'Activo' credits
        are due soon (within 7 days).
        """
        near_due = self.credit_service.get_credits_due_soon(7)
        if near_due:
            msg_text = "\n".join([f"Crédito {c.credit_id} vence el {c.due_date}" for c in near_due])
            QMessageBox.warning(self, "Créditos Próximos a Vencer", msg_text)

    # -----------------------------
    #  ADD / UPDATE / DELETE Logic
    # -----------------------------

    def add_credit_dialog(self):
        """
        Open a dialog to enter data for a new credit.
        """
        from .credit_form_dialog import CreditFormDialog
        dlg = CreditFormDialog(parent=self)
        if dlg.exec():
            # If the user clicked "Save"
            new_credit = dlg.get_credit_data()
            self.credit_service.create_credit(new_credit)
            self.load_credits_into_table()
            self.refresh_top_cards()  # Refresh the top cards

    def update_credit_dialog(self):
        """
        Updates an existing credit.
        """
        row = self.credits_table.currentRow()
        if row < 0:
            QMessageBox.information(self, "Actualizar credito", "Por favor, seleccione un credito a actualizar.")
            return

        credit_id = int(self.credits_table.item(row, 0).text())
        existing_credit = self.credit_repo.get_credit_by_id(credit_id)
        if not existing_credit:
            QMessageBox.warning(self, "Actualizar credito", "El credito seleccionado no existe en la base de datos.")
            return

        from .credit_form_dialog import CreditFormDialog
        dlg = CreditFormDialog(parent=self, credit=existing_credit)
        if dlg.exec():
            updated_credit = dlg.get_credit_data()
            updated_credit.credit_id = credit_id  # Ensure ID remains the same
            self.credit_repo.update_credit(updated_credit)
            self.load_credits_into_table()
            self.refresh_top_cards()  # Refresh the top cards

    def delete_credit(self):
        """
        Delete the selected credit from the DB.
        """
        row = self.credits_table.currentRow()
        if row < 0:
            QMessageBox.information(self, "Eliminar credito", "Por favor, seleccione un credito a eliminar.")
            return

        credit_id = int(self.credits_table.item(row, 0).text())
        confirm = QMessageBox.question(self, "Confirmar eliminacion",
                                       f"Esta seguro de eliminar el credito {credit_id}?")
        if confirm == QMessageBox.StandardButton.Yes:
            self.credit_repo.delete_credit(credit_id)
            self.load_credits_into_table()
            self.refresh_top_cards()  # Refresh the top cards
