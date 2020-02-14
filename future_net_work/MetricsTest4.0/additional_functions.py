from datetime import datetime
import sqlalchemy
from pandas import DataFrame


def create_connstr_meta(params):
    if params['database']['provider'] == 'mssql':
        type_instance = ''
        if params['instance'].get("type"):
            type_instance = f".{params['instance'].get('type')}"
        conn_string = f"mssql+pyodbc://{params['instance']['login']}:{params['instance']['password']}@{params['database']['server']}:1433/{params['instance']['name']}{type_instance}.ClientMetadata?driver=SQL+Server+Native+Client+11.0"
    return conn_string


def create_connstr_client_history(params, schema, market):
    if params['database']['provider'] == 'mssql':
        type_instance = ''
        if params['instance'].get("type"):
            type_instance = f".{params['instance'].get('type')}"
        schema = f'.{schema}'
        market = f'{market}'
        conn_string = f"mssql+pyodbc://{params['instance']['login']}:{params['instance']['password']}@{params['database']['server']}:1433/{params['instance']['name']}{type_instance}{schema}{market}?driver=SQL+Server+Native+Client+11.0"
    return conn_string


def condition(**kwargs):
    condition = ''
    if kwargs:
        condition = 'where '
    for field, value in kwargs.items():
        condition += f' {field}={value}'
    condition_list = condition.split()
    result_condition = condition_list.copy()[:2]
    for condition_parameter in condition_list[2:]:
        condition_parameter = f'and {condition_parameter}'
        result_condition.append(condition_parameter)
    condition = ' '.join(result_condition)
    return condition


class MetricTest:

    def __init__(self, connect_params=None):
        self.connect_params = connect_params
        self.market = None

    def get_markets(self):
        markets = []
        get_market_request = '''SELECT TYPE FROM FRC_MARKETS'''
        engine = sqlalchemy.create_engine(create_connstr_meta(self.connect_params))
        result_trades = engine.execute(get_market_request)
        for row in result_trades:
            markets.append(row[0])
        return markets

    def set_market(self, market):
        self.market = market

    def create_engine(self, schema, market):
        engine = sqlalchemy.create_engine(create_connstr_client_history(self.connect_params, schema, market))
        return engine

    def make_dataframe(self, output_request):
        df = DataFrame(output_request.fetchall())
        df.columns = output_request.keys()
        df.columns = df.columns.str.lower()
        return df

    def get_task(self, id, market=None):
        if self.market:
            market = self.market
        request_get_task = f'SELECT distinct EVDATE, TASKID FROM FRC_CUSTOMSIGNALS where TASKID = {id}'
        result_custom_signals = self.create_engine(market=market, schema='Client').execute(request_get_task)
        df = self.make_dataframe(result_custom_signals)
        tasks = [Task(row) for index, row in df.iterrows()]
        return tasks

    def get_trades(self, market=None, **kwargs):
        trades = []
        dates = []
        if self.market:
            market = self.market
        if 'task' in kwargs.keys():
            dates += [task.date for task in self.get_task(id=kwargs['task'], market=market)]
            kwargs.pop('task')
        if 'tradeid' in kwargs.keys():
            kwargs['TRADENO'] = kwargs.pop('tradeid')
        if 'date' in kwargs.keys():
            dates.append(datetime.strptime(kwargs.pop('date'), "%d.%m.%Y").strftime("%Y%m%d"))
        for date in dates:
            kwargs['EVDATE'] = date
            request_trades = f'SELECT * FROM FRC_TRADES {condition(**kwargs)}'
            result_trades = self.create_engine(market=market, schema='History').execute(request_trades)
            df = self.make_dataframe(result_trades)
            trades_in_date = [Trade(row) for index, row in df.iterrows()]
            trades += trades_in_date
        return trades

    def get_signals(self, market=None, **kwargs):
        signals = []
        dates = []
        if self.market:
            market = self.market
        if 'date' in kwargs.keys():
            dates.append(datetime.strptime(kwargs.pop('date'), "%d.%m.%Y").strftime("%Y%m%d"))
        if 'task' in kwargs.keys():
            dates += [task.date for task in self.get_task(id=kwargs['task'], market=market)]
            kwargs['taskid'] = kwargs.pop('task')
        for date in dates:
            kwargs['EVDATE'] = date
            request_custom_signals = f'SELECT * FROM FRC_CUSTOMSIGNALS {condition(**kwargs)}'
            result_custom_signals = self.create_engine(market=market, schema='Client').execute(request_custom_signals)
            df = self.make_dataframe(result_custom_signals)
            signals_in_date = [Signal(row) for index, row in df.iterrows()]
            signals += signals_in_date
        return signals

    def get_all_trades(self, market=None, **kwargs):
        all_trades = []
        dates = []
        if self.market:
            market = self.market
        if 'date' in kwargs.keys():
            kwargs['evdate'] = datetime.strptime(kwargs.pop('date'), "%d.%m.%Y").strftime("%Y%m%d")
        if 'task' in kwargs.keys():
            dates += [task.date for task in self.get_task(id=kwargs['task'], market=market)]
            kwargs.pop('task')
        for date in dates:
            kwargs['EVDATE'] = date
            request_all_trades = f'SELECT * FROM FRC_ALL_TRADES {condition(**kwargs)}'
            result_all_trades = self.create_engine(market=market, schema='History').execute(request_all_trades)
            df = self.make_dataframe(result_all_trades)
            all_trades_in_date = [AllTrades(row) for index, row in df.iterrows()]
            all_trades += all_trades_in_date
        return all_trades

    def get_orders(self, market=None, **kwargs):
        orders = []
        dates = []
        if self.market:
            market = self.market
        if 'date' in kwargs.keys():
            kwargs['evdate'] = datetime.strptime(kwargs.pop('date'), "%d.%m.%Y").strftime("%Y%m%d")
        request_orders = f'SELECT * FROM FRC_ORDERS {condition(**kwargs)}'
        result_orders = self.create_engine(market=market, schema='History').execute(request_orders)
        df = self.make_dataframe(result_orders)
        orders = [Orders(row) for index, row in df.iterrows()]
        return orders

    def get_events(self, market=None, **kwargs):
        events = []
        dates = []
        if self.market:
            market = self.market
        mapping_type = {'trade': 2, 'order': 1, 'withdraws': 3, 'alltrades': 12, 'timeevents': 14}
        if 'type' in kwargs.keys():
            kwargs['evtype'] = mapping_type[kwargs.pop('type')]
        if 'date' in kwargs.keys():
            kwargs['evdate'] = datetime.strptime(kwargs.pop('date'), "%d.%m.%Y").strftime("%Y%m%d")
        request_events = f'SELECT * FROM FRC_EVENTS {condition(**kwargs)}'
        result_events = self.create_engine(market=market, schema='History').execute(request_events)
        df = self.make_dataframe(result_events)
        events = [Events(row) for index, row in df.iterrows()]
        return events

    def execute_custom_request(self, market=None, schema=None, request=None):
        if self.market:
            market = self.market
        if schema == 'metadata':
            engine = sqlalchemy.create_engine(create_connstr_meta(self.connect_params))
            result_request = engine.execute(request)
        else:
            result_request = self.create_engine(market=market, schema=schema).execute(request)
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
