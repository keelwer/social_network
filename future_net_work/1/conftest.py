import pytest
import EventMonitoringDB
import yaml


def pytest_addoption(parser):
    parser.addoption(
        "--instance_dir",
        action="append",
        default=[],
        help="path to instance directory",
    )
    parser.addoption(
        "--task",
        action="append",
        default=[],
        help="task id",
    )


@pytest.fixture
def instance_dir(request):
    return request.config.getoption("--instance_dir")


@pytest.fixture
def task(request):
    return request.config.getoption("--task")[0]


# @pytest.fixture
# def task():
#     with open('config.yml') as f:
#         connect_params = yaml.safe_load(f)
#     return connect_params['task']['id']


@pytest.fixture
def db(instance_dir):
    # db = EventMonitoringDB.EventMonitoringDB(instance_dir=instance_dir[0])
    db = EventMonitoringDB.EventMonitoringDB(instance_dir='D:\check')
    return db
