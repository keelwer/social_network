from datetime import datetime, date, time
from pandas import DataFrame


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


def make_dataframe(output_request):
    df = DataFrame(output_request.fetchall())
    df.columns = output_request.keys()
    return df


def get_trades(db, **kwargs):
    if 'evdate' in kwargs.keys():
        kwargs['evdate'] = datetime.strptime(kwargs['evdate'], "%d.%m.%Y").strftime("%Y%m%d")
    request_trades = f'SELECT * FROM FRC_TRADES {condition(**kwargs)}'
    result_trades = db('History').execute(request_trades)
    return make_dataframe(result_trades)



def get_custom_signals(db, **kwargs):
    request_custom_signals = f'SELECT * FROM FRC_CUSTOMSIGNALS {condition(**kwargs)}'
    result_custom_signals = db('Client').execute(request_custom_signals)
    return make_dataframe(result_custom_signals)



def get_all_trades(db, **kwargs):
    request_all_trades = f'SELECT * FROM FRC_ALL_TRADES {condition(**kwargs)}'
    result_all_trades = db('History').execute(request_all_trades)
    return make_dataframe(result_all_trades)


def get_orders(db, **kwargs):
    if 'evdate' in kwargs.keys():
        kwargs['evdate'] = datetime.strptime(kwargs['evdate'], "%d.%m.%Y").strftime("%Y%m%d")
    request_orders = f'SELECT * FROM FRC_ORDERS {condition(**kwargs)}'
    result_orders = db('History').execute(request_orders)
    return make_dataframe(result_orders)


def get_events(db, **kwargs):
    if 'evdate' in kwargs.keys():
        kwargs['evdate'] = datetime.strptime(kwargs['evdate'], "%d.%m.%Y").strftime("%Y%m%d")
    request_events = f'SELECT * FROM FRC_EVENTS {condition(**kwargs)}'
    result_events = db('History').execute(request_events)
    return make_dataframe(result_events)


def execute_custom_request(db, schema, request):
    custom_request = request
    results = db(schema).execute(custom_request)
    return make_dataframe(results)