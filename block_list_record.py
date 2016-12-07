import datetime


class BlockListRecord(object):
    """
    This class represents a record in the blocking dictionary of IP addresses which were considered as
    IP addresses used for attacking (probably of potential victims).
    """

    def __init__(self, src_ip):
        self._src_ip = src_ip
        self._last_request_time = datetime.datetime.now()

    def update_request_received(self):
        """
        Updates the last time a DNS query was received from the relevant IP address.
        It is used in order to determine whether an attack was stopped and whether we should keep this IP
        in the blocking dictionary.
        """
        self._last_request_time = datetime.datetime.now()

    def get_last_request_time(self):
        return self._last_request_time


