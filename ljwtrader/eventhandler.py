import logging
from typing import Callable, NoReturn, Mapping, Sequence

from ljwtrader.strategy import Strategy
from ljwtrader.portfolio import Portfolio
from ljwtrader.events import Event, MarketEvent, StrategyEvent, OrderEvent, FillEvent
from ljwtrader.broker import InteractiveBrokers

logger = logging.getLogger(__name__)


class EventHandler:
    """
    Object that serves to route events to the proper system component based on their type

    The event handler consists of a collection of event handlers, an event map that 
    maps each event type to the proper handler, and process_events() method.
    """

    def __init__(self, queue: Sequence[Event]):
        self._queue = queue
        self.strategy: Strategy = None
        self.portfolio: Portfolio = None
        self.broker: InteractiveBrokers = None

    def _handle_market(self, event: MarketEvent):
        self.strategy.check_all(event)

    def _handle_strategy(self, event: StrategyEvent):
        self.portfolio.trigger_order(event)

    def _handle_order(self, event: OrderEvent):
        self.broker.generate_fill_order(event)

    def _handle_fill(self, event: FillEvent):
        self.portfolio.update_holdings_from_fill(event)

    def process_events(self):
        """Pops each event in the queue and directs it to the proper handler"""

        EVENT_MAP: Mapping[Event, Callable] = {
            'MARKET': self._handle_market,
            'STRATEGY': self._handle_strategy,
            'ORDER': self._handle_order,
            'FILL': self._handle_fill,
        }

        while not self._queue.empty():
            event = self._queue.get()
            try:
                event_handler = EVENT_MAP[event.event_type]
            except KeyError as e:
                logger.error(e)
            else:
                logger.debug(f"Handling {event.event_type} event")
                event_handler(event)
