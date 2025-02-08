# data/client_repository.py
from typing import List, Optional
from models.client import Client
from .SQL_connect import get_db_connection

class ClientRepository:

    def get_client_by_id(self, client_id: int) -> Optional[Client]:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            SELECT ClientId, FirstName, LastName, Phone
            FROM Clients
            WHERE ClientId = ?
        """
        cursor.execute(query, (client_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()

        if row:
            return Client(
                client_id=row["ClientId"],
                first_name=row["FirstName"],
                last_name=row["LastName"],
                phone=row["Phone"]
            )
        return None

    def get_all_clients(self) -> List[Client]:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            SELECT ClientId, FirstName, LastName, Phone
            FROM Clients
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        clients = []
        for row in rows:
            clients.append(Client(
                client_id=row["ClientId"],
                first_name=row["FirstName"],
                last_name=row["LastName"],
                phone=row["Phone"]
            ))
        return clients

    def add_client(self, client: Client) -> int:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO Clients (FirstName, LastName, Phone)
            VALUES (?, ?, ?)
        """
        cursor.execute(query, (
            client.first_name,
            client.last_name,
            client.phone
        ))
        conn.commit()
        new_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return new_id

    # Métodos update_client, delete_client, etc. si los necesitas...
