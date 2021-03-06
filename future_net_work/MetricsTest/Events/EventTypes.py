from py_linq import Enumerable


class Trade:
    name = 'trade'

    def __init__(self, row):
        self.date = row.get('EVDATE', None)
        self.id = row.get('TRADENO', None)
        self.price = row.get('PRICE', None)
        self.quantity = row.get('QUANTITY', None)
        self.value = row.get('VALUE', None)
        self.secboard = row.get('SECBOARD', None)
        self.seccode = row.get('SECCODE', None)
        self.user = row.get('USERID', None)
        self.orderid = row.get('ORDERNO', None)
        self.time = row.get('TRADETIME', None)
        self.buysell = row.get('BUYSELL', None)
        self.specialcode = row.get('SPECIALCODE', None)


class Signal:

    def __init__(self, row):
        self.task = row.get('TASKID', None)
        self.date = row.get('EVDATE', None)
        self.time = row.get('EVTIME', None)
        self.tradeid = row.get('TSNO', None)
        self.orderid = row.get('ORDERNO', None)
        self.type = row.get('EVTYPE', None)
        self.price = row.get('PRICE', None)
        self.message = row.get('MESSAGE', None)
        self.quantity = row.get('QUANTITY', None)
        self.seccode = row.get('SECCODE', None)
        self.secboard = row.get('SECBOARD', None)
        self.value = row.get('VALUE', None)
        self.user = row.get('USERID', None)


class AllTrades:
    name = 'alltrades'

    def __init__(self, row):
        self.id = row.get('TRADENO', None)
        self.date = row.get('EVDATE', None)
        self.time = row.get('TRADETIME', None)
        self.seccode = row.get('SECCODE', None)
        self.secboard = row.get('SECBOARD', None)
        self.price = row.get('PRICE', None)
        self.quantity = row.get('QUANTITY', None)
        self.value = row.get('VALUE', None)


class Orders:
    name = 'order'

    def __init__(self, row):
        self.date = row.get('EVDATE', None)
        self.secboard = row.get('SECBOARD', None)
        self.seccode = row.get('SECCODE', None)
        self.id = row.get('ORDERNO', None)
        self.price = row.get('PRICE', None)
        self.quantity = row.get('QUANTITY', None)
        self.value = row.get('VALUE', None)
        self.time = row.get('ORDERTIME', None)


class Events:

    def __init__(self, row):
        self.date = row.get('EVDATE', None)
        self.type = row.get('EVTYPE', None)
        self.time = row.get('EVTIME', None)
        self.orderid = row.get('ORDERNO', None)
        self.tradeid = row.get('TRADENO', None)


class TimeEvents:
    name = 'timeevents'


class Task:

    def __init__(self, row):
        self.starttime = row.get('STARTTIME', None)
        self.endtime = row.get('ENDTIME', None)
        self.taskid = row.get('TASKID', None)


def where(source, name_event=None, mapping=None, **kwargs):
    where_arg = 'where'
    if name_event == 'signal':
        where_arg += f'|{mapping["task"]} = {kwargs["task"]}'
        kwargs.pop('task')
    elif 'task' in kwargs.keys():
        task = source.get_task(id=kwargs['task'])
        start = str(task.starttime)
        end = str(task.endtime)
        where_arg += f'|{mapping["date"]} between {start} and {end}'
    for field, value in kwargs.items():
        where_arg += f'|{mapping.get(field, field)}={value}'
    where_list = where_arg.split('|')
    result_condition = where_list.copy()[:2]
    for condition_parameter in where_list[2:]:
        condition_parameter = f'and {condition_parameter}'
        result_condition.append(condition_parameter)
    where_arg = ' '.join(result_condition)
    return where_arg


def select(*args, mapping):
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


def group_or_order_by(*args, type_clause, mapping):
    clause = f' {type_clause} by'
    for field in args:
        clause += f' {mapping.get(field, field)}'
    parameters_list = clause.split()
    result_list = parameters_list.copy()[:2]
    for field in parameters_list[2:]:
        field = f'{field},'
        result_list.append(field)
    clause = ' '.join(result_list)[:-1]
    return clause


class BaseClassData:
    def __init__(self, source):
        self.source = source
        self.where_arg = ''
        self.groupby = ''
        self.orderby = ''
        self.select_arg = '*'
        self.mapping = {}

    def where(self, **kwargs):
        self.where_arg = where(source=self.source, mapping=self.mapping, **kwargs).upper()
        return self

    def group_by(self, *args):
        self.select_arg = select(mapping=self.mapping, *args).upper()
        self.groupby = group_or_order_by(type_clause='group', mapping=self.mapping, *args).upper()
        return self

    def order_by(self, *args):
        self.orderby = group_or_order_by(type_clause='order', mapping=self.mapping, *args).upper()
        return self


