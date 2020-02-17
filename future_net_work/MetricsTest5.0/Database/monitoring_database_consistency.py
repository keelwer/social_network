import collections
import datetime
from EventMonitoringDeploy import monitoring_instance
import logging
import argparse
import sys

ev_types = ['1', '2', '3', '12', '14']
reference_state = {'1': True, '2': True, '3': True, '12': True, '14': True}
ev_types_for_table = {'1': 'FRC_ORDERS', '2': 'FRC_TRADES', '3': 'FRC_WITHDRAWS', '12': 'FRC_ALL_TRADES', '14': 'FRC_TIMEEVENTS'}
bool_consistency = {True: '', False: ' не'}
tables_of_tools = ['FRC_EVENTS', 'FRC_HIST_SECURITY', 'FRC_HIST_SPECSEC']


def get_number_of_events_by_date(engine, from_date, market):
    get_dict = {}
    number = 0
    select = f"""select COUNT(EVDATE) as string_count, EVDATE from FRC_EVENTS where evdate = '{from_date}' group by evdate"""
    if market == 'fo':
        get_session_by_date = f"""select min(SESSID) from frc_events where evdate = '{from_date}'"""
        select = f"""select COUNT(SESSID) as string_count, EVDATE from FRC_EVENTS where SESSID = ({get_session_by_date}) group by evdate"""
    output = engine.execute(select).fetchall()
    if output:
        if market == 'fo':
            for string in output:
                number += string[0]
            get_dict[str(from_date)] = number
        else:
            get_dict[str(output[0][1])] = output[0][0]
    return get_dict


def get_number_of_orders_by_date(engine, from_date, market):
    get_dict = {}
    number = 0
    select = f"""select COUNT(ORDERNO) as string_count, EVDATE from FRC_ORDERS where evdate = '{from_date}' group by evdate"""
    if market == 'fo':
        get_session_by_date = f"""select min(SESSID) from frc_events where evdate = '{from_date}'"""
        select = f"""select COUNT(SESSID) as string_count, EVDATE from FRC_ORDERS where SESSID = ({get_session_by_date}) group by evdate"""
    output = engine.execute(select).fetchall()
    if output:
        if market == 'fo':
            for string in output:
                number += string[0]
            get_dict[str(from_date)] = number
        else:
            get_dict[str(output[0][1])] = output[0][0]
    return get_dict


def get_number_of_trades_by_date(engine, from_date, market):
    get_dict = {}
    number = 0
    select = f"""select COUNT(EVDATE) as string_count, EVDATE from FRC_TRADES where evdate = '{from_date}' group by evdate"""
    if market == 'fo':
        get_session_by_date = f"""select min(SESSID) from frc_events where evdate = '{from_date}'"""
        select = f"""select COUNT(SESSID) as string_count, EVDATE from FRC_TRADES where SESSID = ({get_session_by_date}) group by evdate"""
    output = engine.execute(select).fetchall()
    if output:
        if market == 'fo':
            for string in output:
                number += string[0]
            get_dict[str(from_date)] = number
        else:
            get_dict[str(output[0][1])] = output[0][0]
    return get_dict


def get_number_of_all_trades_by_date(engine, from_date, market):
    get_dict = {}
    number = 0
    select = f"""select COUNT([TRADENO]) as string_count, EVDATE from FRC_ALL_TRADES where evdate = '{from_date}' group by evdate"""
    if market == 'fo':
        get_session_by_date = f"""select min(SESSID) from frc_events where evdate = '{from_date}'"""
        select = f"""select COUNT(SESSID) as string_count, EVDATE from FRC_ALL_TRADES where SESSID = ({get_session_by_date}) group by evdate"""
    output = engine.execute(select).fetchall()
    if output:
        if market == 'fo':
            for string in output:
                number += string[0]
            get_dict[str(from_date)] = number
        else:
            get_dict[str(output[0][1])] = output[0][0]
    return get_dict


def get_number_of_withdraws_by_date(engine, from_date, market):
    get_dict = {}
    number = 0
    select = f"""select COUNT(EVDATE) as string_count, EVDATE from FRC_WITHDRAWS where evdate = '{from_date}' group by evdate"""
    if market == 'fo':
        get_session_by_date = f"""select min(SESSID) from frc_events where evdate = '{from_date}'"""
        select = f"""select COUNT(SESSID) as string_count, EVDATE from FRC_WITHDRAWS where SESSID = ({get_session_by_date}) group by evdate"""
    output = engine.execute(select).fetchall()
    if output:
        if market == 'fo':
            for string in output:
                number += string[0]
            get_dict[str(from_date)] = number
        else:
            get_dict[str(output[0][1])] = output[0][0]
    return get_dict


