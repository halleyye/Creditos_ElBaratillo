# ui/credit_form_dialog.py

from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox
from PyQt6.QtCore import QDateTime
from models.credit import Credit
from datetime import datetime

class CreditFormDialog(QDialog):
    def __init__(self, parent=None, credit=None):
        super().__init__(parent)
        self.setWindowTitle("Credit Form")
        self.setModal(True)

        self.resize(400,300)

        self.edit_mode = credit is not None
        self.credit = credit

        layout = QVBoxLayout(self)

        # Client name
        layout.addWidget(QLabel("Nombre Cliente:"))
        self.client_name_edit = QLineEdit()
        layout.addWidget(self.client_name_edit)

        # Monto
        layout.addWidget(QLabel("Monto:"))
        self.monto_edit = QLineEdit()
        layout.addWidget(self.monto_edit)

        # Start Date
        layout.addWidget(QLabel("Fecha Inicial (AAAA-MM-DD):"))
        self.start_date_edit = QLineEdit()
        layout.addWidget(self.start_date_edit)

        # Due Date
        layout.addWidget(QLabel("Fecha Final (AAAA-MM-DD):"))
        self.due_date_edit = QLineEdit()
        layout.addWidget(self.due_date_edit)

        # Status
        layout.addWidget(QLabel("Estado:"))
        self.status_combo = QComboBox()
        self.status_combo.addItems(["Activo", "Inactivo"])  # only 2 statuses
        layout.addWidget(self.status_combo)

        # Notes
        layout.addWidget(QLabel("Notas:"))
        self.notes_edit = QLineEdit()
        layout.addWidget(self.notes_edit)

        # Buttons
        btn_layout = QHBoxLayout()
        save_btn = QPushButton("Guardar")
        save_btn.clicked.connect(self.save_and_close)
        cancel_btn = QPushButton("Cancelar")
        cancel_btn.clicked.connect(self.reject)

        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)

        if self.edit_mode:
            self.populate_fields()

    def populate_fields(self):
        """
        If editing an existing credit, fill the fields from the given credit object.
        """
        if not self.credit:
            return
        self.client_name_edit.setText(str(self.credit.client_name))
        self.monto_edit.setText(str(self.credit.monto))
        self.start_date_edit.setText(self.credit.start_date.strftime("%Y-%m-%d"))
        self.due_date_edit.setText(self.credit.due_date.strftime("%Y-%m-%d"))
        self.status_combo.setCurrentText(self.credit.status)
        self.notes_edit.setText(self.credit.notes)

    def save_and_close(self):
        # Basic validation
        try:
            client_name = str(self.client_name_edit.text().strip())
            monto = float(self.monto_edit.text().strip())
            start_date = datetime.strptime(self.start_date_edit.text().strip(), "%Y-%m-%d")
            due_date = datetime.strptime(self.due_date_edit.text().strip(), "%Y-%m-%d")
            status = self.status_combo.currentText()
            notes = self.notes_edit.text().strip()
        except ValueError as e:
            # Could show a message box that there's invalid input
            self.reject()
            return

        # Construct a new Credit object (or updated one)
        self.credit = Credit(
            credit_id=0 if not self.edit_mode else self.credit.credit_id,
            client_name=client_name,
            monto=monto,
            start_date=start_date,
            due_date=due_date,
            status=status,
            notes=notes
        )

        self.accept()

    def get_credit_data(self) -> Credit:
        """
        Returns the credit object with updated data after user hits "Save."
        """
        return self.credit
