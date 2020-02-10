import Metrics

instance_dir = r'D:\check'

def test_trade_price():
    condition_for_trades = '''
    EVDATE = 20191202 and TRADENO = 352303634
    '''
    condition_for_message = '''
    TASKID = 39 and CRITERIAID = 71 and TSNO = 352303634
    '''
    inst = Metrics.MetricsTest(instance_dir=instance_dir, market='CUR')
    price = float(inst.get_trades(columns=['price'], where=condition_for_trades))
    price_in_message = float(inst.get_custom_signals(columns=['message'], where=condition_for_message))
    assert (price == price_in_message)


# def test_client_instr():
#     '''Метрика Инстр:ЦенаСредневзвешеннаяПарам() с МС Сделка - Фондовый рынок'''
#     request = '''
#     declare @tsno decimal(38,0);
# declare @evdate decimal(38,0);
# set @evdate = 20191202;
# set @tsno = 4050634109;
#
# declare @tradeEvno decimal(38,0);
# set @tradeEvno =
# (select top (1) evno
# from [Check4Trick.Aton.Dev.HistoryEQ].[dbo].[FRC_EVENTS]
# where EVTYPE = 2 and evdate = @evdate and TRADENO = @tsno);
#
# declare @maxevno decimal(38,0);
# set @maxevno =
# (select max(evno)
# from [Check4Trick.Aton.Dev.HistoryEQ].[dbo].[FRC_EVENTS]
# where evtype = 12 and evdate = @evdate and evno < @tradeEvno);
#
# select sum(QUANTITY * PRICE)/sum(QUANTITY)
# from [Check4Trick.Aton.Dev.HistoryEQ].[dbo].[FRC_ALL_TRADES]
# where evdate = @evdate and ID <= @maxevno
# and SECBOARD = (select top (1) secboard from [Check4Trick.Aton.Dev.HistoryEQ].[dbo].[FRC_TRADES] where TRADENO = @tsno and EVDATE = @evdate)
# and SECCODE = (select top (1) seccode from [Check4Trick.Aton.Dev.HistoryEQ].[dbo].[FRC_TRADES] where TRADENO = @tsno and EVDATE = @evdate);
#     '''
#     condition_for_message = '''
#     TASKID = 126 and CRITERIAID = 93 and TSNO = 4050634109
#     '''
#     inst = Metrics.MetricsTest(instance_dir=instance_dir, market='EQ')
#     price = float(inst.execute_request(request=request, schema='history'))
#     price_in_message = float(inst.get_custom_signals(columns=['message'], where=condition_for_message))
#     assert (price == price_in_message)
