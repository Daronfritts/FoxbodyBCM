"""
event_bus.py

Foxbody BCM Event Bus

Allows every module to communicate without being directly connected.
"""

from collections import defaultdict

from logger import logger


class EventBus:

    def __init__(self):
        self._subscribers = defaultdict(list)

    def subscribe(self, event_name, callback):
        """
        Register a callback for an event.
        """

        self._subscribers[event_name].append(callback)

        logger.info(
            f"EventBus | Registered '{callback.__name__}' for '{event_name}'"
        )

    def publish(self, event_name, data=None):
        """
        Publish an event to all subscribers.
        """

        logger.info(
            f"EventBus | Publishing '{event_name}'"
        )

        if event_name not in self._subscribers:
            return

        for callback in self._subscribers[event_name]:

            try:
                callback(data)

            except Exception as error:

                logger.error(
                    f"EventBus | Error in '{callback.__name__}': {error}"
                )


event_bus = EventBus()
