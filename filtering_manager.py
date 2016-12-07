from source_ip_record import SourceIpRecord
from threading import Timer
from block_list_record import BlockListRecord
import datetime


class FilteringManager(object):
    """
    This class is responsible for filtering DNS requests and make sure to stop any requests
    in case of an attack.
    """

    FIRST_THRESHOLD_IN_SEC = 600  # 10 minutes
    SECOND_THRESHOLD_IN_SEC = 3600  # 1 hour

    MAXIMAL_REQUESTS_FIRST_THRESHOLD = 100  # 100 requests per 10 minutes
    MAXIMAL_REQUESTS_SECOND_THRESHOLD = 1000  # 1000 requests per 1 hour

    MAXIMAL_TIME_IN_BLOCK_LIST = 3600  # 1 hour is the timeout in the block list

    def __init__(self):
        self._requests_counters_dict = {}
        self._block_dict = {}
        self._first_threshold_timer = Timer(self.FIRST_THRESHOLD_IN_SEC, self._first_threshold_timeout_reached)
        self._second_threshold_timer = Timer(self.SECOND_THRESHOLD_IN_SEC, self._second_threshold_timeout_reached)
        self._first_threshold_timer.start()
        self._second_threshold_timer.start()

    def update_request_received(self, src_ip):
        """
        :param src_ip: A string representing the source IP in the DNS request query which was received.
        :return: True in case we should forward the request to the actual DNS server (which is means it is still not
        considered as an attack). Otherwise (in case it is considered as an attack), it would return False.
        """
        if self.is_in_block_dict(src_ip):
            return False
        if src_ip in self._requests_counters_dict.keys():
            return self._update_src_ip_record(src_ip)
        else:
            return self._initialize_src_ip_record(src_ip)

    def _update_src_ip_record(self, src_ip):
        """
        :param src_ip: A string representing the source IP in the DNS request query which was received.
        :return: True in case we should forward the request to the actual DNS server (which is means it is still not
        considered as an attack). Otherwise (in case it is considered as an attack), it would return False.
        This method updates the source IP record of an already existing record.
        """
        self._requests_counters_dict[src_ip].increase_thresholds()
        if self.does_threshold_reached(self._requests_counters_dict[src_ip]):
            self._block_dict[src_ip] = BlockListRecord(src_ip)
            del self._requests_counters_dict[src_ip]
            return False
        return True

    def _initialize_src_ip_record(self, src_ip):
        """
        :param src_ip: A string representing the source IP in the DNS request query which was received.
        :return: This method will always return True since it is the first time a request was recieved from
        the given IP address, hence it is still not considered as an attack.
        """
        self._requests_counters_dict[src_ip] = SourceIpRecord(src_ip)
        return True

    def _first_threshold_timeout_reached(self):
        """
        This method initializes the first threshold for all existing source IP address records.
        This is since we reached this timeout so we assume the requests which were recieved are not
        part of an attack.
        """
        for src_ip in self._requests_counters_dict.keys():
            self._requests_counters_dict[src_ip].initialize_first_threshold()
        self._first_threshold_timer = Timer(self.FIRST_THRESHOLD_IN_SEC, self._first_threshold_timeout_reached)
        self._first_threshold_timer.start()

    def _second_threshold_timeout_reached(self):
        """
        This method initializes the second threshold for all existing source IP address records.
        This is since we reached this timeout so we assume the requests which were recieved are not
        part of an attack.
        """
        for src_ip in self._requests_counters_dict.keys():
            self._requests_counters_dict[src_ip].initialize_second_threshold()
        self._second_threshold_timer = Timer(self.SECOND_THRESHOLD_IN_SEC, self._second_threshold_timeout_reached)
        self._second_threshold_timer.start()

    def does_threshold_reached(self, src_ip_record):
        """
        :param src_ip_record: A SourceIpRecord object.
        :return: True in case we reached any of the thresholds (the first one or the second one).
        Otherwise it would return False.
        """
        if src_ip_record.get_first_threshold() >= self.MAXIMAL_REQUESTS_FIRST_THRESHOLD:
            return True
        if src_ip_record.get_second_threshold() >= self.MAXIMAL_REQUESTS_SECOND_THRESHOLD:
            return True
        else:
            return False

    def is_in_block_dict(self, src_ip):
        """
        :param src_ip: A string representing the source IP in the DNS request query which was received.
        :return: True in case the given source IP address is in the block list (for trying to attack).
        Otherise it would return False.
        """
        if src_ip in self._block_dict.keys():
            last_request_time = self._block_dict[src_ip].get_last_request_time()
            current_time = datetime.datetime.now()
            time_delta = current_time-last_request_time
            if time_delta.seconds > self.MAXIMAL_TIME_IN_BLOCK_LIST:
                del self._block_dict[src_ip]
                return False
            else:
                self._block_dict[src_ip].update_request_received()
                return True
        return False


