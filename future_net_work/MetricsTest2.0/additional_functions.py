import pytest

@pytest.fixture(scope="module")
def db(schema):
    config = configparser.ConfigParser()
    config.read('Config.ini')
    conn_string = f"mssql+pyodbc://{config['Default']['login']}:{config['Default']['password']}@{config['Default']['server']}:1433/{config['Default']['instance']}.{schema}{config['Default']['market']}?driver=SQL+Server+Native+Client+11.0"
    engine = sqlalchemy.create_engine(conn_string)
    return engine

#добавить фикстуру get_markets
# добавить параметр ввода рынка



@pytest.fixture(autouse=True)
class MetricTest:

    # def __init__(self, market=None):
    #     self.market = market
    #
    #
    # def get_markets(self):
    #     if not self.market:
    #         print('connect and get markets')
    #         # connect to db

    def make_dataframe(self, output_request):
        df = DataFrame(output_request.fetchall())
        df.columns = output_request.keys()
        df.columns = df.columns.str.lower()
        return df

    def get_trades(self, db, **kwargs):
        if 'date' in kwargs.keys():
            kwargs['evdate'] = datetime.strptime(kwargs.pop('date'), "%d.%m.%Y").strftime("%Y%m%d")
        request_trades = f'SELECT * FROM FRC_TRADES {condition(**kwargs)}'
        result_trades = db('History').execute(request_trades)
        df = make_dataframe(result_trades)
        df.rename(columns={'tsno':'trade'}, inplace=True)
        return df

    def get_signals(self, db, **kwargs):
        request_custom_signals = f'SELECT * FROM FRC_CUSTOMSIGNALS {condition(**kwargs)}'
        result_custom_signals = db('Client').execute(request_custom_signals)
        df = make_dataframe(result_custom_signals)
        df.rename(columns={'tsno':'trade'}, inplace=True)
        return df

    def get_all_trades(self, db, **kwargs):
        if 'date' in kwargs.keys():
            kwargs['evdate'] = datetime.strptime(kwargs.pop('date'), "%d.%m.%Y").strftime("%Y%m%d")
        request_all_trades = f'SELECT * FROM FRC_ALL_TRADES {condition(**kwargs)}'
        result_all_trades = db('History').execute(request_all_trades)
        return make_dataframe(result_all_trades)

    def get_orders(self, db, **kwargs):
        if 'date' in kwargs.keys():
            kwargs['evdate'] = datetime.strptime(kwargs.pop('date'), "%d.%m.%Y").strftime("%Y%m%d")
        request_orders = f'SELECT * FROM FRC_ORDERS {condition(**kwargs)}'
        result_orders = db('History').execute(request_orders)
        return make_dataframe(result_orders)

    def get_events(self, db, **kwargs):
        # добавить типы событий
        mapping_type = {'trade': 2, 'order': 12}
        if 'type' in kwargs.keys():
            kwargs['evtype'] = mapping_type[kwargs.pop('type')]
        if 'date' in kwargs.keys():
            kwargs['evdate'] = datetime.strptime(kwargs.pop('date'), "%d.%m.%Y").strftime("%Y%m%d")
        request_events = f'SELECT * FROM FRC_EVENTS {condition(**kwargs)}'
        result_events = db('History').execute(request_events)
        return make_dataframe(result_events)

    def execute_custom_request(self, db, schema, request):
        custom_request = request
        results = db(schema).execute(custom_request)
        return make_dataframe(results)


class Trades:

    def __init__(self, df):
        self.df = df

