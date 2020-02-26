from .Repo import Repo
import datetime
from pandas import DataFrame
from EventMonitoringDeploy import monitoring_instance
from Events.EventTypes import Task, Trade, Signal, AllTrades, Orders, Events


class DbRepo(Repo):
    def __init__(self, connection, markets):
        super(DbRepo, self).__init__()
        self.connection = connection
        self.markets = markets
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
        result = self.connection[f'{schema.lower()}_{self.market}'].execute(query)
        return result

    def get_markets(self):
        return list(self.markets)

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
            task = self.get_task(id=kwargs['task'])
            start = datetime.datetime.strptime(str(task.starttime), "%Y%m%d")
            end = datetime.datetime.strptime(str(task.endtime), "%Y%m%d")
            dates += [date.strftime("%Y%m%d") for date in
                      [start + datetime.timedelta(days=x) for x in range(0, (end - start).days + 1)]]
            taskid = kwargs.pop('task')
        if 'tradeid' in kwargs.keys():
            kwargs['TRADENO'] = kwargs.pop('tradeid')
        if 'date' in kwargs.keys():
            dates.append(datetime.datetime.strptime(kwargs.pop('date'), "%d.%m.%Y").strftime("%Y%m%d"))
        if 'type' in kwargs.keys():
            kwargs['evtype'] = mapping_type[kwargs.pop('type')]
        return dates, kwargs, taskid

    def get_task(self, id):
        request_get_task = f'SELECT * FROM FRC_TASKS where TASKID = {id}'
        result_custom_signals = self.connection[f'client_{str(self.market)}'].execute(request_get_task)
        df = self.__make_dataframe(result_custom_signals)
        task = Task(df)
        return task

    def get_trades(self, order_by, **kwargs):
        trades = []
        dates, kwargs = self.__get_dates_and_arguments(**kwargs)[:2]
        return TradeList(connection=self.connection[f'history_{str(self.market)}'], dates=dates, kwargs=kwargs)
        # for date in dates:
        #     df = self.__make_dataframe(self.get_data(date=str(date), table='FRC_TRADES', schema='history', **kwargs))
        #     trades_for_date = [Trade(row) for index, row in df.iterrows()]
        #     trades += trades_for_date
        # return trades

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
            df = self.__make_dataframe(
                self.get_data(date=str(date), table='FRC_ALL_TRADES', schema='history', **kwargs))
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
            query_request = self.connection[f'{schema.lower()}_{self.market}'].execute(query)
        df = self.__make_dataframe(query_request)
        return df


def make_dataframe(output_request):
    df = DataFrame(output_request.fetchall())
    df.columns = output_request.keys()
    df.columns = df.columns.str.lower()
    return df


def condition_for_request(**kwargs):
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


def get_data(connection, date, table, order_by, **kwargs):
    kwargs['EVDATE'] = date
    query = f'SELECT * FROM {table} {condition_for_request(**kwargs)} {order_by}'
    result = connection.execute(query)
    return result


class TradeList:
    def __init__(self, connection, dates, kwargs):
        self.connection = connection
        self.dates = dates
        self.kwargs = kwargs
        self.orderby = ''

    def get_trades(self):
        trades = []
        for date in self.dates:
            df = make_dataframe(
                get_data(connection=self.connection, date=str(date), table='FRC_TRADES', order_by=self.orderby, **self.kwargs))
            trades_for_date = [Trade(row) for index, row in df.iterrows()]
            trades += trades_for_date
        return trades

    def order_by(self, args):
        self.orderby = 'order by'
        for field in args:
            self.orderby += f' {field}'
        order_list = self.orderby.split()
        result_order_list = order_list.copy()[:3]
        for field in order_list[3:]:
            field = f',{field}'
            result_order_list.append(field)
        self.orderby = ' '.join(result_order_list)

    def __iter__(self):
        return iter(self.get_trades())

    def __len__(self):
        return len(self.get_trades())
    #
    # def __call__(self, *args, **kwargs):
    #     return self.get_trades()



