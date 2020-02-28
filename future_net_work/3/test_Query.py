from Events.EventTypes import Market

def test_query(db):
    db.set_market(Market.EQ)
    query = '''select * from frc_trades where evdate = 20191003'''
    request = db.execute(schema='history', query=query)
    assert (request['evdate'])
