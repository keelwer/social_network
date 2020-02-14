import time


def test_TradePrice(db, task):
    db.set_market('CUR')
    trades = db.get_trades(task=task)
    signals = db.get_signals(task=task)
    for trade in trades:
        assert (float(trade.price) == float(list(filter(lambda signal: signal.tradeid == trade.tradeid, signals))[0].message))


# def test_client_instr(make_db_engine):
#     '''Метрика Инстр:ЦенаСредневзвешеннаяПарам() с МС Сделка - Фондовый рынок'''
#     tradeEvno = str(additional_functions.get_events(make_db_engine=make_db_engine, top='top (1)', columns=['evno'], evdate='02.12.2019',
#                                        evtype='2', tradeno='4050634109'))
#     maxEvno = str(additional_functions.get_events(make_db_engine=make_db_engine, columns=['max(evno)'], inequality_condition=[f'evno<{tradeEvno}'],
#                                      evdate='02.12.2019', evtype='12'))
#     secboard = str(additional_functions.get_trades(make_db_engine=make_db_engine, top='top (1)', columns=['secboard'], evdate='02.12.2019',
#                                       tradeno='352303634'))
#     seccode = str(additional_functions.get_trades(make_db_engine=make_db_engine, top='top (1)', columns=['seccode'], evdate='02.12.2019',
#                                      tradeno='352303634'))
#     metric_result = str(additional_functions.get_all_trades(make_db_engine=make_db_engine, columns=['sum(QUANTITY * PRICE)/sum(QUANTITY)'],
#                                                inequality_condition=[f'ID <= {maxEvno}'], evdate='02.12.2019',
#                                                secboard=secboard, seccode=seccode))
#     message_in_signals = str(additional_functions.get_custom_signals(make_db_engine=make_db_engine, columns=['message'], taskid='126', criteriaid='93',
#                                                         tsno='4050634109'))
#     assert (metric_result == message_in_signals)
