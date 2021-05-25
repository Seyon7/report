import datetime
import pytest
from modules.processor import RacerInfo


@pytest.fixture()
def datetime_obj() -> datetime.datetime:
    """Returns datetime object"""
    datetime_obj = datetime.datetime.strptime("BHS2018-05-24_12:10:01.585"[3:].strip(), "%Y-%m-%d_%H:%M:%S.%f")
    return datetime_obj


@pytest.fixture()
def correct_log_part_with_abbr():
    """Returns part of the correct log dictionary with abbreviations, racer's names and teams.
    Contains 2 correct  notes"""
    piece = {'SVF': RacerInfo(abbreviation='SVF', racer='Sebastian Vettel', team='FERRARI'),
             'FAM': RacerInfo(abbreviation='FAM', racer='Fernando Alonso', team='MCLAREN RENAULT')}
    return piece


@pytest.fixture()
def correct_log_part_with_start():
    """Returns part of the correct log dictionary with abbreviations, racer's names, teams and start time.
        Contains 2 correct  notes"""
    piece = {'SVF': RacerInfo(abbreviation='SVF', racer='Sebastian Vettel', team='FERRARI',
                              start=datetime.datetime(2018, 5, 24, 12, 2, 58, 917000), finish=None),
             'FAM': RacerInfo(abbreviation='FAM', racer='Fernando Alonso', team='MCLAREN RENAULT',
                              start=datetime.datetime(2018, 5, 24, 12, 13, 4, 512000), finish=None)}
    return piece


@pytest.fixture()
def correct_log_part():
    """Returns part from the correct output dictionary of make_race_log function. Contains 2 correct race notes"""
    sample_dict = {'SVF': RacerInfo(abbreviation='SVF', racer='Sebastian Vettel', team='FERRARI',
                                    start=datetime.datetime(2018, 5, 24, 12, 2, 58, 917000),
                                    finish=datetime.datetime(2018, 5, 24, 12, 4, 3, 332000)),
                   'FAM': RacerInfo(abbreviation='FAM', racer='Fernando Alonso', team='MCLAREN RENAULT',
                                    start=datetime.datetime(2018, 5, 24, 12, 13, 4, 512000),
                                    finish=datetime.datetime(2018, 5, 24, 12, 14, 17, 169000))}
    return sample_dict


@pytest.fixture()
def sample_log_with_errors():
    """Returns part from the correct output dictionary of make_race_log function. Contains 1 correct race
     note and 1 with error """
    return {'SVF': RacerInfo(racer='Sebastian Vettel', team='FERRARI',
                             start=datetime.datetime(2018, 5, 24, 12, 2, 58, 917000),
                             finish=datetime.datetime(2018, 5, 24, 12, 4, 3, 332000)),
            'DRR': RacerInfo(racer='Daniel Ricciardo', team='RED BULL RACING TAG HEUER',
                             start=datetime.datetime(2018, 5, 24, 12, 14, 12, 54000),
                             finish=datetime.datetime(2018, 5, 24, 12, 11, 24, 67000))}


@pytest.fixture()
def correct_racer_info_obj():
    """Return RacerInfo class obj"""
    return RacerInfo(racer='Oleksii Leshchenko', team='Niva Veyron', start=datetime.datetime(2020, 5, 24, 12, 11, 24, 917000),
                     finish=datetime.datetime(2020, 5, 24, 12, 4, 3, 332000))


@pytest.fixture()
def wrong_racer_info_obj():
    """Return not completed RacerInfo class obj"""
    return RacerInfo(racer='Sebastian Vettel')


@pytest.fixture()
def sample_formatted_report():
    """Returns part from the correct formatted report list"""
    return [['Sebastian Vettel', 'FERRARI', '0:01:04.415'], ['Fernando Alonso', 'MCLAREN RENAULT', '0:01:12.657']]


@pytest.fixture()
def report_withot_driver_part():
    """Returns part from correct final report"""
    return [" 10. Pierre Gasly                  | SCUDERIA TORO ROSSO HONDA          | 0:01:12.941",
            " 11. Carlos Sainz                  | RENAULT                            | 0:01:12.950"]


@pytest.fixture()
def one_racer_report():
    """Returns example of correct report when driver's name was given"""
    return "Sebastian Vettel              | FERRARI                            | 0:01:04.415"
