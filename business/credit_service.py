# business/credit_service.py

from typing import List
from datetime import datetime
from dataDB.credit_repo import CreditRepository
from models.credit import Credit

class CreditService:
    def __init__(self, credit_repository: CreditRepository):
        self.credit_repository = credit_repository

    def create_credit(self, credit: Credit) -> int:
        """
        Creates a new credit record in the database.
        Make sure the 'status' is either 'Activo' or 'Inactivo'.
        """
        # If you want extra validation:
        # if credit.status not in ("Activo", "Inactivo"):
        #     raise ValueError("El estado de crédito debe ser 'Activo' o 'Inactivo'.")
        return self.credit_repository.add_credit(credit)

    def get_credits_due_soon(self, days_in_advance: int = 7) -> List[Credit]:
        """
        Returns a list of credits that are 'Activo' and have a DueDate
        within the next 'days_in_advance' days.
        """
        credits = self.credit_repository.get_all_credits()
        near_due = []
        today = datetime.now()

        for c in credits:
            days_left = (c.due_date - today).days
            if c.status == "Activo" and days_left <= days_in_advance:
                near_due.append(c)
        return near_due

    def check_and_notify_due_credits(self) -> None:
        """
        Simple example method that prints (or could show a UI pop-up)
        any credits that are due soon.
        """
        soon_credits = self.get_credits_due_soon()
        for credit in soon_credits:
            print(f"El Crédito {credit.credit_id} vence pronto: {credit.due_date}")
