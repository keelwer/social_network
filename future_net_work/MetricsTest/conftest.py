import pytest
import sqlalchemy as db
import configparser


@pytest.fixture
def make_db_engine():
    config = configparser.ConfigParser()
    config.read('Config.ini')

    def _make_db_engine(schema):
        conn_string = f"Data Source={config['Default']['server']};Initial Catalog=" \
                      f"{config['Default']['instance']}.{schema}{config['Default']['market']};IntegratedSecurity=False;" \
                      f"User Id={config['Default']['login']};Password={config['Default']['password']}"
        engine = db.create_engine(conn_string)
        return engine

    return _make_db_engine

# config = configparser.ConfigParser()
# config.read('Config.ini')
# p = config['Default']['server']
