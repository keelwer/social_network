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


class Market:

    def __init__(self, market):
        self.market = market

    def __str__(self):
        return str(self.market).lower()