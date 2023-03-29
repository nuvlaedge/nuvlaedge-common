"""

"""
import json
import logging
from threading import Event

from nuvlaedge.broker import NuvlaEdgeBroker
from nuvlaedge.broker.file_broker import FileBroker
from nuvlaedge.common.constant_files import FILE_NAMES


class Peripheral:

    def __init__(self, name: str, scanning_interval: int = 30):
        self.logger: logging.Logger = logging.getLogger(name)
        # TODO: Temporal default debug level
        self.logger.setLevel(logging.DEBUG)

        self._name: str = name
        self._id: str = ''
        self._scanning_interval: int = scanning_interval

        self.broker: NuvlaEdgeBroker = FileBroker()
        self.last_hash: int = 0

    @staticmethod
    def hash_discoveries(devices: dict) -> int:
        return hash(json.dumps(devices, sort_keys=True))

    def run(self, run_peripheral: callable, **kwargs):
        """
        Runs the peripheral telemetry function
        :return:
        """
        e = Event()
        while True:
            self.logger.info('Discovering peripherals')
            discovered_peripherals: dict = run_peripheral(**kwargs)
            # Maybe we should always publish, regardless of the previous device and let the manager decide what to
            # do with the repetition
            self.logger.info(f'Discovered peripheral KEYS: {list(discovered_peripherals.keys())}')
            # if self.last_hash != self.hash_discoveries(discovered_peripherals) and discovered_peripherals:
            if discovered_peripherals:
                self.logger.info(f'New devices discovered in {self._name} peripheral:  {discovered_peripherals.keys()}')
                self.broker.publish(FILE_NAMES.PERIPHERALS_FOLDER.name + '/' + self._name,
                                    discovered_peripherals,
                                    self._name)
                # self.last_hash = self.hash_discoveries(discovered_peripherals)
            # else:
            #     self.logger.info(f'Nothing to do')

            e.wait(timeout=self._scanning_interval)
