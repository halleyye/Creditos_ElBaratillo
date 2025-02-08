# models/client.py
from dataclasses import dataclass

@dataclass
class Client:
    client_id: int
    first_name: str
    last_name: str
    phone: str = ""
