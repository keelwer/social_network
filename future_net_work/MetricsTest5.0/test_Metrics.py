import time


def test_TradePrice(db, task):
    db.set_market('CUR')
    trades = db.get_trades(task=task)
    signals = db.get_signals(task=task)
    for trade in trades:
        assert (float(trade.price) == float(list(filter(lambda signal: signal.tradeid == trade.tradeid, signals))[0].message))


def test_client_instr(db, task):
    '''Метрика Инстр:ЦенаСредневзвешеннаяПарам() с МС Сделка - Фондовый рынок'''
    tradeEvno_ = db.get_events(task=task)
    for trade in


    tradeEvno = str(additional_functions.get_events(make_db_engine=make_db_engine, top='top (1)', columns=['evno'], evdate='02.12.2019',
                                       evtype='2', tradeno='4050634109'))
    maxEvno = str(additional_functions.get_events(make_db_engine=make_db_engine, columns=['max(evno)'], inequality_condition=[f'evno<{tradeEvno}'],
                                     evdate='02.12.2019', evtype='12'))
    secboard = str(additional_functions.get_trades(make_db_engine=make_db_engine, top='top (1)', columns=['secboard'], evdate='02.12.2019',
                                      tradeno='352303634'))
    seccode = str(additional_functions.get_trades(make_db_engine=make_db_engine, top='top (1)', columns=['seccode'], evdate='02.12.2019',
                                     tradeno='352303634'))
    metric_result = str(additional_functions.get_all_trades(make_db_engine=make_db_engine, columns=['sum(QUANTITY * PRICE)/sum(QUANTITY)'],
                                               inequality_condition=[f'ID <= {maxEvno}'], evdate='02.12.2019',
                                               secboard=secboard, seccode=seccode))
    message_in_signals = str(additional_functions.get_custom_signals(make_db_engine=make_db_engine, columns=['message'], taskid='126', criteriaid='93',
                                                        tsno='4050634109'))
    assert (metric_result == message_in_signals)





    request = '''
    declare @tsno decimal(38,0);
declare @evdate decimal(38,0);
set @evdate = 20191202;
set @tsno = 4050634109;

declare @tradeEvno decimal(38,0);
set @tradeEvno =
(select top (1) evno
from [Check4Trick.Aton.Dev.HistoryEQ].[dbo].[FRC_EVENTS]
where EVTYPE = 2 and evdate = @evdate and TRADENO = @tsno);

declare @maxevno decimal(38,0);
set @maxevno =
(select max(evno)
from [Check4Trick.Aton.Dev.HistoryEQ].[dbo].[FRC_EVENTS]
where evtype = 12 and evdate = @evdate and evno < @tradeEvno);

select sum(QUANTITY * PRICE)/sum(QUANTITY)
from [Check4Trick.Aton.Dev.HistoryEQ].[dbo].[FRC_ALL_TRADES]
where evdate = @evdate and ID <= @maxevno
and SECBOARD = (select top (1) secboard from [Check4Trick.Aton.Dev.HistoryEQ].[dbo].[FRC_TRADES] where TRADENO = @tsno and EVDATE = @evdate)
and SECCODE = (select top (1) seccode from [Check4Trick.Aton.Dev.HistoryEQ].[dbo].[FRC_TRADES] where TRADENO = @tsno and EVDATE = @evdate);
    '''
    # condition_for_message = '''
    # TASKID = 126 and CRITERIAID = 93 and TSNO = 4050634109
    # '''
    # inst = Metrics.MetricsTest(instance_dir=instance_dir, market='EQ')
    # price = float(inst.execute_request(request=request, schema='history'))
    # price_in_message = float(inst.get_custom_signals(columns=['message'], where=condition_for_message))
    # assert (price == price_in_message)
