from .Repo import Repo
import pandas
from Events.EventTypes import Task, Trade, Signal, AllTrades, Orders, Events
from Events.markets import MarketInit



class DbRepo(Repo):
    def __init__(self, connection):
        super(DbRepo, self).__init__()
        self.connection = connection
        self.market = None

    def get_data(self, select, table, where, group_by, order_by, schema):
        query = f'SELECT {select} FROM {table}{where} {group_by} {order_by}'
        result = self.connection[f'{schema}_{self.market.lower()}'].execute(query)
        return result

    def get_markets(self):
        markets = []
        query = '''SELECT TYPE FROM FRC_MARKETS'''
        result = self.execute(schema='metadata', query=query)
        for row in result:
            markets.append(row[0])
        markets = [MarketInit(market) for market in markets]
        return markets

    def set_market(self, market):
        self.market = market

    def __make_dataframe(self, output_request):
        df = pandas.DataFrame(output_request.fetchall())
        df.columns = output_request.keys()
        df.columns = df.columns.str.lower()
        return df

    def get_task(self, id):
        request_get_task = f'SELECT * FROM FRC_TASKS where TASKID = {id}'
        result_custom_signals = self.connection[f'client_{str(self.market).lower()}'].execute(request_get_task)
        data = [dict(row) for row in result_custom_signals]
        task = Task(data[0])
        return task

    def get_trades(self, select, where, group_by, order_by, make_df=False):
        if make_df:
            data = self.__make_dataframe(self.get_data(select=select, table='FRC_TRADES', where=where, group_by=group_by, order_by=order_by, schema='history'))
        else:
            result_query = self.get_data(select=select, table='FRC_TRADES', where=where, group_by=group_by, order_by=order_by, schema='history')
            data = [dict(row) for row in result_query]
        return data

    def get_signals(self, select, where, group_by, order_by, make_df=False):
        if make_df:
            data = self.__make_dataframe(self.get_data(select=select, table='FRC_CUSTOMSIGNALS', where=where, group_by=group_by, order_by=order_by, schema='client'))
        else:
            result_query = self.get_data(select=select, table='FRC_CUSTOMSIGNALS', where=where, group_by=group_by, order_by=order_by, schema='client')
            data = [dict(row) for row in result_query]
        return data

    def get_all_trades(self, select, where, group_by, order_by, make_df=False):
        if make_df:
            data = self.__make_dataframe(self.get_data(select=select, table='FRC_ALL_TRADES', where=where, group_by=group_by, order_by=order_by, schema='history'))
        else:
            result_query = self.get_data(select=select, table='FRC_ALL_TRADES', where=where, group_by=group_by, order_by=order_by, schema='history')
            data = [dict(row) for row in result_query]
        return data

    def get_orders(self, select, where, group_by, order_by, make_df=False):
        if make_df:
            data = self.__make_dataframe(self.get_data(select=select, table='FRC_ORDERS', where=where, group_by=group_by, order_by=order_by, schema='history'))
        else:
            result_query = self.get_data(select=select, table='FRC_ORDERS', where=where, group_by=group_by, order_by=order_by, schema='history')
            data = [dict(row) for row in result_query]
        return data


    def get_events(self, select, where, group_by, order_by, make_df=False):
        if make_df:
            data = self.__make_dataframe(self.get_data(select=select, table='FRC_EVENTS', where=where, group_by=group_by, order_by=order_by, schema='history'))
        else:
            result_query = self.get_data(select=select, table='FRC_EVENTS', where=where, group_by=group_by, order_by=order_by, schema='history')
            data = [dict(row) for row in result_query]
        return data

    def execute(self, schema, query):
        if schema.lower() == 'metadata':
            query_request = self.connection[f'metadata'].execute(query)
        else:
            query_request = self.connection[f'{schema.lower()}_{self.market.lower()}'].execute(query)
        df = self.__make_dataframe(query_request)
        return df


