import logging
import socket


logger = logging.getLogger(__name__)


class Client(object):
    """
    StatsD client dropping all metrics.
    """

    def incr(self, name, delta=1, tags=None):
        pass
