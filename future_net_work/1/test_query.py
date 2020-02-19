def test_query(db, task):
    db.set_market('EQ')
    query = '''select * from frc_trades where evdate = 20191003'''
    request = db.execute(schema='history', query=query)
    assert (request['evdate'])
