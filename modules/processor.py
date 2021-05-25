import os
from dataclasses import dataclass
import datetime

from modules.exceptions import *


data_files = {
    "start": "start.log",
    "end": "end.log",
    "abbreviation": "abbreviations.txt"
}
error_log_path = os.path.join(os.path.dirname(__file__), '../ErrorLogs/error_log.txt')
print(__file__)


@dataclass()
class RacerInfo:
    abbreviation: str = None
    racer: str = None
    team: str = None
    start: datetime = None
    finish: datetime = None

    @property
    def best_lap_time(self):
        if self.start is None or self.finish is None:
            return None
        return self.finish - self.start


def check_if_files_exists(data_folder_path: str) -> bool:
    assert type(data_folder_path) == str
    for filename in data_files.values():
        if not os.path.isfile(os.path.join(data_folder_path, filename)):
            raise FileDoesNotExistError(f"File {filename} is not found")
    return True


def make_path_to_files(data_folder_path: str) -> list:
    assert type(data_folder_path) == str
    if check_if_files_exists(data_folder_path):
        start_file_path = os.path.join(data_folder_path, data_files["start"])
        end_file_path = os.path.join(data_folder_path, data_files["end"])
        abbreviation_file_path = os.path.join(data_folder_path, data_files["abbreviation"])
        path_list = [start_file_path, end_file_path, abbreviation_file_path]
        for path in path_list:
            if not os.path.exists(path):
                raise FileDoesNotExistError(f"{path} does not exist")
        assert type(path_list) == list
        return path_list
    raise FileNotFoundError("No such file or directory")


def get_racer_abbreviation(raw_abbr_string: str):
    assert type(raw_abbr_string) == str
    abbr = raw_abbr_string[:3]
    if not abbr.isalpha():
        raise AbbreviationStringFormatError
    return abbr


def get_datetime(raw_string: str) -> datetime.datetime:
    assert type(raw_string) == str
    try:
        datetime_obj = datetime.datetime.strptime(raw_string[3:].strip(), '%Y-%m-%d_%H:%M:%S.%f')
    except ValueError:
        raise ParseDateError
    assert type(datetime_obj) == datetime.datetime
    return datetime_obj


def create_log_with_abbr_team_name(abbreviation_data_path: str):
    assert type(abbreviation_data_path) == str

    log = {}
    try:
        with open(abbreviation_data_path) as f:
            content = f.readlines()
            for line in content:
                line = line.strip()
                try:
                    abbreviation, name, team = line.split("_")
                except ValueError:
                    raise StringFormatError
                log[abbreviation] = RacerInfo(abbreviation=abbreviation, racer=name, team=team)
    except FileNotFoundError:
        raise FileDoesNotExistError(f"Filepath is incorrect: {abbreviation_data_path}")
    assert type(log) == dict
    return log


def add_timestamp(path: str, log: dict):
    assert type(path) == str
    assert type(log) == dict

    log_to_add_timestamp = log

    try:
        with open(path) as f:
            content = f.readlines()
        for line in content:
            for key in log_to_add_timestamp.keys():
                if line.startswith(key):
                    if 'start' in path:
                        log_to_add_timestamp[key].start = get_datetime(line)
                    elif 'end' in path:
                        log_to_add_timestamp[key].finish = get_datetime(line)
                    else:
                        raise WrongDataFileError
    except FileNotFoundError:
        raise FileDoesNotExistError(f"Filepath is incorrect: {path}")
    assert type(log_to_add_timestamp)
    return log_to_add_timestamp


def make_log(data_folder_path: str) -> dict:
    assert type(data_folder_path) == str

    path_list = make_path_to_files(data_folder_path)

    for path in path_list:
        assert type(path) == str

    try:
        start_data_path, finish_data_path, abbreviation_data_path = path_list
        log = create_log_with_abbr_team_name(abbreviation_data_path)
        log = add_timestamp(start_data_path, log)
        log = add_timestamp(finish_data_path, log)
    except FileNotFoundError:
        raise WrongFilePathError

    assert type(log) == dict
    return log


def make_error_log_string(racer_log: RacerInfo) -> str:
    assert type(racer_log) == RacerInfo
    assert racer_log.racer is not None
    assert racer_log.start is not None
    assert racer_log.finish is not None

    error_str = f"{racer_log.racer} race time is incorrect — finish {racer_log.finish} before start {racer_log.start}\n"
    assert type(error_str) == str
    return error_str


def make_error_log_file(log_dict: dict):
    assert type(log_dict) == dict
    with open(error_log_path, 'w') as f:
        for key in log_dict.keys():
            if log_dict[key].best_lap_time.days < 0:
                f.write(make_error_log_string(log_dict[key]))


def print_error_log(error_path: str):
    assert type(error_path) == str
    if os.path.exists(error_path):
        print("------------------------------------------------------------------------")
        with open(error_path) as f:
            content = f.readlines()
            for line in content:
                print(line.strip())
    else:
        raise FileDoesNotExistError("Error log file does not exist")


def delete_log_notes_with_error(log: dict) -> dict:
    assert type(log) == dict
    key_list = list(log.keys())
    for key in key_list:
        if log[key].best_lap_time.days < 0:
            del log[key]
    assert type(log) == dict
    return log


def make_one_racer_info(name: str, log: list) -> str:
    assert type(name) == str
    assert type(log) == list

    for racer, team, race_time in log:
        if racer == name:
            info_str = f"{racer:30}| {team:35}| {race_time:11}"
            assert type(info_str) == str
            return info_str
    try:
        with open(error_log_path) as f:
            for line in f:
                if name in line:
                    info_str = line.strip()
                    return info_str
    except FileNotFoundError:
        raise FileDoesNotExistError("Error log file does not exist")
    raise WrongDriverName("This driver did not participate in the race")


def format_report(log: dict) -> list:
    assert type(log) == dict
    formatted_report = []
    for val in log.values():
        formatted_report.append([val.racer, val.team, str(val.best_lap_time)[:-3]])
    print(formatted_report)
    assert type(formatted_report) == list
    return formatted_report


def sorted_log(formatted_report: list, order: str) -> list:
    assert type(formatted_report) == list
    assert order in ("asc", "desc")
    sorted_report = sorted(formatted_report, key=lambda x: x[2], reverse=False)

    race_log_list = []
    counter = 1
    for racer, team, race_time in sorted_report:
        one_racer_result = f'{counter:3}. {racer:30}| {team:35}| {race_time:11}'
        race_log_list.append(one_racer_result)
        counter += 1
    if len(race_log_list) > 15:
        race_log_list.insert(15, "------------------------------------------------------------------------")
    if order == 'desc':
        race_log_list.reverse()
    assert type(race_log_list) == list
    return race_log_list


def build_report(data_folder_path: str, order="asc", driver=None):
    assert type(data_folder_path) == str
    assert type(order) == str
    assert order in ("asc", "desc")
    assert driver is None or type(driver) == str
    assert os.path.exists(data_folder_path)

    log = make_log(data_folder_path)
    make_error_log_file(log)
    log = delete_log_notes_with_error(log)
    formatted_log = format_report(log)
    if driver:
        report = make_one_racer_info(driver, formatted_log)
        assert type(report) == str
    else:
        report = sorted_log(formatted_log, order)
        assert type(report) == list
    return report, driver


def print_report(report_data_set: tuple):
    assert type(report_data_set) == tuple

    report, driver = report_data_set

    if driver:
        print(report)
    else:
        for i in report:
            print(i)
        print_error_log(error_log_path)
