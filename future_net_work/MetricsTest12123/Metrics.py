from datetime import datetime, date, time

def get_columns(columns_put):
    columns = '*'
    if columns_put:
        columns = ''
        for column in columns_put:
            columns += f' {column}'
    return columns


def condition(inequality_condition='', **kargs):
    condition = f'where {inequality_condition}'
    for field, value in kargs.items():
        condition += f' {field}={value}'
    condition_list = condition.split()
    result_condition = condition_list.copy()[:2]
    for condition_parameter in condition_list[2:]:
        condition_parameter = f'and {condition_parameter}'
        result_condition.append(condition_parameter)
    condition = ' '.join(result_condition)
    return condition


def check_output_quantity(func):
    def check(*args, **kwargs):
        output_data = func(*args, **kwargs)
        if len(output_data) == 1:
            output_data = output_data[0][0]
        return output_data

    return check


@check_output_quantity
def get_trades(make_db_engine, top='', columns=[], inequality_condition='', order_by='', **kwargs):
    if 'evdate' in kwargs.keys():
        kwargs['evdate'] = datetime.strptime(kwargs['date'], "%d.%m.%Y").strftime("%Y%m%d")
    request_trades = f'SELECT {top} {get_columns(columns)} FROM FRC_TRADES ' \
                     f'{condition(inequality_condition=inequality_condition, **kwargs)} {order_by}'
    result_trades = make_db_engine('History').execute(request_trades).fetchall()
    return result_trades


@check_output_quantity
def get_custom_signals(make_db_engine, top='', columns=[], inequality_condition='', order_by='', **kwargs):
    request_custom_signals = f'SELECT {top} {get_columns(columns)} FROM FRC_CUSTOMSIGNALS ' \
                             f'{condition(inequality_condition=inequality_condition, **kwargs)} {order_by}'
    result_custom_signals = make_db_engine('Client').execute(request_custom_signals).fetchall()
    return result_custom_signals


@check_output_quantity
def get_all_trades(make_db_engine, top='', columns=[], inequality_condition='', order_by='', **kwargs):
    request_all_trades = f'SELECT {top} {get_columns(columns)} FROM FRC_ALL_TRADES ' \
                         f'{condition(inequality_condition=inequality_condition, **kwargs)} {order_by}'
    result_all_trades = make_db_engine('History').execute(request_all_trades).fetchall()
    return result_all_trades


@check_output_quantity
def get_orders(make_db_engine, top='', columns=[], inequality_condition='', order_by='', **kwargs):
    if 'evdate' in kwargs.keys():
        kwargs['evdate'] = datetime.strptime(kwargs['date'], "%d.%m.%Y").strftime("%Y%m%d")
    request_orders = f'SELECT {top} {get_columns(columns)} FROM FRC_ORDERS ' \
                     f'{condition(inequality_condition=inequality_condition, **kwargs)} {order_by}'
    result_orders = make_db_engine('History').execute(request_orders).fetchall()
    return result_orders


@check_output_quantity
def get_events(make_db_engine, top='', columns=[], inequality_condition='', order_by='', **kwargs):
    if 'evdate' in kwargs.keys():
        kwargs['evdate'] = datetime.strptime(kwargs['date'], "%d.%m.%Y").strftime("%Y%m%d")
    request_orders = f'SELECT {top} {get_columns(columns)} FROM FRC_EVENTS ' \
                     f'{condition(inequality_condition=inequality_condition, **kwargs)} {order_by}'
    result_orders = make_db_engine('History').execute(request_orders).fetchall()
    return result_orders


@check_output_quantity
def execute_request(make_db_engine, schema, request):
    result = make_db_engine(schema).execute(request).fetchall()
    return result
