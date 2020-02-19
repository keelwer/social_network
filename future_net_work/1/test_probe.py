def test_client_instr(db):
    db.set_market('EQ')
    '''Метрика Инстр:ЦенаСредневзвешеннаяПарам() с МС Сделка - Фондовый рынок'''
    signals = db.get_signals(task=114)
    events_trades = db.get_events(task=114, type='trade')
    events_alltrades = db.get_events(task=114, type='alltrades')
    trades = db.get_trades(task=114)
    all_trades = db.get_all_trades(task=114)
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
        assert (signal.message == result)