``iranholidays`` is a small python library that provides functions to check if a date is a holiday in Iran or not. 

**Warning:** For Islamic holidays, like Eid al-Fitr, the calculation may be off by a day or two since those events depend on seeing the moon by naked eye and cannot be predicted by computers.

Usage:

.. code-block:: python

    from iranholidays import is_holiday

    assert is_holiday((2024, 4, 1, 'G')) is True # Gregorian
    assert is_holiday((1403, 1, 13, 'S')) is True  # Solar
    assert is_holiday((1403, 1, 14, 'S')) is False
    assert is_holiday((1445, 9, 21, 'L')) is True # Lunar

In case you have a date object from the following libraries, you can check it directly using one of the ``is_workday_*`` functions:

.. code-block:: python

    from datetime import date

    from hijri_converter import Hijri
    from jdatetime import date as jdate

    from iranholidays import (
        is_workday_gregorian,
        is_workday_lunar,
        is_workday_solar,
    )

    assert is_workday_gregorian(date(2024, 4, 1), weekend=()) is False
    assert is_workday_solar(jdate(1403, 1, 13), weekend=()) is False
    assert is_workday_lunar(Hijri(1445, 9, 21), weekend=()) is False
    assert holiday_occasion_from_hijri() == 'Martyrdom of Ali'

``is_workday`` function checks if a date is a weekend. The default value for weekend parameter is ``(4,)`` which means Friday. Either pass a different value to ``weekend`` parameter to override it or use ``set_default_weekend`` function to change the default:

.. code-block:: python

    from iranholidays import is_workday, set_default_weekend
    date = (2024, 2, 15, 'G')  # a non-holiday Thursday
    assert is_workday(date) is True
    assert is_workday(date, weekend=(3, 4)) is False
    set_default_weekend((3, 4))  # set default weekends to Thursday and Friday
    assert is_workday(date) is False
