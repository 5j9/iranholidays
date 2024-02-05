from datetime import date, datetime

from hijri_converter import Hijri
from jdatetime import date as jdate, datetime as jdatetime
from pytest import raises

from iranholidays import (
    HIJRI_HOLIDAYS,
    SOLAR_HOLIDAYS,
    is_holiday,
    is_workday,
    set_default_weekend,
)

assert len(HIJRI_HOLIDAYS) == len(SOLAR_HOLIDAYS) == 13


def test_holiday_occasion_solar_calendar():
    # In reality, this was NOT a holiday in Iran (30st of Ramazan)
    assert is_holiday((1402, 2, 1, 'S')) is True
    assert is_holiday((1402, 2, 2, 'S')) is True
    # In reality, this WAS a holiday in Iran (2nd of Shawal)
    assert is_holiday((1402, 2, 3, 'S')) is False
    assert is_holiday((1402, 2, 4, 'S')) is False
    assert is_holiday((1402, 1, 13, 'S')) is True


def test_holiday_occasion_gregorian_calendar():
    assert is_holiday((2023, 4, 21, 'G')) is True
    assert is_holiday((2023, 4, 22, 'G')) is True
    # In reality, this WAS a holiday in Iran (2nd of Shawal)
    assert is_holiday((2023, 4, 23, 'G')) is False
    assert is_holiday((2023, 4, 24, 'G')) is False

    assert is_holiday((2023, 4, 2, 'G')) is True


def test_holiday_occasion_unknown_calendar():
    with raises(ValueError, match="unknown calendar='Z'"):
        # noinspection PyTypeChecker
        is_holiday((1402, 2, 3, 'Z'))


def test_holiday_occasion_from_jdate():
    # In reality, this was NOT a holiday in Iran (30st of Ramazan)
    assert is_holiday(jdate(1402, 2, 1)) is True
    assert is_holiday(jdatetime(1402, 2, 2, 23, 59)) is True
    # In reality, this WAS a holiday in Iran (2nd of Shawal)
    assert is_holiday(jdatetime(1402, 2, 3, 0)) is False
    assert is_holiday(jdate(1402, 2, 4)) is False
    assert is_holiday(jdatetime(1402, 1, 13)) is True


def test_holiday_occasion_gregorian():
    assert is_holiday(date(2023, 4, 21)) is True
    assert is_holiday(datetime(2023, 4, 22)) is True
    # In reality, this WAS a holiday in Iran (2nd of Shawal)
    assert is_holiday(date(2023, 4, 23)) is False
    assert is_holiday(datetime(2023, 4, 24, 10)) is False

    assert is_holiday(date(2023, 4, 2)) is True


def test_holiday_occasion_hijri():
    with raises(ValueError):
        # Hijri does not allow 30-day Ramadan in this year, but in Iran
        # Ramadan had 30 days.
        Hijri(1444, 9, 30)

    r29 = Hijri(1444, 9, 29)
    assert r29.weekday() == 3  # Thursday
    assert is_holiday(r29) is False
    assert is_holiday(Hijri(1444, 10, 1)) is True
    assert is_holiday(Hijri(1444, 10, 2)) is True
    assert is_holiday(Hijri(1444, 10, 3)) is False

    assert is_holiday(Hijri(1444, 9, 11)) is True


def test_holiday_occasion_lunar_calendar():
    assert is_holiday((1444, 9, 29, 'L')) is False
    assert is_holiday((1444, 10, 1, 'L')) is True
    assert is_holiday((1444, 10, 2, 'L')) is True
    assert is_holiday((1444, 10, 3, 'L')) is False

    assert is_holiday((1444, 9, 11, 'L')) is True


def test_set_weekend():
    date = (2024, 2, 5, 'G')  # a non-holiday Monday
    assert is_workday(date) is True
    assert is_workday(date, weekend=(0,)) is False
    set_default_weekend((0,))
    assert is_workday(date) is False
