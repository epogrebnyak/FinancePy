from dataclasses import dataclass
from enum import Enum
from typing import Tuple


def num_days_in_month(month: int) -> int:
    return [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month - 1]


def is_leap(year: int) -> bool:
    return (year % 4 == 0) and (year % 100 != 0) or (year % 400 == 0)


def num_days_in_february(year) -> int:
    if year == 1900 or is_leap(year):
        return 29  # 1900 considered leap year for Excel compatibility
    else:
        return 28


def num_days(year: int, month: int) -> int:
    if month == 2:
        return num_days_in_february(year)
    else:
        return num_days_in_month(month)


def make_dates(start_year, end_year):
    """Create mapping dictionary for converting dates to Excel
    representation.
    """
    result = {}
    day_counter = 1  # Jan 1, 1900 is day 1 in excel
    for year in range(start_year, end_year + 1):
        for month in range(1, 12 + 1):
            max_days = num_days(year, month)
            for day in range(1, max_days + 1):
                result[(year, month, day)] = day_counter
                day_counter += 1
    return result


START_YEAR = 1900
END_YEAR = 2100
EXCEL_INTEGERS_DICT = make_dates(start_year=START_YEAR, end_year=END_YEAR)
REVERSE_DICT = {v: k for k, v in EXCEL_INTEGERS_DICT.items()}


def to_excel_date(year, month, day) -> int:
    """Convert date to integer index similar to Excel representation."""
    return EXCEL_INTEGERS_DICT[(year, month, day)]


def from_excel_date(xl_date: int) -> Tuple[int, int, int]:
    """Convert Excel representation back to (year, month, day)"""
    return REVERSE_DICT[xl_date]

# convert to tests
assert to_excel_date(1900, 1, 5) == 5
assert to_excel_date(2020, 3, 1) == 43891
assert from_excel_date(5) == (1900, 1, 5)
assert from_excel_date(43891) == (2020, 3, 1)


def is_allowed_date(year, month, day):
    return (year, month, day) in EXCEL_INTEGERS_DICT.keys()

assert not is_allowed_date(1812, 1, 1)


@dataclass(order=True)
class Date:
    """This is date-only (no time) class.
    Year-first allows easy ordering, example:
      Date(2020, 12, 31) < Date(2021, 1, 1)
    """

    year: int
    month: int
    day: int

    def to_excel(self):
        return to_excel_date(self.year, self.month, self.day)

    @property
    def weekday(self):
        return week_day(self.to_excel())

    def add_days(self, n_days):
        xl_date = self.to_excel() + n_days
        year, month, day = from_excel_date(xl_date)
        return Date(year, month, day)


# convert to tests
assert Date(2020, 12, 31) < Date(2020, 12, 31).add_days(1)
assert Date(2020, 12, 31) > Date(2020, 12, 31).add_days(-1)
assert Date(2020, 12, 31).add_days(1).add_days(-1) == Date(2020, 12, 31)


class WeekDay(Enum):
    MON = 0
    TUE = 1
    WED = 2
    THU = 3
    FRI = 4
    SAT = 5
    SUN = 6


def week_day(xl_date: int):
    return WeekDay((xl_date + 6) % 7)


# convert to tests
assert Date(2020, 3, 2).weekday == WeekDay.TUE
