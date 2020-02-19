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
   from [Check4Trick.Aton.QA.HistoryEQ].[dbo].[FRC_TRADES]
   where SECBOARD = @secboard and SECCODE = @seccode and EVDATE = @evdate and TRADETYPE not in ('H','h','G') and TRADENO in
   (select max(TRADENO)
   from [Check4Trick.Aton.QA.HistoryEQ].[dbo].[FRC_TRADES]
   where SECBOARD = @secboard and SECCODE = @seccode and EVDATE = @evdate and TRADETYPE not in ('H','h','G') and TRADENO < @tsno)


КлиентИнстр:ОбъемСделокИсторическая
select SECBOARD, SECCODE, FIRMCODE, SPECCODE, sum(qty_all) as qty
from [Check4Trick.Aton.QA.HistoryEQ].[dbo].[FRC_HIST_SPECSEC]
where RECDATE in
(
select max(RECDATE)
from [Check4Trick.Aton.QA.HistoryEQ].[dbo].[FRC_HIST_SPECSEC]
where RECDATE < 20191204
)
group by SECBOARD, SECCODE, FIRMCODE, SPECCODE
order by SECBOARD, SECCODE, FIRMCODE, SPECCODE