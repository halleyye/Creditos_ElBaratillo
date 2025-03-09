# models/credit.py
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Credit:
    credit_id: int
    client_name: str
    monto: float
    start_date: datetime
    due_date: datetime
    status: str = "Activo"  # Default to "Activo"
    notes: str = ""
