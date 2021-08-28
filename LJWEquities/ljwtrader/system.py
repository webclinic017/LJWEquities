from queue import Queue

import logging
logger = logging.getLogger(__name__)


class TradingSystem:
    """
    Object that serves to govern the entire trading logic process

    All user input should be applied in this class, which acts as a unifier between all of the system components.
    The TradingSystem pushes data from the Data handler to the Event handler.
    """
    def __init__(self, start_date, end_date, frequency, vendor):    

        self.start_date = start_date
        self.end_date = end_date
        self.frequency = frequency
        self.vendor = vendor
        self._queue = Queue()

        logger.info(f"Start Date: {self.start_date}, End Date: {self.end_date}, Frequency: {self.frequency}, Vendor {self.vendor}")
