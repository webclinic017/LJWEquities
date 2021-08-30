from queue import Queue

from .datahandler import DataHandler
from .eventhandler import EventHandler

import logging
logging.basicConfig(filename='ljwtrader.log')
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

        self._data_handler = DataHandler(
            self._queue,
            self.start_date,
            self.end_date,
            self.frequency,
            self.vendor
            )

        self._event_handler = EventHandler(
            self._queue,
            self._data_handler
            )

    def run_backtest(self):
        self._event_handler.run_backtest()
    
    def get_start_date(self):
        return self.start_date

    def get_end_date(self):
        return self.end_date

    def get_frequency(self):
        return self.frequency

    def get_vendor(self):
        return self.vendor