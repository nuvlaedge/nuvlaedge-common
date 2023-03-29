from __future__ import annotations
from typing import Union

from pydantic import validator

from nuvlaedge.models import NuvlaEdgeBaseModel


class PeripheralData(NuvlaEdgeBaseModel):
    identifier: str
    available: bool
    classes: list

    device_path: Union[str, None]
    port: Union[int, None]
    interface: Union[str, None]
    product: Union[str, None]
    version: Union[int, None]
    additional_assets: Union[dict, None]
    vendor: Union[str, None]
    product: Union[str, None]
    local_data_gateway_endpoint: Union[str, None]
    raw_data_sample: Union[str, None]
    data_gateway_enabled: Union[bool, None]
    serial_number: Union[str, None]
    video_device: Union[str, None]
    resources: Union[list, None]

    @validator('device_path', 'vendor', 'raw_data_sample', 'serial_number', 'video_device')
    def validate_device_path(cls, v):
        if isinstance(v, str) and not v:
            raise ValueError('Cannot be an empty string')
        return v
