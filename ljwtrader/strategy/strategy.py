import logging
from typing import Any, Callable, List, Sequence

from ljwtrader.data import DataHandler
from ljwtrader.events import Event, MarketEvent, StrategyEvent

logger = logging.getLogger(__name__)


class Strategy:

    # TODO: Properly document

    def __init__(self,
                 queue: Sequence[Event],
                 data_handler: DataHandler,
                 long=None,
                 short=None):
        self.queue = queue
        self.data_handler = data_handler
        self.directions = {}
        self.positions = {'long': {}, 'short': {}}

    def add_indicator_to_strategy(self, ticker: str,
                                  indicators: Sequence[Callable],
                                  direction: str):
        """Adds and indicator's calculations to be executed on market data"""

        # TODO: This should probably use some sort of validation

        # + The ticker should be validated
        # + So should the indicators, not sure how though since its a function
        # + Direction can only be 'buy' and 'sell', and enum

        self.positions[direction][ticker] = indicators

    def add_strategy_event_to_queue(self, ticker, direction,
                                    event: MarketEvent):

        # TODO Need to come up with an actual strategy_id

        new_event = StrategyEvent(ticker, event.datetime, 'deez', direction)
        self.queue.put(new_event)

    def check_all(self, event: MarketEvent):
        """
        Checks all indicators in response to an update in market data

        :param event: Event that serves as the basis for any new strategy event
        :MarketEvent event:
        """

        for ticker, indicators in self.positions['long'].items():

            result = all(map(lambda func: func(self.data_handler), indicators))
            prev_state = self.directions.get(ticker, False)

            if result and not prev_state:
                self.directions[ticker] = True
                self.add_strategy_event_to_queue(ticker, 'BUY', event)
            elif not result and prev_state:
                self.directions[ticker] = False
                self.add_strategy_event_to_queue(ticker, 'SELL', event)

        for ticker, indicators in self.positions['short'].items():

            result = all(map(lambda func: func(self.data_handler), indicators))
            prev_state = self.directions.get(ticker, False)

            if result and not prev_state:
                prev_state = True
                self.directions[ticker] = True
                self.add_strategy_event_to_queue(ticker, 'SELL', event)
            elif not result and prev_state:
                self.directions[ticker] = False
                self.add_strategy_event_to_queue(ticker, 'BUY', event)
