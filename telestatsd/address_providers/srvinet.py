from datetime import datetime, timedelta
import logging

import srvlookup


logger = logging.getLogger(__name__)


class Provider(object):
    """
    socket.AF_INET addresses provider based on SRV records
    https://en.wikipedia.org/wiki/SRV_record
    """

    PROTO_TCP = 'TCP'
    PROTO_UDP = 'UDP'

    def __init__(self, service, domain, protocol=None, refresh_delta=None):
        """
        :param service:
        :type: str
        :param domain:
        :type: str
        :param protocol: PROTO_TCP or PROTO_UDP
        :type: str
        :param refresh_delta: interval between refreshing SRV record by
                              talking to DNS server.
        :type: datetime.timedelta
        """
        self._service = service
        self._domain = domain
        self._protocol = self.PROTO_UDP if protocol is None else protocol
        self._refresh_delta = (timedelta(minutes=1) if refresh_delta is None
                               else refresh_delta)
        self._last_refresh_at = datetime.fromtimestamp(0)
        self._addr = None

    def _refresh_addr(self):
        """
        Gets current list of SRV records from DNS server and use the first one.

        TODO: Check if we can assume that server returns records in random order.
        """
        try:
            srvs = srvlookup.lookup(self._service, self._protocol,
                                    self._domain)
        except srvlookup.SRVQueryFailure:
            logger.debug('SRV query failed')
            return

        assert len(srvs) > 0
        srv = srvs[0]
        self._addr = (srv.host, srv.port)
        self._last_refresh_at = datetime.now()

    def get(self):
        """
        :rtype: tuple or None
        """
        if (datetime.now() - self._last_refresh_at) > self._refresh_delta:
            self._refresh_addr()

        return self._addr
