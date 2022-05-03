import util.const as const

def date_file_str(t):
    try:
        return t.astimezone(const.LTZ).strftime(const.DATE_FILE_FORMAT)
    except:
        return "inv_datetime"