class TradesData(BaseClassData):

    def __init__(self, source):
        super(TradesData, self).__init__(source)
        self.source = source
        self.mapping = {'task': 'TASKID', 'date': 'EVDATE', 'id': 'TRADENO', 'user': 'USERID', 'orderid': 'ORDERNO',
                        'time': 'TRADETIME'}

    def to_list(self):
        data = self.source.get_trades(select=self.select_arg, where=self.where_arg, group_by=self.groupby,
                                      order_by=self.orderby, make_df=False)
        return [Trade(row) for row in data]

    def to_frame(self):
        dataframe = self.source.get_trades(select=self.select_arg, where=self.where_arg, group_by=self.groupby,
                                           order_by=self.orderby, make_df=True)
        return dataframe

    def to_enumerable(self):
        data = self.source.get_trades(select=self.select_arg, where=self.where_arg, group_by=self.groupby,
                                      order_by=self.orderby, make_df=False)
        return Enumerable(data)


class SignalsData(BaseClassData):

    def __init__(self, source):
        super(SignalsData, self).__init__(source)
        self.source = source
        self.mapping = {'task': 'TASKID', 'date': 'EVDATE', 'time': 'EVTIME', 'tradeid': 'TSNO', 'orderid': 'ORDERNO',
                        'type': 'EVTYPE'}

    def where(self, **kwargs):
        self.where_arg = where(source=self.source, mapping=self.mapping, name_event='signal', **kwargs).upper()
        return self

    def to_list(self):
        data = self.source.get_signals(select=self.select_arg, where=self.where_arg, group_by=self.groupby,
                                       order_by=self.orderby, make_df=False)
        return [Signal(row) for row in data]

    def to_frame(self):
        dataframe = self.source.get_signals(select=self.select_arg, where=self.where_arg, group_by=self.groupby,
                                            order_by=self.orderby, make_df=True)
        return dataframe

    def to_enumerable(self):
        data = self.source.get_signals(select=self.select_arg, where=self.where_arg, group_by=self.groupby,
                                       order_by=self.orderby, make_df=False)
        return Enumerable(data)


class AllTradesData(BaseClassData):

    def __init__(self, source):
        super(AllTradesData, self).__init__(source)
        self.source = source
        self.mapping = {'id': 'TRADENO', 'date': 'EVDATE', 'time': 'TRADETIME'}

    def to_list(self):
        data = self.source.get_all_trades(select=self.select_arg, where=self.where_arg, group_by=self.groupby,
                                          order_by=self.orderby, make_df=False)
        return [Trade(row) for row in data]

    def to_frame(self):
        dataframe = self.source.get_all_trades(select=self.select_arg, where=self.where_arg, group_by=self.groupby,
                                               order_by=self.orderby, make_df=True)
        return dataframe

    def to_enumerable(self):
        data = self.source.get_all_trades(select=self.select_arg, where=self.where_arg, group_by=self.groupby,
                                          order_by=self.orderby, make_df=False)
        return Enumerable(data)


class OrdersData(BaseClassData):

    def __init__(self, source):
        super(OrdersData, self).__init__(source)
        self.source = source
        self.mapping = {'date': 'EVDATE', 'time': 'ORDERTIME', 'id': 'ORDERNO'}

    def to_list(self):
        data = self.source.get_orders(select=self.select_arg, where=self.where_arg, group_by=self.groupby,
                                      order_by=self.orderby, make_df=False)
        return [Trade(row) for row in data]

    def to_frame(self):
        dataframe = self.source.get_orders(select=self.select_arg, where=self.where_arg, group_by=self.groupby,
                                           order_by=self.orderby, make_df=True)
        return dataframe

    def to_enumerable(self):
        data = self.source.get_orders(select=self.select_arg, where=self.where_arg, group_by=self.groupby,
                                      order_by=self.orderby, make_df=False)
        return Enumerable(data)


class EventsData(BaseClassData):

    def __init__(self, source):
        super(EventsData, self).__init__(source)
        self.source = source
        self.mapping = {'type': 'EVTYPE', 'date': 'EVDATE', 'time': 'EVTIME', 'orderid': 'ORDERNO',
                        'tradeid': 'TRADENO', 'trade': 2, 'order': 1, 'withdraws': 3, 'alltrades': 12, 'timeevents': 14}

    def where(self, **kwargs):
        if 'type' in kwargs.keys():
            kwargs['evtype'] = self.mapping[kwargs.pop('type')]
        self.where_arg = where(source=self.source, mapping=self.mapping, **kwargs).upper()
        return self

    def to_list(self):
        data = self.source.get_events(select=self.select_arg, where=self.where_arg, group_by=self.groupby,
                                      order_by=self.orderby, make_df=False)
        return [Trade(row) for row in data]

    def to_frame(self):
        dataframe = self.source.get_events(select=self.select_arg, where=self.where_arg, group_by=self.groupby,
                                           order_by=self.orderby, make_df=True)
        return dataframe

    def to_enumerable(self):
        data = self.source.get_events(select=self.select_arg, where=self.where_arg, group_by=self.groupby,
                                      order_by=self.orderby, make_df=False)
        return Enumerable(data)
