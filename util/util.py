import datetime

#our f_dst resolution (for now) is to handle all time objects as offset naive
def now():
    return datetime.datetime.now()