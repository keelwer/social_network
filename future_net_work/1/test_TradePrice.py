Инстр:ЦенаПредпослСделки
def test_TradePrice(db, task):
    db.set_market('cur')
    signals = db.get_signals(task=task)
    date = db.get_task(task)[0].date
    query = f'''select tradeno, secboard, seccode, price from frc_trades where evdate = {date} order by tradeno desc'''
    df = db.execute(schema='history', query=query)
    for signal in signals:
        maxtradeno = df[
            (df.tradeno < signal.tradeid) & (~df.tradetype.isin(['H', 'h', 'G'])) & (df.seccode == signal.seccode) & (
                    df.secboard == signal.secboard)][['tradeno']].max()
        price = df[(df.secboard == signal.secboard) & (df.seccode == signal.seccode) & (df.tradeno == maxtradeno) & (
            ~df.tradetype.isin(['H', 'h', 'G']))][['price']]
        assert (signal.price == price)

    '''КлиентИнстр:ОбъемСделокИсторическая
    select SECBOARD, SECCODE, FIRMCODE, SPECCODE, sum(qty_all) as qty
    from [Check4Trick.Aton.QA.HistoryEQ].[dbo].[FRC_HIST_SPECSEC]
    where RECDATE in
    (
    select max(RECDATE)
    from [Check4Trick.Aton.QA.HistoryEQ].[dbo].[FRC_HIST_SPECSEC]
    where RECDATE < 20191204
    )
    group by SECBOARD, SECCODE, FIRMCODE, SPECCODE
    order by SECBOARD, SECCODE, FIRMCODE, SPECCODE'''


Инстр:ЦенаПредпослСделки

   	declare @seccode varchar(12);
   declare @secboard varchar(4);
   declare @tsno decimal(38,0);
   declare @evdate decimal(38,0);
   set @evdate = 20191204;
   set @secboard = 'TQBR';
   set @seccode = 'AGRO';
   set @tsno = 4050676079;
   select price
   from [Check4Trick.Aton.QA.HistoryEQ].[dbo].[FRC_TRADES] where SECBOARD = @secboard and SECCODE = @seccode
and EVDATE = @evdate and TRADETYPE not in ('H','h','G') and TRADENO in
   (select max(TRADENO) from [Check4Trick.Aton.QA.HistoryEQ].[dbo].[FRC_TRADES] where SECBOARD = @secboard and SECCODE = @seccode
and EVDATE = @evdate and TRADETYPE not in ('H','h','G') and TRADENO < @tsno)