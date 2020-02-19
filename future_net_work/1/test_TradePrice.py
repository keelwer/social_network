def test_TradePrice(db, task):
    db.set_market('cur')
    trades = db.get_trades(task=task)
    signals = db.get_signals(task=task)
    trades.sort(key=lambda trade: trade.tradeid, reverse=False)
    signals.sort(key=lambda signals: signals.tradeid, reverse=False)
    assert (len(trades) == len(signals))
    for index, trade in enumerate(trades):
        assert (float(trade.price) == float(signals[index].message))
