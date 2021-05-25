import pytest
import sys
import io
from unittest.mock import patch, mock_open

from modules.processor import *


@pytest.mark.parametrize("correct_path,wrong_path", [("../data", "abracadabra")])
def test_check_if_files_exists(correct_path, wrong_path):
    assert check_if_files_exists(correct_path) is True
    with pytest.raises(FileDoesNotExistError):
        check_if_files_exists(wrong_path)


@patch('modules.processor.check_if_files_exists', return_value=True)
@pytest.mark.parametrize("correct_path,wrong_path", [("../data", "dat")])
def test_make_path_to_files(mock, correct_path, wrong_path):
    assert make_path_to_files(correct_path) == ["../data\\start.log", "../data\\end.log", "../data\\abbreviations.txt"]
    with pytest.raises(FileDoesNotExistError):
        make_path_to_files(wrong_path)


@pytest.mark.parametrize("correct_abbr_string, wrong_abbr_format",
                         [("APV_Augusto Pinochet_VAZ 2101", "1_Dsdfghjkkjhgfvcdfghjkjhg")])
def test_get_racer_abbreviation(correct_abbr_string, wrong_abbr_format):
    result = get_racer_abbreviation(correct_abbr_string)
    assert result == "APV"
    with pytest.raises(AbbreviationStringFormatError):
        get_racer_abbreviation(wrong_abbr_format)


@pytest.mark.parametrize("correct_raw_string,incorrect_raw_string",
                         [("BHS2018-05-24_12:10:01.585", "APV28-05-24_120:01.5")])
def test_get_datetime(correct_raw_string, incorrect_raw_string, datetime_obj):
    result = get_datetime(correct_raw_string)
    assert result == datetime_obj
    with pytest.raises(ParseDateError):
        get_datetime(incorrect_raw_string)


@pytest.mark.parametrize("correct_path,wrong_path", [("../data\\abbreviations.txt", "abracadabra")])
def test_create_log_with_abbr_team_name(correct_path, wrong_path, correct_log_part_with_abbr):
    m = mock_open()
    with patch('builtins.open', m):
        create_log_with_abbr_team_name(correct_path)
    assert m.call_count == 1
    handle = m()
    handle.readlines.assert_called()

    result = create_log_with_abbr_team_name(correct_path)
    assert result.items() >= correct_log_part_with_abbr.items()

    with pytest.raises(FileDoesNotExistError):
        create_log_with_abbr_team_name(wrong_path)


@pytest.mark.parametrize('start_path,end_path,wrong_filename,wrong_path',
                         [("../data\\start.log", "../data\\end.log", "../data\\abbreviations.txt", "abracadabra")])
def test_add_timestamp(start_path, end_path, wrong_filename, wrong_path,
                       correct_log_part_with_abbr, correct_log_part_with_start, correct_log_part):
    m = mock_open()
    with patch('builtins.open', m):
        add_timestamp(start_path, correct_log_part_with_abbr)
        add_timestamp(end_path, correct_log_part_with_start)
    assert m.call_count == 2
    handle = m()
    handle.readlines.assert_called()

    result = add_timestamp(start_path, correct_log_part_with_abbr)
    assert result.items() == correct_log_part_with_start.items()

    result = add_timestamp(end_path, correct_log_part_with_start)
    assert result.items() == correct_log_part.items()

    with pytest.raises(FileDoesNotExistError):
        add_timestamp(wrong_path, correct_log_part_with_abbr)

    with pytest.raises(WrongDataFileError):
        add_timestamp(wrong_filename, correct_log_part_with_abbr)


@pytest.mark.parametrize("correct_path,wrong_path", [('../data', 'dratuti')])
def test_make_log(correct_path, wrong_path, correct_log_part):
    result = make_log(correct_path)
    assert result.items() > correct_log_part.items()

    with pytest.raises(FileDoesNotExistError):
        make_log(wrong_path)


def test_make_error_log_string(correct_racer_info_obj, wrong_racer_info_obj):
    result = make_error_log_string(correct_racer_info_obj)
    assert result == "Oleksii Leshchenko race time is incorrect — finish 2020-05-24 12:04:03.332000 " \
                     "before start 2020-05-24 12:11:24.917000\n"
    with pytest.raises(AssertionError):
        make_error_log_string(wrong_racer_info_obj)


