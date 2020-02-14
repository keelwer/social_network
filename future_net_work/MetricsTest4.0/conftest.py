import pytest
import additional_functions


import yaml
with open('config.yml') as f:
    dataMap = yaml.safe_load(f)


@pytest.fixture
def task():
    with open('config.yml') as f:
        connect_params = yaml.safe_load(f)
    return connect_params['task']['id']


@pytest.fixture
def db():
    with open('config.yml') as f:
        connect_params = yaml.safe_load(f)
    db_class = additional_functions.MetricTest(connect_params=connect_params)
    return db_class
