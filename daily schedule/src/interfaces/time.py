from src.interfaces.validate import Validate
from datetime import datetime
from typing import Union, Tuple
from calendar import monthrange


class Time(Validate):
    DAYS = ["lunedì", "martedì", "mercoledì", "giovedì", "venerdì", "sabato", "domenica"]
    MONTHS = ['gennaio', 'febbraio', 'marzo', 'aprile', 'maggio', 'giugno', 'luglio',
              'agosto', 'settembre', 'ottobre', 'novembre', 'dicembre']

    @staticmethod
    def get_wday(date: Union[Tuple[int, int, int], datetime]) -> int:
        if isinstance(date, tuple):
            date = datetime(*date)
        return date.timetuple().tm_wday

    @staticmethod
    def get_yday(date: Union[Tuple[int, int, int], datetime]) -> int:
        if isinstance(date, tuple):
            date = datetime(*date)
        return date.timetuple().tm_yday

    @classmethod
    def day_name(cls, day: int) -> str:
        cls.validate_params_ex(day, int)
        if not 0 <= day <= 6:
            raise ValueError(f"Day must be included between 0 and 6, {day} is invalid")
        return cls.DAYS[day].capitalize()

    @classmethod
    def month_name(cls, month: int) -> str:
        cls.validate_params_ex(month, int)
        if not 0 < month < 13:
            raise ValueError(f"Day must be included between 1 and 12, {month} is invalid")
        return cls.MONTHS[month - 1].capitalize()

    @classmethod
    def it_date(cls, date: Union[Tuple[int, int, int], datetime]) -> str:
        if isinstance(date, tuple):
            date = datetime(*date)
        day = date.day
        year = date.year
        day_name = cls.day_name(cls.get_wday(date))
        month_name = cls.month_name(date.month)
        return f"{day_name} {day} {month_name} {year}"

    @classmethod
    def process_string_date(cls, date: str) -> int:
        today = datetime.now().timetuple()
        match list(map(int, date.split('-'))):
            case [d]:
                if d < 1 or d > 366:
                    raise ValueError("Day out of range")
                td_day = today.tm_mday
                month_range = monthrange(today.tm_year, today.tm_mon)[1]
                if td_day <= d <= month_range:
                    return today.tm_yday - td_day + d
                elif d < td_day:
                    return today.tm_yday - td_day + month_range + d
                else:
                    return d
            case [d, m]:
                if d < 1 or d > 31:
                    raise ValueError("Day out of range")
                if m < 1 or m > 12:
                    raise ValueError("Month out of range")
                td_month = today.tm_mon
                td_day = today.tm_mday
                td_year = today.tm_year
                if m < td_month or d < td_day and m == td_month:
                    td_year += 1
                return datetime(td_year, m, d).timetuple().tm_yday
            case [d, m, y]:
                return datetime(y, m, d).timetuple().tm_yday
            case _:
                raise ValueError("Too many values to unpack")


if __name__ == '__main__':
    for i in range(7):
        print(Time.day_name(i))