def test_make_error_log(sample_log_with_errors):
    m = mock_open()
    with patch('builtins.open', m):
        make_error_log_file(sample_log_with_errors)

    assert m.call_count == 1
    handle = m()
    handle.write.assert_called_once_with('Daniel Ricciardo race time is incorrect — finish 2018-05-24 12:11:24.067000'
                                         ' before start 2018-05-24 12:14:12.054000\n')


@pytest.mark.parametrize("correct_path,wrong_path,wrong_path_type", [("../ErrorLogs/error_log.txt", "../path", True)])
def test_print_error_log(correct_path, wrong_path, wrong_path_type):
    captured_output = io.StringIO()
    sys.stdout = captured_output
    m = mock_open()
    with patch('builtins.open', m):
        print_error_log(correct_path)

    assert m.call_count == 1
    handle = m()
    handle.readlines.assert_called()

    sys.stdout = sys.__stdout__
    assert captured_output.getvalue().strip().find("---------------------------------------------------") == 0
    assert captured_output.getvalue().find("Daniel Ricciardo race time is incorrect — finish 2018-05-24 12:11:24.067000"
                                           " before start 2018-05-24 12:14:12.054000")

    with pytest.raises(FileDoesNotExistError):
        print_error_log(wrong_path)


def test_delete_log_notes_with_error(sample_log_with_errors):
    result = delete_log_notes_with_error(sample_log_with_errors)
    assert result == {'SVF': RacerInfo(racer='Sebastian Vettel', team='FERRARI',
                                       start=datetime.datetime(2018, 5, 24, 12, 2, 58, 917000),
                                       finish=datetime.datetime(2018, 5, 24, 12, 4, 3, 332000))}


@pytest.mark.parametrize("correct_name,name_from_error_log,bad_name",
                         [("Sebastian Vettel", "Esteban Ocon", "Vasya Oblomov")])
def test_make_one_racer_info(correct_name, name_from_error_log, bad_name, sample_formatted_report):
    result = make_one_racer_info(correct_name, sample_formatted_report)
    assert result == 'Sebastian Vettel              | FERRARI                            | 0:01:04.415'
    result_from_error_log = make_one_racer_info(name_from_error_log, sample_formatted_report)
    assert result_from_error_log == 'Esteban Ocon race time is incorrect — finish 2018-05-24 12:12:11.838000 ' \
                                    'before start 2018-05-24 12:17:58.810000'
    with pytest.raises(WrongDriverName):
        make_one_racer_info(bad_name, sample_formatted_report)


def test_format_report(correct_log_part, sample_formatted_report):
    result = format_report(correct_log_part)
    assert result == sample_formatted_report


@pytest.mark.parametrize("asc_order,desc_order,wrong_order", [("asc", "desc", "aaa")])
def test_sorted_log(sample_formatted_report, asc_order, desc_order, wrong_order):
    result_asc = sorted_log(sample_formatted_report, asc_order)
    assert result_asc[0] == "  1. Sebastian Vettel              | FERRARI                            | 0:01:04.415"

    result_desc = sorted_log(sample_formatted_report, desc_order)
    assert result_desc[0] == "  2. Fernando Alonso               | MCLAREN RENAULT                    | 0:01:12.657"


@pytest.mark.parametrize("correct_path,correct_driver,wrong_driver",
                         [("../data", "Sebastian Vettel", "Oleksii Leshchenko")])
def test_build_report(correct_path, correct_driver, wrong_driver,
                      report_withot_driver_part, one_racer_report):
    result_without_driver = build_report(correct_path)
    report, driver = result_without_driver
    assert driver is None
    assert all(elem in report for elem in report_withot_driver_part)

    result_with_driver = build_report(correct_path, driver=correct_driver)
    report, driver = result_with_driver
    assert type(driver) == str
    assert report == one_racer_report

    with pytest.raises(WrongDriverName):
        build_report(correct_path, driver=wrong_driver)


def test_print_report(report_withot_driver_part, one_racer_report):
    captured_output = io.StringIO()
    sys.stdout = captured_output
    print_report((one_racer_report, "Sebastian Vettel"))
    sys.stdout = sys.__stdout__
    assert captured_output.getvalue().find(one_racer_report) != -1

    captured_output = io.StringIO()
    sys.stdout = captured_output
    print_report((report_withot_driver_part, None))
    sys.stdout = sys.__stdout__
    assert captured_output.getvalue().find(" 11. Carlos Sainz                  | RENAULT                            | 0:01:12.950") != -1
