from filtering_manager import FilteringManager
import time
from threading import Timer

class TestFilteringManager(object):
    """
    This class was written only for testing the filtering manager module, pay attention
    to related notes in the documentation 
    """
    def __init__(self):
        pass

    def test_first_threshold(self):
        self.filtering_manager = FilteringManager()
        self.filtering_manager._first_threshold_timer.cancel()
        self.filtering_manager._second_threshold_timer.cancel()
        self.filtering_manager._first_threshold_timer = Timer(3, self.filtering_manager._first_threshold_timeout_reached)
        self.filtering_manager._second_threshold_timer = Timer(999999, self.filtering_manager._second_threshold_timeout_reached)
        for i in range(0,99):
            self.filtering_manager.update_request_received('127.0.0.0')
        assert(not self.filtering_manager.is_in_block_dict('127.0.0.0'))
        for i in range(0,2):
             self.filtering_manager.update_request_received('127.0.0.0')
        assert(self.filtering_manager.is_in_block_dict('127.0.0.0'))
        print(self.filtering_manager._block_dict)
        assert(self.filtering_manager.update_request_received('127.0.0.0') == False)
        self.filtering_manager._first_threshold_timer.cancel()
        self.filtering_manager._second_threshold_timer.cancel()
        return True

    def test_block_list(self):
        # change the MAXIMAL time in block list to 3 before this test
        self.filtering_manager = FilteringManager()
        self.filtering_manager._first_threshold_timer.cancel()
        self.filtering_manager._second_threshold_timer.cancel()
        self.filtering_manager._first_threshold_timer = Timer(3, self.filtering_manager._first_threshold_timeout_reached)
        self.filtering_manager._second_threshold_timer = Timer(999999, self.filtering_manager._second_threshold_timeout_reached)
        for i in range(0,99):
            self.filtering_manager.update_request_received('127.0.0.0')
        assert(not self.filtering_manager.is_in_block_dict('127.0.0.0'))
        for i in range(0,2):
             self.filtering_manager.update_request_received('127.0.0.0')
        assert(self.filtering_manager.is_in_block_dict('127.0.0.0'))
        time.sleep(5)
        assert(not self.filtering_manager.is_in_block_dict('127.0.0.0'))
        self.filtering_manager._first_threshold_timer.cancel()
        self.filtering_manager._second_threshold_timer.cancel()
        return True

    def multiple_ips(self):
        self.filtering_manager = FilteringManager()
        self.filtering_manager._first_threshold_timer.cancel()
        self.filtering_manager._second_threshold_timer.cancel()
        self.filtering_manager._first_threshold_timer = Timer(3, self.filtering_manager._first_threshold_timeout_reached)
        self.filtering_manager._second_threshold_timer = Timer(999999, self.filtering_manager._second_threshold_timeout_reached)
        self.filtering_manager.update_request_received('127.0.0.0')
        self.filtering_manager.update_request_received('1.1.1.1')
        self.filtering_manager.update_request_received('2.2.2.2')
        self.filtering_manager.update_request_received('3.3.3.3')
        print (self.filtering_manager._requests_counters_dict)


if __name__ == '__main__':
    test_filtering_manager_object = TestFilteringManager()
    test_filtering_manager_object.test_first_threshold()
    test_filtering_manager_object.test_block_list()
    test_filtering_manager_object.multiple_ips()