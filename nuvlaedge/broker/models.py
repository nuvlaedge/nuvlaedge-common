from datetime import datetime
from pydantic import BaseModel


class NuvlaEdgeMessage(BaseModel):
    sender: str
    data: dict
    time: datetime | None
