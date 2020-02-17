from datetime import datetime
from pandas import DataFrame
from EventMonitoring.Database import database_connection


class MetricTest:

    def __init__(self, connect_params=None):
        self.connect_params = connect_params
        self.db = database_connection.DbConnection(self.connect_params)
        self.market = None

    def get_markets(self):
        return self.db.get_markets()

    def set_market(self, market):
        self.market = market

    def make_dataframe(self, output_request):
        df = DataFrame(output_request.fetchall())
        df.columns = output_request.keys()
        df.columns = df.columns.str.lower()
        return df

    def get_dates_and_arguments(self, market=None, **kwargs):
        dates = []
        mapping_type = {'trade': 2, 'order': 1, 'withdraws': 3, 'alltrades': 12, 'timeevents': 14}
        if 'task' in kwargs.keys():
            dates += [task.date for task in self.get_task(id=kwargs['task'], market=market)]
            kwargs.pop('task')
        if 'tradeid' in kwargs.keys():
            kwargs['TRADENO'] = kwargs.pop('tradeid')
        if 'date' in kwargs.keys():
            dates.append(datetime.strptime(kwargs.pop('date'), "%d.%m.%Y").strftime("%Y%m%d"))
        if 'type' in kwargs.keys():
            kwargs['evtype'] = mapping_type[kwargs.pop('type')]
        return dates, kwargs


    def get_task(self, id, market=None):
        if self.market:
            market = self.market
        request_get_task = f'SELECT distinct EVDATE, TASKID FROM FRC_CUSTOMSIGNALS where TASKID = {id}'
        result_custom_signals = self.db.create_engine(market=market, schema='Client').execute(request_get_task)
        df = self.make_dataframe(result_custom_signals)
        tasks = [Task(row) for index, row in df.iterrows()]
        return tasks

    def get_trades(self, market=None, **kwargs):
        trades = []
        if self.market:
            market = self.market
        dates, kwargs = self.get_dates_and_arguments(market=market, **kwargs)
        for date in dates:
            df = self.make_dataframe(
                self.db.get_data(date=str(date), market=market, table='FRC_TRADES', schema='History', **kwargs))
            trades_for_date = [Trade(row) for index, row in df.iterrows()]
            trades += trades_for_date
        return trades

    def get_signals(self, market=None, **kwargs):
        signals = []
        if self.market:
            market = self.market
        dates, kwargs = self.get_dates_and_arguments(market=market, **kwargs)
        for date in dates:
            df = self.make_dataframe(
                self.db.get_data(date=str(date), market=market, table='FRC_CUSTOMSIGNALS', schema='Client', **kwargs))
            signals_for_date = [Signal(row) for index, row in df.iterrows()]
            signals += signals_for_date
        return signals

    def get_all_trades(self, market=None, **kwargs):
        all_trades = []
        if self.market:
            market = self.market
        dates, kwargs = self.get_dates_and_arguments(market=market, **kwargs)
        for date in dates:
            df = self.make_dataframe(
                self.db.get_data(date=str(date), market=market, table='FRC_ALL_TRADES', schema='History', **kwargs))
            all_trades_for_date = [AllTrades(row) for index, row in df.iterrows()]
            all_trades += all_trades_for_date
        return all_trades

    def get_orders(self, market=None, **kwargs):
        orders = []
        dates = []
        if self.market:
            market = self.market
        dates, kwargs = self.get_dates_and_arguments(market=market, **kwargs)
        for date in dates:
            df = self.make_dataframe(
                self.db.get_data(date=str(date), market=market, table='FRC_ORDERS', schema='History', **kwargs))
            orders_for_date = [Orders(row) for index, row in df.iterrows()]
            orders += orders_for_date
        return orders

    def get_events(self, market=None, **kwargs):
        events = []
        if self.market:
            market = self.market
        dates, kwargs = self.get_dates_and_arguments(market=market, **kwargs)
        for date in dates:
            df = self.make_dataframe(
                self.db.get_data(date=str(date), market=market, table='FRC_EVENTS', schema='History', **kwargs))
            events_for_date = [Events(row) for index, row in df.iterrows()]
            events += events_for_date
        return events

    def execute_custom_request(self, market=None, schema=None, request=None):
        if self.market:
            market = self.market
        if schema == 'metadata':
            engine = self.db.create_engine(connect_params=self.connect_params)
            result_request = engine.execute(request)
        else:
            result_request = self.db.create_engine(market=market, schema=schema).execute(request)
        return result_request


class Trade:

    def __init__(self, df):
        self.df = df
        self.date = self.df['evdate']
        self.tradeid = self.df['tradeno']
        self.price = self.df['price']
        self.quantity = self.df['quantity']


class Signal:

    def __init__(self, df):
        self.df = df
        self.taskid = self.df['taskid']
        self.date = self.df['evdate']
        self.tradeid = self.df['tsno']
        self.evtype = self.df['evtype']
        self.price = self.df['price']
        self.message = self.df['message']
        self.quantity = self.df['quantity']


class AllTrades:

    def __init__(self, df):
        self.df = df
        self.date = self.df['evdate']
        self.tradeid = self.df['tradeno']
        self.value = self.df['value']
        self.price = self.df['price']
        self.quantity = self.df['quantity']


class Orders:

    def __init__(self, df):
        self.df = df
        self.date = self.df['evdate']
        self.orderid = self.df['orderno']
        self.value = self.df['value']
        self.price = self.df['price']
        self.quantity = self.df['quantity']


class Events:

    def __init__(self, df):
        self.df = df
        self.date = self.df['evdate']
        self.orderid = self.df['orderno']
        self.evtype = self.df['evtype']
        self.tradeid = self.df['tradeno']


class Task:

    def __init__(self, df):
        self.df = df
        self.date = self.df['evdate']
        self.taskid = self.df['taskid']