def get_number_of_time_events_by_date(engine, from_date, market):
    get_dict = {}
    number = 0
    select = f"""select COUNT(EVDATE) as string_count, EVDATE from FRC_TIMEEVENTS where evdate = '{from_date}' group by evdate"""
    if market == 'fo':
        get_session_by_date = f"""select min(SESSID) from frc_events where evdate = '{from_date}'"""
        select = f"""select COUNT(SESSID) as string_count, EVDATE from FRC_TIMEEVENTS where SESSID = ({get_session_by_date}) group by evdate"""
    output = engine.execute(select).fetchall()
    if output:
        if market == 'fo':
            for string in output:
                number += string[0]
            get_dict[str(from_date)] = number
        else:
            get_dict[str(output[0][1])] = output[0][0]
    return get_dict


def get_number_of_rows_in_hist_security_by_date(engine, from_date, market):
    get_dict = {}
    select = f"""select COUNT(RECDATE) as string_count, RECDATE from FRC_HIST_SECURITY where RECDATE = '{from_date}' group by RECDATE"""
    if market == 'fo':
        select = f"""select COUNT(RECDATE) as string_count, RECDATE from FRC_HIST_SECURITY where RECDATE = (select min(SESSID) from frc_events where evdate = '{from_date}') group by RECDATE"""
    output = engine.execute(select).fetchall()
    if output:
        get_dict[str(output[0][1])] = output[0][0]
    return get_dict


def get_number_of_rows_in_hist_specsec_by_date(engine, from_date, market):
    get_dict = {}
    select = f"""select COUNT(RECDATE) as string_count, RECDATE from FRC_HIST_SPECSEC where RECDATE = '{from_date}' group by RECDATE"""
    if market == 'fo':
        select = f"""select COUNT(RECDATE) as string_count, RECDATE from FRC_HIST_SPECSEC where RECDATE = (select min(SESSID) from frc_events where evdate = '{from_date}') group by RECDATE"""
    output = engine.execute(select).fetchall()
    if output:
        get_dict[str(output[0][1])] = output[0][0]
    return get_dict


def get_event_type_statistics(engine, ev_type, date, market):
    select = f"""SELECT 
          EVTYPE, count(1), EVDATE
      FROM FRC_EVENTS where EVTYPE = '{ev_type}' and EVDATE = '{date}' group by EVDATE, EVTYPE"""
    if market == 'fo':
        select = f"""SELECT
      EVTYPE, count(1), SESSID
  FROM FRC_EVENTS where SESSID = (select min(SESSID) from frc_events where evdate = '{date}') and EVTYPE = '{ev_type}' group by EVTYPE, SESSID"""
    output = engine.execute(select).fetchall()
    for result in output:
        result = (str(date), result[0], result[1])
        return result


