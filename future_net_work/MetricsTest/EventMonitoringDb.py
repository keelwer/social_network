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
        return self.source.get_trades(**kwargs)

    def get_signals(self, **kwargs):
        return self.source.get_signals(**kwargs)

    def get_all_trades(self, **kwargs):
        return self.source.get_all_trades(**kwargs)

    def get_orders(self, **kwargs):
        return self.source.get_orders(**kwargs)

    def get_events(self, **kwargs):
        return self.source.get_events(**kwargs)

    def execute(self, schema, query):
        return self.source.execute(schema, query)
