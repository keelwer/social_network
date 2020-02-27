from Events.EventTypes import Market


def test_PriceMiddleParametric(db, task):
    db.set_market(Market('eq'))
    '''Метрика Инстр:ЦенаСредневзвешеннаяПарам() с МС Сделка - Фондовый рынок'''
    signals = db.get_signals(task=task)
    events_trades = db.get_events(task=task, type='trade')
    events_alltrades = db.get_events(task=task, type='alltrades')
    trades = db.get_trades(task=task)
    all_trades = db.get_all_trades(task=task)
    tradeevno_tradeid = {event.tradeid: event.evno for event in events_trades}
    secboard_tradeid = dict()
    seccode_tradeid = dict()
    for trade in trades:
        secboard_tradeid[trade.tradeid] = trade.secboard
        seccode_tradeid[trade.tradeid] = trade.seccode
    for signal in signals:
        maxEvno = max(list(filter(lambda event: event.evno < tradeevno_tradeid[signal.tradeid], events_alltrades)), key=lambda event: event.evno).evno
        filter_trades = list(filter(lambda anon_trade: anon_trade.id <= maxEvno and anon_trade.secboard == secboard_tradeid[signal.tradeid] and anon_trade.seccode == seccode_tradeid[signal.tradeid], all_trades))
        result = sum(float(trades.price) * float(trades.quantity) for trades in filter_trades) / sum(float(trades.quantity) for trades in filter_trades)
        assert (float(signal.message) == result)