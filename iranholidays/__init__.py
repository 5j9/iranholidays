from datetime import date as _date, datetime as _datetime
from typing import Literal as _Literal

from hijri_converter import Gregorian as _Gregorian, Hijri as _Hijri
from jdatetime import date as _jdate, datetime as _jdatetime
from jdatetime.jalali import GregorianToJalali as _G, JalaliToGregorian as _J

__version__ = '0.0.1'

SOLAR_HOLIDAYS = [
    None,
    {  # Farvardīn
        1: 'Nowruz',
        2: 'Nowruz',
        3: 'Nowruz',
        4: 'Nowruz',
        12: 'Islamic Republic Day',
        13: 'Sizdah Be-dar',
    },
    {  # 2: Ordībehešt
    },
    {  # 3: Khordād
        14: 'death of Ruhollah Khomeini',
        15: 'the 15 Khordad uprising',
    },
    {  # 4: Tīr
    },
    {  # 5: Mordād
    },
    {  # 6: Shahrīvar
    },
    {  # 7: Mehr
    },
    {  # 8: Ābān
    },
    {  # 9: Āzar
    },
    {  # 10: Dey
    },
    {  # 11: Bahman
        22: 'Islamic Revolution',
    },
    {  # 12: Esfand
        29: 'Nationalization of the Iranian oil industry',
        30: 'Nowruz',
    },
]

HIJRI_HOLIDAYS = [
    None,
    {  # 1: al-Muḥarram
        9: "Tasu'a",
        10: 'Ashura',
    },
    {  # 2: Ṣafar
        20: "Arba'een",
        28: 'Death of Muhammad, Martyrdom of Hasan ibn Ali',
        30: 'Martyrdom of Ali ibn Musa al-Rida',
    },
    {  # 3: Rabīʿ al-ʾAwwal
        8: 'Martyrdom of Hasan al-Askari',
        17: "Mawlid an-Nabi, Birth of Ja'far al-Sadiq",
    },
    {  # 4: Rabīʿ ath-Thānī
    },
    {  # 5: Jumādā al-ʾŪlā
    },
    {  # 6: Jumādā ath-Thāniyah
        3: 'Death of Fatima',
    },
    {  # 7: Rajab
        13: "Birth of Ja'far al-Sadiq",
        27: "Muhammad's first revelation",
    },
    {  # 8: Shaʿbān
        15: "Mid-Sha'ban",
    },
    {  # 9: Ramaḍān
        21: 'Martyrdom of Ali',
    },
    {  # 10: Shawwāl
        1: 'Eid al-Fitr',
        2: 'Eid al-Fitr',
        25: "Martyrdom of Ja'far al-Sadiq",
    },
    {  # 11: Ḏū al-Qaʿdah
    },
    {  # 12: Ḏū al-Ḥijjah
        10: 'Eid al-Adha',
        18: 'Eid al-Ghadir',
    },
]


def holiday_occasion_from_date(date: _date | _datetime) -> str | None:
    """Return a string describing the holiday or None.

    The first param should either be a date object or
    tuple[int, int, int, _Literal['S', 'L', 'G']].

    If a tuple, the first three items are year, month, and day, and the last
    item describes the calendar as follows:
        'S': Solar Hijri (official calendar of Iran)
        'L': Lunar Hijri (Umm al-Qura calendar)
        'G': Gregorian
    """
    if date.weekday() == 4:
        return 'Friday'
    year, month, day = date.year, date.month, date.day
    _, hm, hd = _Gregorian(year, month, day).to_hijri().datetuple()
    if (r := HIJRI_HOLIDAYS[hm].get(hd)) is not None:
        return r
    sy, sm, sd = _G(year, month, day).getJalaliList()
    return SOLAR_HOLIDAYS[sm].get(sd)


def holiday_occasion_from_jdate(date: _jdatetime | _jdate) -> str | None:
    if date.weekday() == 4:
        return 'Friday'
    month, day = date.month, date.day
    if (r := SOLAR_HOLIDAYS[month].get(day)) is not None:
        return r
    h = _Gregorian(*date.togregorian().timetuple()[:3]).to_hijri()
    hy, hm, hd = h.datetuple()
    return HIJRI_HOLIDAYS[hm].get(hd)


def holiday_occasion_from_hijri(date: _Hijri) -> str | None:
    if date.weekday() == 4:
        return 'Friday'
    month, day = date.month, date.day
    if (r := HIJRI_HOLIDAYS[month].get(day)) is not None:
        return r
    sy, sm, sd = _G(*date.to_gregorian().datetuple()).getJalaliList()
    if (r := SOLAR_HOLIDAYS[sm].get(sd)) is not None:
        return r


def holiday_occasion(
    year: int, month: int, day: int, calendar: _Literal['S', 'L', 'G']
) -> str | None:
    # no matter what calendar, three checks are performed:
    # * Being a Friday
    # * Being in SOLAR_HOLIDAYS
    # * Being in HIJRI_HOLIDAYS
    # The order of checks depends on the calendar.
    if calendar == 'S':
        if (r := SOLAR_HOLIDAYS[month].get(day)) is not None:
            return r
        gy, gm, gd = _J(year, month, day).getGregorianList()
        h = _Gregorian(gy, gm, gd).to_hijri()
        hy, hm, hd = h.datetuple()
        if (r := HIJRI_HOLIDAYS[hm].get(hd)) is not None:
            return r
        if _date(gy, gm, gd).weekday() == 4:
            return 'Friday'

    elif calendar == 'G':
        return holiday_occasion_from_date(_date(year, month, day))

    elif calendar == 'L':
        if (r := HIJRI_HOLIDAYS[month].get(day)) is not None:
            return r
        gy, gm, gd = _Hijri(year, month, day).to_gregorian().datetuple()
        if _date(gy, gm, gd).weekday() == 4:
            return 'Friday'
        sy, sm, sd = _G(gy, gm, gd).getJalaliList()
        if (r := SOLAR_HOLIDAYS[sm].get(sd)) is not None:
            return r

    else:
        raise ValueError(f'unknown {calendar=}')
