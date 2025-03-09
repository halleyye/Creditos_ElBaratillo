# dataDB/credit_repo.py

from typing import List, Optional
from datetime import datetime
from models.credit import Credit
from .db_connection import get_db_connection

class CreditRepository:

    def get_credit_by_id(self, credit_id: int) -> Optional[Credit]:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            SELECT CreditId, ClientName, Monto, StartDate, DueDate, Status, Notes
            FROM Credits
            WHERE CreditId = ?
        """
        cursor.execute(query, (credit_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()

        if row:
            return Credit(
                credit_id=row["CreditId"],
                client_name=row["ClientName"],
                monto=float(row["Monto"]),
                start_date=datetime.fromisoformat(row["StartDate"]),
                due_date=datetime.fromisoformat(row["DueDate"]),
                status=row["Status"],
                notes=row["Notes"]
            )
        return None

    def get_all_credits(self) -> List[Credit]:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            SELECT CreditId, ClientName, Monto, StartDate, DueDate, Status, Notes
            FROM Credits
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        credits = []
        for row in rows:
            credits.append(Credit(
                credit_id=row["CreditId"],
                client_name=row["ClientName"],
                monto=float(row["Monto"]),
                start_date=datetime.fromisoformat(row["StartDate"]),
                due_date=datetime.fromisoformat(row["DueDate"]),
                status=row["Status"],
                notes=row["Notes"]
            ))
        return credits

    def add_credit(self, credit: Credit) -> int:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO Credits (ClientName, Monto, StartDate, DueDate, Status, Notes)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        cursor.execute(query, (
            credit.client_name,
            credit.monto,
            credit.start_date.isoformat(),
            credit.due_date.isoformat(),
            credit.status,
            credit.notes
        ))
        conn.commit()
        new_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return new_id

    def update_credit(self, credit: Credit) -> None:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            UPDATE Credits
            SET 
                ClientName = ?, 
                Monto = ?, 
                StartDate = ?, 
                DueDate = ?, 
                Status = ?, 
                Notes = ?
            WHERE CreditId = ?
        """
        cursor.execute(query, (
            credit.client_name,
            credit.monto,
            credit.start_date.isoformat(),
            credit.due_date.isoformat(),
            credit.status,
            credit.notes,
            credit.credit_id
        ))
        conn.commit()
        cursor.close()
        conn.close()

    def delete_credit(self, credit_id: int) -> None:
        """
        Deletes a credit from the database by its ID.
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            DELETE FROM Credits
            WHERE CreditId = ?
        """
        cursor.execute(query, (credit_id,))
        conn.commit()
        cursor.close()
        conn.close()
