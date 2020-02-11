import pytest
import sqlalchemy
import configparser


@pytest.fixture
def db():
    config = configparser.ConfigParser()
    config.read('Config.ini')
    def _db(schema):
        conn_string = f"mssql+pyodbc://{config['Default']['login']}:{config['Default']['password']}@{config['Default']['server']}:1433/{config['Default']['instance']}.{schema}{config['Default']['market']}?driver=SQL+Server+Native+Client+11.0"
        engine = sqlalchemy.create_engine(conn_string)
        return engine
    return _db

