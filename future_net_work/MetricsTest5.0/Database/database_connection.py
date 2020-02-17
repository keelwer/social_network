from datetime import datetime
import sqlalchemy


class DbConnection:

    def __init__(self, connect_params):
        self.connect_params = connect_params

    def create_connstr_meta(self, params):
        if params['database']['provider'] == 'mssql':
            type_instance = ''
            if params['instance'].get("type"):
                type_instance = f".{params['instance'].get('type')}"
            conn_string = f"mssql+pyodbc://{params['instance']['login']}:{params['instance']['password']}@{params['database']['server']}:1433/{params['instance']['name']}{type_instance}.ClientMetadata?driver=SQL+Server+Native+Client+11.0"
        return conn_string

    def create_connstr_client_history(self, params, schema, market):
        if params['database']['provider'] == 'mssql':
            type_instance = ''
            if params['instance'].get("type"):
                type_instance = f".{params['instance'].get('type')}"
            schema = f'.{schema}'
            market = f'{market}'
            conn_string = f"mssql+pyodbc://{params['instance']['login']}:{params['instance']['password']}@{params['database']['server']}:1433/{params['instance']['name']}{type_instance}{schema}{market}?driver=SQL+Server+Native+Client+11.0"
        return conn_string

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

    def get_markets(self):
        markets = []
        get_market_request = '''SELECT TYPE FROM FRC_MARKETS'''
        engine = sqlalchemy.create_engine(self.create_connstr_meta(self.connect_params))
        result_trades = engine.execute(get_market_request)
        for row in result_trades:
            markets.append(row[0])
        return markets

    def create_engine(self, connect_params=None, schema=None, market=None):
        if connect_params:
            sqlalchemy.create_engine(self.create_connstr_meta(connect_params))
        else:
            engine = sqlalchemy.create_engine(self.create_connstr_client_history(self.connect_params, schema, market))
        return engine

    def get_data(self, date, market, table, schema, **kwargs):
        kwargs['EVDATE'] = date
        request = f'SELECT * FROM {table} {self.condition_for_request(**kwargs)}'
        result = self.create_engine(market=market, schema=schema).execute(request)
        return result
