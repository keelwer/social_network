import Metrics


def test_trade_price():
    engine = str()
    price = str(Metrics.get_trades(columns=['price'], evdate='02.12.2019', tradeno='352303634'))
    message_in_signals = str(Metrics.get_custom_signals(engine=engine, columns=['message'], taskid='39', criteriaid='71',
                                                        tsno='352303634'))
    assert (price == message_in_signals)


def test_client_instr():
    '''Метрика Инстр:ЦенаСредневзвешеннаяПарам() с МС Сделка - Фондовый рынок'''
    engine = str()
    tradeEvno = str(Metrics.get_events(top='top (1)', columns=['evno'], evdate='02.12.2019',
                                       evtype='2', tradeno='4050634109'))
    maxEvno = str(Metrics.get_events(columns=['max(evno)'], inequality_condition=f'evno < {tradeEvno}',
                                     evdate='02.12.2019', evtype='12'))
    secboard = str(Metrics.get_trades(top='top (1)', columns=['secboard'], evdate='02.12.2019',
                                      tradeno='352303634'))
    seccode = str(Metrics.get_trades(top='top (1)', columns=['seccode'], evdate='02.12.2019',
                                     tradeno='352303634'))
    metric_result = str(Metrics.get_all_trades(columns=['sum(QUANTITY * PRICE)/sum(QUANTITY)'],
                                               inequality_condition=f'ID <= {maxEvno}', evdate='02.12.2019',
                                               secboard=secboard, seccode=seccode))
    message_in_signals = str(Metrics.get_custom_signals(columns=['message'], taskid='126', criteriaid='93',
                                                        tsno='4050634109'))
    assert (metric_result == message_in_signals)
