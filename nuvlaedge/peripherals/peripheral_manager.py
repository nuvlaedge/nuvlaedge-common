"""

"""
import json
import logging
import time
from pathlib import Path
from threading import Event, Thread

import filelock
from nuvla.api import Api as NuvlaClient
from nuvla.api.models import CimiCollection, CimiResponse, CimiResource

from nuvlaedge.constant_files import FILE_NAMES
from nuvlaedge.constants import PERIPHERAL_RESOURCE_NAME
from nuvlaedge.broker import NuvlaEdgeBroker
from nuvlaedge.broker.models import NuvlaEdgeMessage


class PeripheralManager(Thread):
    REFRESH_RATE = 30  # Peripheral refresh rate in seconds
    # Normally, NuvlaDB and local DB shouldn't be desynchronized. For safety, we check Nuvla db and synchronize the
    # local one with it for safe keeping
    NUVLA_SYNCHRONIZATION_PERIOD = 4*REFRESH_RATE

    PERIPHERALS_LOCATION: Path = FILE_NAMES.PERIPHERALS_FOLDER

    def __init__(self, persistence, broker: NuvlaEdgeBroker, nuvla_client, nuvlaedge_uuid: str):
        super(PeripheralManager, self).__init__(daemon=True)
        self.logger: logging.Logger = logging.getLogger(self.__class__.__name__)

        self._uuid: str = nuvlaedge_uuid

        self.persistence = persistence
        self.broker: NuvlaEdgeBroker = broker
        self.nuvla_client: NuvlaClient = nuvla_client

        self.exit_event: Event = Event()

        self.running_peripherals: set = set()

        # This variable is updated either from the local registry or from Nuvla database
        self.nuvla_registered_devices: dict = {}
        self.local_registry_path: Path = FILE_NAMES.PERIPHERALS_FOLDER / 'local_registry.json'

    def get_nuvla_registered_peripherals(self):
        """

        :return:
        """
        nuvla_peripherals: CimiCollection = self.nuvla_client.search('nuvlabox-peripheral',
                                                                     filter=f'parent="{self._uuid}"')
        self.nuvla_registered_devices = {dev.data['identifier']: dev.data for dev in nuvla_peripherals.resources}

    def update_local_registry(self, devices: dict, add: set, delete: set, update: set):
        """

        :param devices:
        :param add:
        :param delete:
        :param update:
        :return:
        """
        local_devices: dict = {}
        peripherals_registered_file: Path = FILE_NAMES.PERIPHERALS_FOLDER / 'local_registry.json'

        with peripherals_registered_file.open('a') as file:
            local_devices = json.load(file)
            local_ids: set = set(local_devices.keys())
            new_ids: set = set(devices.keys())
            for i in new_ids - local_ids:
                local_devices[devices.get(i).get('identifier')] = devices.get(i)

            json.dump(local_devices, file)

    def get_local_registry(self) -> dict:
        """
        Reads the local registry file. This exists to reduce as much as possible communication with Nuvla
        :return:
        """
        if not self.local_registry_path.exists() or self.local_registry_path.stat().st_size == 0:
            return {}

        with self.local_registry_path.open('r') as file:
            return json.load(file)

    def delete_nuvla_peripherals(self, device_list: list[dict]):
        """
        Receives a list of peripherals whose id's are to be removed because they are no longer found in the current
        NuvlaEdge
        :param device_list:
        :return:
        """

        for device in device_list:
            if 'id' in device:
                response: CimiResponse = self.nuvla_client.delete(device['id'])
                # if response.data.get('status'):
                print(response.data.get('status'))

    def edit_nuvla_peripherals(self, device_list: list[dict]):
        """

        :param device_list:
        :return:
        """

        for dev in device_list:
            response: CimiResponse = self.nuvla_client.edit(dev['id'], dev)
            self.logger.info(f'Status response for editing {dev["id"]}: {response.data.get("status")}')

    def add_nuvla_peripheral(self, device_list: list):
        """
        Receives a list of peripherals whose id's are to be added
        :param device_list:
        :return:
        """
        for dev in device_list:
            if 'identifier' not in dev:
                self.logger.info(f'Trying to add an uncompleted peripheral device: {json.dumps(dev, indent=4)}')
                continue

            self.nuvla_client.add(PERIPHERAL_RESOURCE_NAME, dev)

    def resolve_peripheral_devices(self, new_devices: list[NuvlaEdgeMessage]):
        """
        Receives a list of messages and process them sequentially performing the corresponding actions against nuvla
        :param new_devices:
        :return:
        """
        latest_devices = sorted(new_devices, key=lambda x: x.time)[0].data
        latest_devs_keys = set(latest_devices.keys())
        current_devs = set(self.nuvla_registered_devices.keys())

        self.add_nuvla_peripheral([latest_devices.get(i) for i in latest_devs_keys - current_devs])
        self.delete_nuvla_peripherals([latest_devices.get(i) for i in current_devs - latest_devs_keys])
        self.edit_nuvla_peripherals([latest_devices.get(i) for i in latest_devs_keys & current_devs])

    def run(self) -> None:
        self.logger.info(f'Starting peripheral manager thread')

        while not self.exit_event.is_set():
            # In the original implementation, every iteration required for every new device to contact Nuvla
            self.get_nuvla_registered_peripherals()

            for peripheral in self.running_peripherals:
                self.logger.info(f'Reading new devices from {self.PERIPHERALS_LOCATION.name}/{peripheral}')

                new_devs = self.broker.consume(f'{self.PERIPHERALS_LOCATION.name}/{peripheral}')
                if not new_devs:
                    continue

                self.resolve_peripheral_devices(new_devs)

                self.logger.debug(f'New devices {new_devs}')

            self.exit_event.wait(self.REFRESH_RATE)

        self.logger.debug('Ended peripheral manager loop')

    def join(self, timeout: float | None = ...) -> None:
        self.logger.info(f'Exiting peripheral manager thread')
        self.exit_event.set()
        super().join()

