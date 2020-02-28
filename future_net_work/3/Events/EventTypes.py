from py_linq import Enumerable

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
        self.seccode = self.df['seccode']
        self.secboard = self.df['secboard']



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
        self.starttime = self.df['starttime'].values[0]
        self.endtime = self.df['endtime'].values[0]
        self.taskid = self.df['taskid'].values[0]


def where(source, **kwargs):
    where_arg = ' where'
    if 'task' in kwargs.keys():
        task = source.get_task(id=kwargs['task'])
        start = str(task.starttime)
        end = str(task.endtime)
        where_arg += f' evdate between {start} and {end}'
    return where_arg


def select(mapping, *args):
    select_arg = ''
    for field in args:
        select_arg += f' {mapping.get(field, field)}'
    select_list = select_arg.split()
    result_order_list = []
    for field in select_list:
        field = f'{field},'
        result_order_list.append(field)
    select_arg = ' '.join(result_order_list)[:-1]
    return select_arg


def group_or_order_by(type, mapping, *args):
    clause = f' {type} by'
    for field in args:
        clause += f' {mapping.get(field, field)}'
    parameters_list = clause.split()
    result_list = parameters_list.copy()[:2]
    for field in parameters_list[2:]:
        field = f'{field},'
        result_list.append(field)
    clause = ' '.join(result_list)[:-1]
    return clause


class TradesData:

    def __init__(self, source):
        self.source = source
        self.where_arg = ''
        self.groupby = ''
        self.orderby = ''
        self.select_arg = '*'
        self.mapping = {'task': 'TASKID', 'date': 'EVDATE', 'time': 'ORDERTIME', 'id': 'tradeno'}

    def where(self, **kwargs):
        self.where_arg = where(source=self.source, **kwargs)
        return self

    def select(self, *args):
        self.select_arg = select(mapping=self.mapping, *args)
        return self

    def group_by(self, *args):
        self.groupby = group_or_order_by(type='group', mapping=self.mapping, *args)
        return self

    def order_by(self, *args):
        self.orderby = group_or_order_by(type='order', mapping=self.mapping, *args)
        return self

    def to_list(self):
        df = self.source.get_trades(select=self.select_arg, where=self.where_arg, group_by=self.groupby,
                                    order_by=self.orderby)
        return [Trade(row) for index, row in df.iterrows()]

    def to_frame(self):
        df = self.source.get_trades(select=self.select_arg, where=self.where_arg, group_by=self.groupby,
                                    order_by=self.orderby)
        return df

    def to_enumerable(self):
        df = self.source.get_trades(select=self.select_arg, where=self.where_arg, group_by=self.groupby,
                                    order_by=self.orderby)
        return Enumerable(df.T.to_dict().values())


class SignalsData:

    def __init__(self, source):
        self.source = source
        self.where_arg = ''
        self.groupby = ''
        self.orderby = ''
        self.select_arg = '*'
        self.mapping = {'task': 'TASKID', 'date': 'EVDATE', 'time': 'ORDERTIME', 'id': 'tradeno'}
        # self.mapping = {'task': 'TASKID','date': 'EVDATE', 'time': 'ORDERTIME', 'id': 'tradeno'}

    def where(self, **kwargs):
        self.where_arg = where(source=self.source, **kwargs)
        return self

    def select(self, *args):
        self.select_arg = select(mapping=self.mapping, *args)
        return self

    def group_by(self, *args):
        self.groupby = group_or_order_by(type='group', mapping=self.mapping, *args)
        return self

    def order_by(self, *args):
        self.orderby = group_or_order_by(type='order', mapping=self.mapping, *args)
        return self

    def to_list(self):
        df = self.source.get_signals(select=self.select_arg, where=self.where_arg, group_by=self.groupby,
                                     order_by=self.orderby)
        return [Signal(row) for index, row in df.iterrows()]

    def to_frame(self):
        df = self.source.get_signals(select=self.select_arg, where=self.where_arg, group_by=self.groupby,
                                     order_by=self.orderby)
        return df

    def to_enumerable(self):
        df = self.source.get_signals(select=self.select_arg, where=self.where_arg, group_by=self.groupby,
                                     order_by=self.orderby)
        return Enumerable(df.T.to_dict().values())


