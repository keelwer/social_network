from datetime import datetime, date, time

mapping_field = {
    'date': 'EVDATE',
    'trade': 'TRADENO',
    'event': 'evno',
    'task': 'TASKID',
    'criteria': 'CRITERIAID',
    'tsno': 'TSNO',
    'event_type': 'EVTYPE',
    'price': 'price',
    'message': 'message',
    'secboard': 'SECBOARD',
    'seccode': 'SECCODE',
    'id': 'ID',
}


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
        condition += f' {mapping_field[field]}={value}'
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
def get_trades(engine, top='', columns=[], inequality_condition='', order_by='', **kwargs):
    '''
    :param date:
    :param trade:
    '''
    if 'date' in kwargs.keys():
        kwargs['date'] = datetime.strptime(kwargs['date'], "%d.%m.%Y").strftime("%Y%m%d")
    request_trades = f'SELECT {top} {get_columns(columns)} FROM FRC_TRADES ' \
                     f'{condition(inequality_condition=inequality_condition, **kwargs)} {order_by}'
    result_trades = engine.execute(request_trades).fetchall()
    return result_trades


@check_output_quantity
def get_custom_signals(engine, top='', columns=[], inequality_condition='', order_by='', **kwargs):
    '''
    :param task:
    :param criteria:
    :param tsno:
    '''
    request_custom_signals = f'SELECT {top} {get_columns(columns)} FROM FRC_CUSTOMSIGNALS ' \
                             f'{condition(inequality_condition=inequality_condition, **kwargs)} {order_by}'
    result_custom_signals = engine.execute(request_custom_signals).fetchall()
    return result_custom_signals


@check_output_quantity
def get_all_trades(engine, top='', columns=[], inequality_condition='', order_by='', **kwargs):
    request_all_trades = f'SELECT {top} {get_columns(columns)} FROM FRC_ALL_TRADES ' \
                         f'{condition(inequality_condition=inequality_condition, **kwargs)} {order_by}'
    result_all_trades = engine.execute(request_all_trades).fetchall()
    return result_all_trades


@check_output_quantity
def get_orders(engine, top='', columns=[], inequality_condition='', order_by='', **kwargs):
    if 'date' in kwargs.keys():
        kwargs['date'] = datetime.strptime(kwargs['date'], "%d.%m.%Y").strftime("%Y%m%d")
    request_orders = f'SELECT {top} {get_columns(columns)} FROM FRC_ORDERS ' \
                     f'{condition(inequality_condition=inequality_condition, **kwargs)} {order_by}'
    result_orders = engine.execute(request_orders).fetchall()
    return result_orders


@check_output_quantity
def get_events(engine, top='', columns=[], inequality_condition='', order_by='', **kwargs):
    '''
    :param date:
    :param event:
    :param trade:
    :param event_type:
    '''
    if 'date' in kwargs.keys():
        kwargs['date'] = datetime.strptime(kwargs['date'], "%d.%m.%Y").strftime("%Y%m%d")
    request_orders = f'SELECT {top} {get_columns(columns)} FROM FRC_EVENTS ' \
                     f'{condition(inequality_condition=inequality_condition, **kwargs)} {order_by}'
    result_orders = engine.execute(request_orders).fetchall()
    return result_orders


@check_output_quantity
def execute_request(engine, request):
    result = engine.execute(request).fetchall()
    return result
