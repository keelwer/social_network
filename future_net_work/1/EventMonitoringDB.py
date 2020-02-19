from datetime import datetime
from pandas import DataFrame
from EventMonitoring.Deploy import monitoring_instance


class EventMonitoringDB:

    def __init__(self, instance_dir):
        self.instance_dir = instance_dir
        self.instance = monitoring_instance.MonitoringInstance(self.instance_dir)
        self.connection = self.instance.get_connections()
        self.market = None

    def condition_for_request(self, **kwargs):
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

    def get_data(self, date, table, schema, **kwargs):
        kwargs['EVDATE'] = date
        query = f'SELECT * FROM {table} {self.condition_for_request(**kwargs)}'
        result = self.connection[f'{schema.lower()}_{self.market.lower()}'].execute(query)
        return result

    def get_markets(self):
        return list(self.instance.get_market_config().values())

    def set_market(self, market):
        self.market = market

    def __make_dataframe(self, output_request):
        df = DataFrame(output_request.fetchall())
        df.columns = output_request.keys()
        df.columns = df.columns.str.lower()
        return df

    def __get_dates_and_arguments(self, **kwargs):
        dates = []
        mapping_type = {'trade': 2, 'order': 1, 'withdraws': 3, 'alltrades': 12, 'timeevents': 14}
        taskid = None
        if 'task' in kwargs.keys():
            dates += [task.date for task in self.get_task(id=kwargs['task'])]
            taskid = kwargs.pop('task')
        if 'tradeid' in kwargs.keys():
            kwargs['TRADENO'] = kwargs.pop('tradeid')
        if 'date' in kwargs.keys():
            dates.append(datetime.strptime(kwargs.pop('date'), "%d.%m.%Y").strftime("%Y%m%d"))
        if 'type' in kwargs.keys():
            kwargs['evtype'] = mapping_type[kwargs.pop('type')]
        return dates, kwargs, taskid

    def get_task(self, id):
        request_get_task = f'SELECT distinct EVDATE, TASKID FROM FRC_CUSTOMSIGNALS where TASKID = {id}'
        result_custom_signals = self.connection[f'client_{self.market.lower()}'].execute(request_get_task)
        df = self.__make_dataframe(result_custom_signals)
        tasks = [Task(row) for index, row in df.iterrows()]
        return tasks

    def get_trades(self, **kwargs):
        trades = []
        dates, kwargs = self.__get_dates_and_arguments(**kwargs)[:2]
        for date in dates:
            df = self.__make_dataframe(self.get_data(date=str(date), table='FRC_TRADES', schema='history', **kwargs))
            trades_for_date = [Trade(row) for index, row in df.iterrows()]
            trades += trades_for_date
        return trades

    def get_signals(self, **kwargs):
        signals = []
        dates, kwargs, taskid = self.__get_dates_and_arguments(**kwargs)
        if taskid:
            kwargs['taskid'] = taskid
        for date in dates:
            df = self.__make_dataframe(
                self.get_data(date=str(date), table='FRC_CUSTOMSIGNALS', schema='client', **kwargs))
            signals_for_date = [Signal(row) for index, row in df.iterrows()]
            signals += signals_for_date
        return signals

    def get_all_trades(self, **kwargs):
        all_trades = []
        dates, kwargs = self.__get_dates_and_arguments(**kwargs)[:2]
        for date in dates:
            df = self.__make_dataframe(self.get_data(date=str(date), table='FRC_ALL_TRADES', schema='history', **kwargs))
            all_trades_for_date = [AllTrades(row) for index, row in df.iterrows()]
            all_trades += all_trades_for_date
        return all_trades

    def get_orders(self, **kwargs):
        orders = []
        dates, kwargs = self.__get_dates_and_arguments(**kwargs)[:2]
        for date in dates:
            df = self.__make_dataframe(self.get_data(date=str(date), table='FRC_ORDERS', schema='history', **kwargs))
            orders_for_date = [Orders(row) for index, row in df.iterrows()]
            orders += orders_for_date
        return orders

    def get_events(self, **kwargs):
        events = []
        dates, kwargs = self.__get_dates_and_arguments(**kwargs)[:2]
        for date in dates:
            df = self.__make_dataframe(self.get_data(date=str(date), table='FRC_EVENTS', schema='history', **kwargs))
            events_for_date = [Events(row) for index, row in df.iterrows()]
            events += events_for_date
        return events

    def execute(self, schema, query):
        if schema == 'metadata':
            query_request = self.connection[f'metadata'].execute(query)
        else:
            query_request = self.connection[f'{schema.lower()}_{self.market.lower()}'].execute(query)
        df = self.__make_dataframe(query_request)
        return df


class Trade:

    def __init__(self, df):
        self.df = df
        self.date = self.df['evdate']
        self.tradeid = self.df['tradeno']
        self.price = self.df['price']
        self.quantity = self.df['quantity']
        self.secboard = self.df['secboard']
        self.seccode = self.df['seccode']


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
        self.id = self.df['id']
        self.date = self.df['evdate']
        self.tradeid = self.df['tradeno']
        self.value = self.df['value']
        self.price = self.df['price']
        self.quantity = self.df['quantity']
        self.secboard = self.df['secboard']
        self.seccode = self.df['seccode']


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
        self.evno = self.df['evno']


class Task:

    def __init__(self, df):
        self.df = df
        self.date = self.df['evdate']
        self.taskid = self.df['taskid']
