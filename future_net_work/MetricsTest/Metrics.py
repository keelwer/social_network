from EventMonitoringDeploy import monitoring_instance


def get_columns(columns_put):
    columns = '*'
    if columns_put:
        columns = ''
        for column in columns_put:
            columns += f' {column}'
    return columns


def condition(where):
    condition = ''
    if where:
        condition = f' where {where}'
    return condition


class MetricsTest:
    def __init__(self, instance_dir: str, market):
        self.instance_dir = instance_dir
        self.market = market

    def instance(self):
        instance = monitoring_instance.MonitoringInstance(instance_dir=self.instance_dir)
        return instance

    def _check_output_quantity(func):
        def check(self, *args, **kwargs):
            output_data = func(self, *args, **kwargs)
            if len(output_data) == 1:
                output_data = output_data[0][0]
            return output_data

        return check

    @_check_output_quantity
    def get_trades(self, columns=[], where=None):
        request_trades = f'SELECT {get_columns(columns)} FROM FRC_TRADES {condition(where=where)}'
        result_trades = self.engine_sql('history').execute(request_trades).fetchall()
        return result_trades

    @_check_output_quantity
    def get_all_trades(self, columns=[], where=None):
        request_all_trades = f'SELECT {get_columns(columns)} FROM FRC_ALL_TRADES {condition(where=where)}'
        result_all_trades = self.engine_sql('history').execute(request_all_trades).fetchall()
        return result_all_trades

    @_check_output_quantity
    def get_custom_signals(self, columns=[], where=None):
        request_custom_signals = f'SELECT {get_columns(columns)} FROM FRC_CUSTOMSIGNALS {condition(where=where)}'
        result_custom_signals = self.engine_sql('client').execute(request_custom_signals).fetchall()
        return result_custom_signals

    @_check_output_quantity
    def get_orders(self, columns=[], where=None):
        request_orders = f'SELECT {get_columns(columns)} FROM FRC_ORDERS {condition(where=where)}'
        result_orders = self.engine_sql('history').execute(request_orders).fetchall()
        return result_orders

    def engine_sql(self, schema):
        req_schema = ''
        if schema == 'history':
            req_schema = f'history_{self.market.lower()}'
        elif schema == 'client':
            req_schema = f'client_{self.market.lower()}'
        engine = self.instance().get_connections()[req_schema]
        return engine

    @_check_output_quantity
    def execute_request(self, request, schema):
        result = self.engine_sql(schema).execute(request).fetchall()
        return result
