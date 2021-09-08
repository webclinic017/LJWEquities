from queue import Queue
import operator
from datetime import datetime
from typing import List, AnyStr

from .datahandler import DataHandler
from .eventhandler import EventHandler
from .strategy import Strategy

import logging

logging.basicConfig(
    filename='ljwtrader.log',
    level=logging.DEBUG,
    format="[%(module)s:%(lineno)3s]%(funcName)12s() -- %(message)s")
logger = logging.getLogger(__name__)


class TradingSystem:
    """
    Object that serves to govern the entire trading logic process. All user input should be 
    applied in this class, which acts as a unifier between all of the system components.
    """
    def __init__(self, start_date: datetime,
                 end_date: datetime, frequency: AnyStr, vendor: AnyStr, long: Sequence[tuple] = None, short: Sequence[tuple] = None):
        """Arguments supplied to the TradingSystem constructor by interface

        Args:
            symbols (List[AnyStr]): Collection of symbols that the system should track
            start_date (datetime): Beginning date of analysis       # ? This is backtest specific
            end_date (datetime): End date of analysis               # ? This is backtest specific
            frequency (str): Frequency of the bar data
            vendor (str): Data vendor to be used for the backtest   # ? This is backtest specific
        """
        self.symbols = []

        for _, indicator in long:
            self.symbols.append(indicator.args[0])

        if short is not None:
            for _, indicator in short:
                self.symbols.append(indicator.args[0])


        self.start_date = start_date
        self.end_date = end_date
        self.frequency = frequency
        self.vendor = vendor
        self._queue = Queue()

        logger.info(
            f"Symbols: {self.symbols}, Start Date: {self.start_date}, End Date: {self.end_date}, Frequency: {self.frequency}, Vendor: {self.vendor}"
        )

        self._event_handler = EventHandler(self._queue)

        self._data_handler = DataHandler(self.symbols, self._queue,
                                         self.start_date, self.end_date,
                                         self.frequency, self.vendor,
                                         self._event_handler.process_events)

        self._strategy = Strategy(self._queue, self._data_handler, long=long, short=short)
        self._event_handler.strategy = self._strategy

    def run_backtest(self):
        logger.info('Initiating backtest')
        self._data_handler.start_backtest()
