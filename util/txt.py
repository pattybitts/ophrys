import math, datetime

import util.const as const

def time_str(t):
    try:
        return t.astimezone(const.LTZ).strftime(const.TIME_FORMAT)
    except:
        return "inv_datetime"

def date_str(t):
    try:
        return t.astimezone(const.LTZ).strftime(const.DATE_FORMAT)
    except:
        return "inv_datetime"

def short_date(t):
    try:
        return t.astimezone(const.LTZ).strftime(const.SHORT_DATE)
    except:
        return "inv_datetime"

def date_file_str(t):
    try:
        return t.astimezone(const.LTZ).strftime(const.DATE_FILE_FORMAT)
    except:
        return "inv_datetime"    

def td_date_str(t):
    try:
        return t.astimezone(const.LTZ).strftime(const.TD_DATE_FORMAT)
    except:
        return "inv_datetime"

def delta_str(td):
    try:
        d = math.floor(td.total_seconds() / 24 / 60 / 60)
        td -= datetime.timedelta(days=d)
        h = math.floor(td.total_seconds() / 60 / 60)
        td -= datetime.timedelta(hours=h)
        m = math.floor(td.total_seconds() / 60)
        td -= datetime.timedelta(minutes=m)
        return "{d:02}:{h:02}:{m:02}:{s:>02.0f}".format(
            d=d,
            h=h,
            m=m,
            s=td.total_seconds()
        )
    except:
        return "inv_timedelta"