import Metrics


def test_trade_price():
    engine = str()
    price = str(Metrics.get_trades(engine=engine, columns=['price'], date='02.12.2019', trade='352303634'))
    message_in_signals = str(Metrics.get_custom_signals(engine=engine, columns=['message'], task='39', criteria='71',
                                                        tsno='352303634'))
    assert (price == message_in_signals)


def test_client_instr():
    '''Метрика Инстр:ЦенаСредневзвешеннаяПарам() с МС Сделка - Фондовый рынок'''
    engine = str()
    tradeEvno = str(Metrics.get_events(engine=engine, top='top (1)', columns=['evno'], date='02.12.2019',
                                       event_type='2', trade='4050634109'))
    maxEvno = str(Metrics.get_events(engine=engine, columns=['max(evno)'], inequality_condition=f'evno < {tradeEvno}',
                                     date='02.12.2019', event_type='12'))
    secboard = str(Metrics.get_trades(engine=engine, top='top (1)', columns=['secboard'], date='02.12.2019',
                                      trade='352303634'))
    seccode = str(Metrics.get_trades(engine=engine, top='top (1)', columns=['seccode'], date='02.12.2019',
                                     trade='352303634'))
    metric_result = str(Metrics.get_all_trades(engine=engine, columns=['sum(QUANTITY * PRICE)/sum(QUANTITY)'],
                                               inequality_condition=f'ID <= {maxEvno}', date='02.12.2019',
                                               secboard=secboard, seccode=seccode))
    message_in_signals = str(Metrics.get_custom_signals(engine=engine, columns=['message'], task='126', criteria='93',
                                                        tsno='4050634109'))
    assert (metric_result == message_in_signals)