class AllTradesData:

    def __init__(self, source, **kwargs):
        self.kwargs = kwargs
        self.source = source
        self.where_arg = ''
        self.groupby = ''
        self.orderby = ''
        self.select_arg = '*'
        self.mapping = {'task': 'TASKID', 'date': 'EVDATE', 'time': 'ORDERTIME', 'id': 'tradeno'}
        # self.mapping = {'task': 'TASKID','date': 'EVDATE', 'time': 'ORDERTIME', 'id': 'tradeno'}

    def where(self, **kwargs):
        self.where_arg = where(source=self.source, **kwargs)
        return self

    def select(self, *args):
        self.select_arg = select(mapping=self.mapping, *args)
        return self

    def group_by(self, *args):
        self.groupby = group_or_order_by(type='group', mapping=self.mapping, *args)
        return self

    def order_by(self, *args):
        self.orderby = group_or_order_by(type='order', mapping=self.mapping, *args)
        return self

    def to_list(self):
        df = self.source.get_all_trades(select=self.select_arg, where=self.where_arg, group_by=self.groupby,
                                        order_by=self.orderby)
        return [Signal(row) for index, row in df.iterrows()]

    def to_frame(self):
        df = self.source.get_all_trades(select=self.select_arg, where=self.where_arg, group_by=self.groupby,
                                        order_by=self.orderby)
        return df

    def to_enumerable(self):
        df = self.source.get_all_trades(select=self.select_arg, where=self.where_arg, group_by=self.groupby,
                                        order_by=self.orderby)
        return Enumerable(df.T.to_dict().values())


class OrdersData:

    def __init__(self, source, **kwargs):
        self.kwargs = kwargs
        self.source = source
        self.where_arg = ''
        self.groupby = ''
        self.orderby = ''
        self.select_arg = '*'
        self.mapping = {'task': 'TASKID', 'date': 'EVDATE', 'time': 'ORDERTIME', 'id': 'tradeno'}
        # self.mapping = {'task': 'TASKID','date': 'EVDATE', 'time': 'ORDERTIME', 'id': 'tradeno'}

    def where(self, **kwargs):
        self.where_arg = where(source=self.source, **kwargs)
        return self

    def select(self, *args):
        self.select_arg = select(mapping=self.mapping, *args)
        return self

    def group_by(self, *args):
        self.groupby = group_or_order_by(type='group', mapping=self.mapping, *args)
        return self

    def order_by(self, *args):
        self.orderby = group_or_order_by(type='order', mapping=self.mapping, *args)
        return self

    def to_list(self):
        df = self.source.get_orders(select=self.select_arg, where=self.where_arg, group_by=self.groupby,
                                    order_by=self.orderby)
        return [Signal(row) for index, row in df.iterrows()]

    def to_frame(self):
        df = self.source.get_orders(select=self.select_arg, where=self.where_arg, group_by=self.groupby,
                                    order_by=self.orderby)
        return df

    def to_enumerable(self):
        df = self.source.get_orders(select=self.select_arg, where=self.where_arg, group_by=self.groupby,
                                    order_by=self.orderby)
        return Enumerable(df.T.to_dict().values())


class EventsData:

    def __init__(self, source, **kwargs):
        self.kwargs = kwargs
        self.source = source
        self.where_arg = ''
        self.groupby = ''
        self.orderby = ''
        self.select_arg = '*'
        self.mapping = {'task': 'TASKID', 'date': 'EVDATE', 'time': 'ORDERTIME', 'id': 'tradeno'}
        # self.mapping = {'task': 'TASKID','date': 'EVDATE', 'time': 'ORDERTIME', 'id': 'tradeno'}

    def where(self, **kwargs):
        self.where_arg = where(source=self.source, **kwargs)
        return self

    def select(self, *args):
        self.select_arg = select(mapping=self.mapping, *args)
        return self

    def group_by(self, *args):
        self.groupby = group_or_order_by(type='group', mapping=self.mapping, *args)
        return self

    def order_by(self, *args):
        self.orderby = group_or_order_by(type='order', mapping=self.mapping, *args)
        return self

    def to_list(self):
        df = self.source.get_events(select=self.select_arg, where=self.where_arg, group_by=self.groupby,
                                    order_by=self.orderby)
        return [Signal(row) for index, row in df.iterrows()]

    def to_frame(self):
        df = self.source.get_events(select=self.select_arg, where=self.where_arg, group_by=self.groupby,
                                    order_by=self.orderby)
        return df

    def to_enumerable(self):
        df = self.source.get_events(select=self.select_arg, where=self.where_arg, group_by=self.groupby,
                                    order_by=self.orderby)
        return Enumerable(df.T.to_dict().values())
