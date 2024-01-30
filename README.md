``iranholidays`` is a small python library that provides functions to check if a date is a holiday in Iran or not. 

**Warning:** For Islamic holidays, like Eid al-Fitr, the calculation may be off by a day or two since those events depend on seeing the moon by naked eye and cannot be predicted accurately by computers.

Usage:

```python
from iranholidays import holiday_occasion

assert (
    holiday_occasion(2024, 4, 1, 'G')  # Gregorian
    == holiday_occasion(1403, 1, 13, 'S')  # Solar
    == 'Sizdah Be-dar'
)

assert holiday_occasion(1445, 9, 21, 'L') == 'Martyrdom of Ali'  # Lunar

# holiday_occasion returns None for non-holidays
assert holiday_occasion(1403, 1, 14, 'S') is None
```

In case you have a date object from the following libraries, you can check it directly using one of the `hiliday_occasion_from_*` functions:
```python
from datetime import date

from hijri_converter import Hijri
from jdatetime import date as jdate

from iranholidays import (
    holiday_occasion_from_date,
    holiday_occasion_from_hijri,
    holiday_occasion_from_jdate,
)

assert (
    holiday_occasion_from_date(date(2024, 4, 1))
    == holiday_occasion_from_jdate(jdate(1403, 1, 13))
    == 'Sizdah Be-dar'
)
assert holiday_occasion_from_hijri(Hijri(1445, 9, 21)) == 'Martyrdom of Ali'
```
