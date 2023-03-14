"""

"""
from datetime import datetime
from pydantic import BaseModel


class NuvlaPeripheral(BaseModel):
    available: bool
    classes: list
    device_path: str
    identifier: str
    interface: str
    product: str
    version: int


class PeripheralMessage(BaseModel):
    data: NuvlaPeripheral
    delete: bool
    time: datetime
