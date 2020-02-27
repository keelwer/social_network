from abc import ABC, abstractmethod


class Repo:
    @abstractmethod
    def get_task(self, id):
        pass

    @abstractmethod
    def get_trades(self, order_by):
        pass

    @abstractmethod
    def get_signals(self, order_by):
        pass

    @abstractmethod
    def get_all_trades(self, order_by):
        pass

    @abstractmethod
    def get_orders(self, order_by):
        pass

    @abstractmethod
    def get_events(self, order_by):
        pass

    def execute(self, schema, query):
        pass
