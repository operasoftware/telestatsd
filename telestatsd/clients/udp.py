from functools import wraps
import logging
import random
import socket

from telestatsd.address_providers.inet import Provider as INETProvider


logger = logging.getLogger(__name__)


def sampled(method):
    @wraps(method)
    def inner(*args, **kwargs):
        rate = kwargs.pop('rate', None)

        if rate is not None and rate < 1:
            if random.random() > rate:
                return

            kwargs['rate_suffix'] = '|@{0}'.format(rate)

        return method(*args, **kwargs)

    return inner


class Client(object):
    """
    StatsD UDP client supporting tags (Telegraf's extension)
    """

    def __init__(self, address_provider=None, tags=None):
        """
        :param address_provider: socket.AF_INET addresses provider
        :type: object
        :param tags: tags to add to each metric
        :type: dict
        """
        if address_provider is None:
            address_provider = INETProvider()

        self._address_provider = address_provider
        self._tags = {} if tags is None else tags

    def send(self, payload):
        """
        :param payload: actual data to send
        :type: str
        """
        soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        address = self._address_provider.get()

        if address is None:
            logger.error('Address not provided',
                         extra={'address_provider': self._address_provider})
            return

        soc.sendto(payload, address)

    @sampled
    def incr(self, name, delta=1, tags=None, rate_suffix=''):
        """
        :param name:
        :type: str
        :param delta:
        :type: int
        :param tags:
        :type: dict
        :param rate_suffix:
        :type str
        """
        name = self._append_tags_to_name(name, tags)
        payload = '{0}:{1}|c{2}'.format(name, delta, rate_suffix)
        self.send(payload)

    def _append_tags_to_name(self, name, tags):
        """
        :param name: metric's name
        :type: str
        :param tags: tags to append
        :type: dict
        :rtype: str
        """
        merged_tags = self._tags.copy()

        if tags is not None:
            merged_tags.update(tags)

        serialized_tags = ','.join(['%s=%s' % (k, v) for k, v in
                                    merged_tags.iteritems()])

        if serialized_tags:
            return name + ',' + serialized_tags
        else:
            return name
