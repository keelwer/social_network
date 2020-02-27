def test_PricePenultimateTrade(db, task):
    db.set_market('cur')
    signals = db.get_signals(task=task)
    starttime = db.get_task(task).starttime
    endtime = db.get_task(task).endtime
    query = f'''select tradeno, secboard, seccode, tradetype, price from frc_trades where evdate between {starttime} and {endtime} order by tradeno desc'''
    df = db.execute(schema='history', query=query)
    for signal in signals:
        maxtradeno = df[
            (df.tradeno < signal.tradeid) & (~df.tradetype.isin(['H', 'h', 'G'])) & (df.seccode == signal.seccode) & (
                    df.secboard == signal.secboard)][['tradeno']].max()
        if str(maxtradeno['tradeno']) == 'nan':
            continue
        price = df[(df.secboard == signal.secboard) & (df.seccode == signal.seccode) & (df.tradeno == maxtradeno['tradeno']) & (
            ~df.tradetype.isin(['H', 'h', 'G']))]['price'].values
        assert (float(signal.price) == float(price))