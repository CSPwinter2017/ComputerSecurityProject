class SourceIpRecord(object):
    """
    This class represents a source IP record in the filtering mechanism (with the
    relevant counters for the thresholds).
    """

    def __init__(self, src_ip):
        self._src_ip = src_ip
        self._first_threshold = 0
        self._second_threshold = 0

    def increase_thresholds(self):
        """
        A DNS request was received from the relevant IP so we increase both thresholds
        """
        self._first_threshold += 1
        self._second_threshold += 1

    def initialize_first_threshold(self):
        """
        First timeout has exceeded, so it is considered the requests we received were not part
        of an attack.
        """
        self._first_threshold = 0

    def initialize_second_threshold(self):
        """
        Second timeout has exceeded, so it is considered the requests we received were not part
        of an attack.
        """
        self._second_threshold = 0

    def get_first_threshold(self):
        return self._first_threshold

    def get_second_threshold(self):
        return self._second_threshold
