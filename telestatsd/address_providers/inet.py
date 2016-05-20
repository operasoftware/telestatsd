class Provider(object):
    """
    socket.AF_INET addresses provider.
    """

    def __init__(self, host, port):
        """
        :param host:
        :type: str
        :param port:
        :type: int
        """
        self._host = host
        self._port = port

    def get(self):
        """
        :rtype: tuple
        """
        return (self._host, self._port)
