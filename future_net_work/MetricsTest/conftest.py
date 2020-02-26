import pytest
import EventMonitoringDb
from EventMonitoring.Deploy import monitoring_instance
from Repos import DbRepo

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


# @pytest.fixture
# def task(request):
#     return request.config.getoption("--task")[0]


@pytest.fixture
def db():
    instance_dir = 'D:\check'
    instance = monitoring_instance.MonitoringInstance(instance_dir)
    connection = instance.get_connections()
    markets = instance.get_market_config().values()
    dbrepo = DbRepo.DbRepo(connection=connection, markets=markets)
    db = EventMonitoringDb.EventMonitoringDb(dbrepo)
    return db
