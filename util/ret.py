#this module is an atrocity and probably needs a ground-up rework

#Generic Returns
WARNING = 5 #something unexpected or unideal occured but the return ought to be clean
INCOMPLETE = 4 #process or object is running as expected, but some action is still needed
INIT = 3 #process or variable has been initialized but taken no significant actions
SUCCESS = 2 #process is completed and has no errors
TRUE = 1 #return is truthy, no other info
FALSE = -1 #return is falsy, no other info
ERROR = -2 #process has failed and should be aborted
NO_ACTION = -3 #no further action should be taken on object or within process
BAD_INPUT = -4 #the input provided was invalid
NOT_FOUND = -5 #as in, not found in search. not fatal in match
DUPLICATE = -6 #the action or creation attempted already exists
LIMITED = -7 #the query has failed because of a rate limt

STRINGS = {5: "WARNING", 4: "INCOMPLETE", 3: "INIT", 2: "SUCCESS", 1: "TRUE", \
    -1: "FALSE", -2: "ERROR", -3: "NO_ACTION", -4: "BAD_INPUT", -5: "NOT_FOUND", -6: "DUPLICATE", -7: "LIMITED"}

def success(ret):
    if ret is None: return False
    if not isinstance(ret, int): return True
    return ret > 0

def to_string(ret):
    if ret is None: return "None"
    if isinstance(ret, str): return "str: " + str(ret)
    if not isinstance(ret, int): return "obj: " + ret.__class__.__name__
    try:
        return STRINGS.get(ret)
    except:
        return "Unknown Code: " + str(ret)

def combine(ret1, ret2):
    return TRUE if success(ret1) and success(ret2) else FALSE