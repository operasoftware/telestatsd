from telestatsd.clients.udp import Client as UDPClient

import logging


class Client(UDPClient):
    """
    StatsD client sending everything to logger.
    """

    def __init__(self, logger=None, tags=None):
        """
        :param logger:
        :type: logging.Logger
        :param tags: tags to add to each metric
        :type: dict
        """
        super(Client, self).__init__(address_provider=None, tags=tags)

        if logger is None:
            logger = logging.getLogger('telestatsd.clients.logger')

        self._logger = logger

    def send(self, payload):
        """
        :param payload: actual data to send
        :type: str
        """
        self._logger.info(payload)