def monitoring_database_consistency(instance_dir, from_date, to_date, market: str, debug=True):
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger('c4t_monitoring_database_consistency')
    logger.level = (logging.DEBUG if debug else logging.INFO)
    if debug:
        handler = logging.FileHandler('logs_database_consistency.log')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    logger.addHandler(logging.StreamHandler(sys.stderr))
    try:
        instance = monitoring_instance.MonitoringInstance(instance_dir=instance_dir)
    except FileNotFoundError:
        logger.debug('Неправильный путь к инстансу')
        sys.exit(1)
    logger.debug('Подключение к базе данных. Это займет некоторое время.')
    try:
        engine = instance.get_connections()[f'history_{market.lower()}']
    except KeyError:
        logger.debug('Данного рынка не существует')
        sys.exit(1)
    ev_type_for_table = {}

    result_for_empty_tables = {}
    not_equal_number_of_strings_evtype = collections.defaultdict(lambda: collections.defaultdict(bool))
    try:
        start = datetime.datetime.strptime(str(from_date), "%Y%m%d")
        end = datetime.datetime.strptime(str(to_date), "%Y%m%d")
    except ValueError:
        logger.debug('Дата задана в неверном формате. Необходимый формат YYYYMMDD.')
        sys.exit(1)
    if start > end:
        logger.debug('Первая дата должна быть меньше второй')
        sys.exit(1)
    logger.debug('Подключение успешно.')
    logger.debug('Происходит подсчет. Это займет некоторое время...')
    date_generated = [date.strftime("%Y%m%d") for date in  # создание интервала дат только рабочих дней (пн-пт)
                      [start + datetime.timedelta(days=x) for x in range(0, (end - start).days + 1)] if
                      datetime.datetime.strptime(date.strftime("%Y%m%d"), "%Y%m%d").weekday() < 5]
    bool_table_fullness = False
    bool_table_consistency = False
    for day in date_generated:
        empty_tables = []
        events = get_number_of_events_by_date(engine=engine, from_date=day, market=market.lower())
        ev_type_for_table['1'] = get_number_of_orders_by_date(engine=engine, from_date=day, market=market.lower())
        ev_type_for_table['2'] = get_number_of_trades_by_date(engine=engine, from_date=day, market=market.lower())
        ev_type_for_table['12'] = get_number_of_all_trades_by_date(engine=engine, from_date=day,
                                                                   market=market.lower())
        ev_type_for_table['3'] = get_number_of_withdraws_by_date(engine=engine, from_date=day,
                                                                 market=market.lower())
        ev_type_for_table['14'] = get_number_of_time_events_by_date(engine=engine, from_date=day,
                                                                    market=market.lower())
        hist_security = get_number_of_rows_in_hist_security_by_date(engine=engine, from_date=day,
                                                                    market=market.lower())
        hist_specsec = get_number_of_rows_in_hist_specsec_by_date(engine=engine, from_date=day,
                                                                  market=market.lower())

        if day not in events.keys():
            empty_tables.append('FRC_EVENTS')
        if day not in ev_type_for_table['1'].keys():
            empty_tables.append('FRC_ORDERS')
        if day not in ev_type_for_table['2'].keys():
            empty_tables.append('FRC_TRADES')
        if day not in ev_type_for_table['12'].keys():
            empty_tables.append('FRC_ALL_TRADES')
        if day not in ev_type_for_table['3'].keys():
            empty_tables.append('FRC_WITHDRAWS')
        if day not in ev_type_for_table['14'].keys():
            empty_tables.append('FRC_TIMEEVENTS')
        if day not in hist_security.keys():
            empty_tables.append('FRC_HIST_SECURITY')
        if day not in hist_specsec.keys():
            empty_tables.append('FRC_HIST_SPECSEC')
        if empty_tables:
            result_for_empty_tables[day] = empty_tables
        for ev_type in ev_types:
            result = get_event_type_statistics(engine=engine, ev_type=ev_type, date=day, market=market.lower())
            if result and day in ev_type_for_table[ev_type].keys():
                if result[2] == ev_type_for_table[ev_type][day]:
                    not_equal_number_of_strings_evtype[day][ev_type] = True
                else:
                    not_equal_number_of_strings_evtype[day][ev_type] = False
            else:
                not_equal_number_of_strings_evtype[day][ev_type] = False

    auxiliary_dictionary = not_equal_number_of_strings_evtype.copy()
    for day, l in not_equal_number_of_strings_evtype.items():
        if not_equal_number_of_strings_evtype[day] == reference_state:
            auxiliary_dictionary.pop(day)
    if not auxiliary_dictionary and not_equal_number_of_strings_evtype:
        bool_table_consistency = True
    if not result_for_empty_tables:
        bool_table_fullness = True
    logger.debug(f'Проверка таблиц на заполненность.')
    logger.debug(f'Проверка данных таблиц на консистентность.')
    if bool_table_consistency:
        logger.debug('Данные в таблицах консистентны')
    else:
        for day, events_type in not_equal_number_of_strings_evtype.items():
            logger.debug('<' + '-' * 35 + 'День ' + day + '-' * 35 + '>')
            for table in tables_of_tools:
                logger.debug('{:20s}'.format(table) + f': Таблица{bool_consistency[day in result_for_empty_tables.keys() and table in result_for_empty_tables[day]]} пустая')
            for ev_type, bool_ev in events_type.items():
                logger.debug(
                    '{:20s}'.format(ev_types_for_table[ev_type]) + f': Таблица{bool_consistency[day in result_for_empty_tables.keys() and ev_types_for_table[ev_type] in result_for_empty_tables[day]]} пустая; ' + f'Данные{bool_consistency[bool_ev]} консистентны')
        logger.debug(f'Данные в таблицах не консистентны.')
    return bool_table_fullness, bool_table_consistency, result_for_empty_tables, not_equal_number_of_strings_evtype


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--instance_dir', required=True, help='Input path to instance')
    parser.add_argument('--from_date', required=True, help='Input first date')
    parser.add_argument('--to_date', required=True, help='Input second date')
    parser.add_argument('--market', required=True, help='Input market')
    try:
        monitoring_database_consistency(instance_dir=parser.parse_args().instance_dir,
                                        from_date=parser.parse_args().from_date, to_date=parser.parse_args().to_date,
                                        market=parser.parse_args().market)
    except Exception as e:
        print(e)
