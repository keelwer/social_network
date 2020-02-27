from Events.EventTypes import Task, Trade, Signal, AllTrades, Orders, Events
import datetime
import pandas


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
        trades = TradeData(source=self.source, **kwargs)
        # return self.source.get_trades(**kwargs)
        return trades

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


class TradeData:

    def __init__(self, source, **kwargs):
        self.kwargs = kwargs
        self.source = source
        self.where_arg = ''
        self.groupby = ''
        self.orderby = ''
        self.select_arg = '*'
        self.mapping = {'task': 'TASKID','date': 'EVDATE', 'time': 'ORDERTIME', 'id': 'tradeno'}

    def where(self, **kwargs):
        self.where_arg = ' where'
        if 'task' in kwargs.keys():
            task = self.source.get_task(id=kwargs['task'])
            # start = datetime.datetime.strptime(str(task.starttime), "%Y%m%d")
            # end = datetime.datetime.strptime(str(task.endtime), "%Y%m%d")
            start = str(task.starttime)
            end = str(task.endtime)
            self.where_arg += f' evdate between {start} and {end}'
        return self

    def select(self, *args):
        self.select_arg = ''
        for field in args:
            self.select_arg += f' {self.mapping.get(field, field)}'
        select_list = self.select_arg.split()
        # result_order_list = select_list.copy()[:1]
        result_order_list = []
        for field in select_list:
            field = f'{field},'
            result_order_list.append(field)
        self.select_arg = ' '.join(result_order_list)[:-1]
        return self

    def group_by(self, *args):
        self.groupby = ' group by'
        for field in args:
            self.groupby += f' {self.mapping.get(field, field)}'
        group_list = self.groupby.split()
        result_order_list = group_list.copy()[:2]
        for field in group_list[2:]:
            field = f'{field},'
            result_order_list.append(field)
        self.groupby = ' '.join(result_order_list)[:-1]
        return self

    def order_by(self, *args):
        self.orderby = ' order by'
        for field in args:
            print(field)
            # self.orderby += f' {self.mapping.get(str(field), default=str(field))}'
            self.orderby += f' {self.mapping.get(field, field)}'
        order_list = self.orderby.split()
        result_order_list = order_list.copy()[:2]
        for field in order_list[2:]:
            field = f'{field},'
            result_order_list.append(field)
        self.orderby = ' '.join(result_order_list)[:-1]
        return self

    def __make_dataframe(self, output_request):
        df = pandas.DataFrame(output_request.fetchall())
        df.columns = output_request.keys()
        df.columns = df.columns.str.lower()
        return df

    def get_data(self):
        query = f'SELECT {self.select_arg} FROM FRC_TRADES{self.where_arg} {self.groupby} {self.orderby}'
        result = self.source.connection[f'history_{self.source.market}'].execute(query)
        return result

    def to_list(self):
        df = self.__make_dataframe(self.get_data())
        return [Trade(row) for index, row in df.iterrows()]
