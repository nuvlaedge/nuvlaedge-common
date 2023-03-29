from __future__ import annotations
from typing import Protocol, Union, Dict

from nuvlaedge.models.messages import NuvlaEdgeMessage


class NuvlaEdgeBroker(Protocol):
    def consume(self, channel: str) -> list[NuvlaEdgeMessage]:
        ...

    def publish(self, channel: str, data: Union[Dict | NuvlaEdgeMessage], sender: str = '') -> bool:
        ...
