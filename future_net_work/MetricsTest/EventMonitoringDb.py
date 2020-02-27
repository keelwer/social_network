from Events.EventTypes import TradesData, SignalsData, AllTradesData, OrdersData, EventsData



class EventMonitoringDb:

    def __init__(self, source):
        self.source = source

    def get_markets(self):
        return self.source.get_markets()

    def set_market(self, market):
        return self.source.set_market(market)

    def get_task(self, id):
        return self.source.get_task(id)

    def get_trades(self, **kwargs):
        trades = TradesData(source=self.source, **kwargs)
        return trades

    def get_signals(self, **kwargs):
        signals = SignalsData(source=self.source, **kwargs)
        return signals

    def get_all_trades(self, **kwargs):
        alltrades = AllTradesData(source=self.source, **kwargs)
        return alltrades

    def get_orders(self, **kwargs):
        orders = OrdersData(source=self.source, **kwargs)
        return orders

    def get_events(self, **kwargs):
        events = EventsData(source=self.source, **kwargs)
        return events

    def execute(self, schema, query):
        return self.source.execute(schema, query)

