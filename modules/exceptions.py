class StringFormatError(Exception):
    """Can not parse string from abbreviation file"""


class AbbreviationStringFormatError(Exception):
    """Abbreviation string format is not as needed. Correct string must be like 'APV_Augusto Pinochet_VAZ 2101'"""


class ParseDateError(Exception):
    """Can not parse the given date. Check the input string format. Correct format 'BHS2018-05-24_12:10:01.585'"""


class FileDoesNotExistError(Exception):
    """This file does not exist"""


class WrongFilePathError(Exception):
    """One or more filepath is incorrect"""


class WrongDataFileError(Exception):
    """Wrong filename"""


class WrongDriverName(Exception):
    """This driver did not participate in the race"""
