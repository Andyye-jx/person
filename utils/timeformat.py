import time
from datetime import datetime


def time_to_datetime(timestamp):
    """
    时间戳转为datetime对象
    return: datetime_obj
    """
    return datetime.fromtimestamp(timestamp)


def time_to_localtime(timestamp, fmt="%Y-%m-%d %H:%M:%S"):
    """
    时间戳转换为本地时间字符串
    return: str
    """
    if isinstance(timestamp, str):
        return timestamp
    return time.strftime(fmt, time.localtime(timestamp))


def datetime_to_time(dt, fmt="%Y-%m-%d %H:%M:%S"):
    """
    datetime时间转为时间戳
    return: int
    """
    return int(time.mktime(time.strptime(dt.strftime(fmt), fmt)))


def strdatetime_to_time(str_time, fmt="%Y-%m-%d %H:%M:%S"):
    """
    字符串时间转为时间戳
    return: int
    """
    return int(time.mktime(time.strptime(str_time, fmt)))


def strtime_to_datetime(str_time, fmt="%Y-%m-%d %H:%M:%S"):
    """
    字符串时间转换datetime对象
    return: datetime_obj
    """
    return datetime.strptime(str_time, fmt)


def strtime_to_date(str_time, fmt="-"):
    """
    时间字符串 转换 date对象
    2013-01-02 2013, 1, 2
    return: date_obj
    """
    y, m, d = str_time.split(fmt)
    return datetime.date(int(y), int(m), int(d))


def datetime_to_str(dt):
    """
    datetime对象 转换 字符串时间
    return: str
    """
    return str(dt)


def date_to_datetime(dt, fmt="%Y-%m-%d"):
    return datetime.strptime(str(dt), fmt)


def get_now_time(fmt="%Y-%m-%d %H:%M:%S"):
    return datetime.now().strftime(fmt)


def get_now_date(fmt="%Y-%m-%d"):
    return datetime.now().strftime(fmt)


def format_timestamp(stamp: int) -> int:
    """格式时间戳位数 10位数字"""
    n = len(str(stamp))
    return int(stamp / (10 ** (n - 10)))
