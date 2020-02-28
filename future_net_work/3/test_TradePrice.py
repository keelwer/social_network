from Events.markets import Market

def test_TradePrice(db):
    db.set_market(Market.CUR)
    trades = db.get_trades().where(task=39).order_by('id').to_list()
    signals = db.get_signals().where(task=39).order_by('id').to_list()
    assert (len(trades) == len(signals))
    for index, trade in enumerate(trades):
        len(trades)
        assert (float(trade.price) == float(signals[index].message))

