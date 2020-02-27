from Events.EventTypes import Market

def test_TradePrice(db):
    db.set_market(Market('cur'))
    # trades = db.get_trades(task=39).order_by(('tradeno',))
    trades = db.get_trades(task=39).order_by(('tradeno',))
    # trades1 = trades.order_by(('tradeno',))

    # trades = trades.order_by(('tradeid',))
    signals = db.get_signals(task=39)
    # trades.sort(key=lambda trade: trade.tradeid, reverse=False)
    # signals.sort(key=lambda signals: signals.tradeid, reverse=False)
    # assert (len(trades) == len(signals))
    for index, trade in enumerate(trades):
        len(trades1)
        assert (float(trade.price) == float(signals[index].message))

