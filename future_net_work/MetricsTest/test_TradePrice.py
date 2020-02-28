from Events.markets import Market

def test_TradePrice(db):
    db.set_market(Market.CUR)
    trades = db.get_trades().where(task=39).order_by('id',).group_by('id', 'price').to_list()
    signals = db.get_signals().where(task=39).order_by('tradeid',).to_list()
    assert (len(trades) == len(signals))
    for signal, trade in zip(signals, trades):
        assert(float(signal.message) == float(trade.price))

