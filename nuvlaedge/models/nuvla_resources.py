"""
Contains the definitions and spec of Nuvla Resources
"""
from datetime import datetime
from  typing import List, Union, Dict

from pydantic import validator

from nuvlaedge.models import NuvlaEdgeBaseModel
from nuvlaedge.models.peripheral import PeripheralData


class NuvlaResourceBase(NuvlaEdgeBaseModel):
    """

    """
    # These entries are mandatory when the message is received from Nuvla. Cannot/Should not be created or edited
    # by the NuvlaEdge.
    # TODO: Maybe we can skip here the compulsory check of parameters to add flexibility to the model
    id: Union[str, None]
    resource_type: Union[str, None]
    created: Union[datetime, None]
    updated: Union[datetime, None]
    acl: Union[Dict, None]

    # Optional params in the common schema
    name: Union[str, None]
    description: Union[str, None]
    tags: Union[List[str], None]
    parent: Union[str, None]  # Nuvla ID format
    resource_metadata: Union[str, None]
    operations: Union[List, None]
    created_by: Union[str, None]
    updated_by: Union[str, None]


class NuvlaBoxAttributes(NuvlaEdgeBaseModel):
    version: int
    owner: Union[str, None]

    nuvlabox_status: Union[str, None]
    infrastructure_service_group: Union[str, None]
    credential_api_key: Union[str, None]
    host_level_management_api_key: Union[str, None]


class NuvlaBoxResource(NuvlaEdgeBaseModel):

    state: str
    refresh_interval: int
    
    location: Union[List, None]
    supplier: Union[str, None]
    organization: Union[str, None]
    manufacturer_serial_number: Union[str, None]
    firmware_version: Union[str, None]
    hardware_type: Union[str, None]
    form_factor: Union[str, None]
    wifi_ssid: Union[str, None]
    wifi_password: Union[str, None]
    root_password: Union[str, None]
    login_username: Union[str, None]
    login_password: Union[str, None]
    comment: Union[str, None]
    lan_cidr: Union[str, None]
    hw_revision_code: Union[str, None]
    monitored: Union[bool, None]
    vpn_server_id: Union[str, None]
    internal_data_gateway_endpoint: Union[str, None]
    ssh_keys: Union[List[str], None]
    capabilities: Union[List[str], None]
    online: Union[bool, None]
    inferred_location: Union[List[float], None]
    nuvlabox_engine_version: Union[str, None]

    @validator('*')
    def non_empty_str(cls, v):
        print(v)
        if isinstance(v, str):
            return v if v else None
        return v


class NuvlaBoxPeripheralResource(NuvlaResourceBase, PeripheralData):
    ...
