from abc import ABCMeta, abstractmethod
import logging
import operator
from typing import List

import numpy as np
from ljwtrader.datahandler import DataHandler
from .position import Position

logger = logging.getLogger(__name__)


class Strategy(metaclass=ABCMeta):
    """
    The Strategy is simply a collection of one or more condition-position groups. 
    Buy (Sell) or Sell (Buy) what, when x, y, & z are true/false?
    """

    id: str
    conditional_positions: List[Position]
    data_handler: DataHandler

    @abstractmethod
    def check_all(self):
        """Evaluate the status of each conditional position in strategy"""
        return NotImplementedError("Strategy must have a check_all() function")


class StrategySpec(Strategy):
    def __init__(self, conditional_positions: List[Position],
                 data_handler: DataHandler):

        self.conditional_positions = conditional_positions
        self.data_handler = data_handler

    def check_all(self):
        results = []
        for position in self.conditional_positions:
            calc_value = position(self.data_handler)
            results.append(calc_value)
            logger.debug(f'Ticker: {position.ticker} Check: {calc_value}')
