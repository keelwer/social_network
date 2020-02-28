from abc import ABC, abstractmethod


class Repo:
    @abstractmethod
    def get_task(self, *args, **kwargs):
        pass

    @abstractmethod
    def get_trades(self, *args, **kwargs):
        pass

    @abstractmethod
    def get_signals(self, *args, **kwargs):
        pass

    @abstractmethod
    def get_all_trades(self, *args, **kwargs):
        pass

    @abstractmethod
    def get_orders(self, *args, **kwargs):
        pass

    @abstractmethod
    def get_events(self, *args, **kwargs):
        pass

