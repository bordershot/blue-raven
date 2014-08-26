# TODO:
# So far, only zero argument commands are supported.  Many commands
# take (for example) a list of meter IDs.  We should provide methods
# to make that simple.

def _prepare(name, *tags):
    s = "<Command>\n" + "  <Name>" + name + "</Name>\n" + _prepare_tags(tags) +"</Command>\n"
    return s;

def _prepare_tags(tags):
    s = ""
    for pair in tags:
        s += "  " + _prepare_tag(pair)
    return s
    
def _prepare_tag(pair):
    name = pair[0]
    value = pair[1]
    return "<" + name + ">" + str(value) + "</" + name + ">\n"
    
    
# ================================================================
# RAVEn feature

# Command: INITIALIZE
def initialize():
    return _prepare("initialize")
    
# Command: RESTART
def restart():
    return _prepare("restart")

# Command: FACTORY_RESET
def factory_reset():
    return _prepare("factory_reset")

# Command: GET_CONNECTION_STATUS
def get_connection_status():
    return _prepare("get_connection_status")

# Command: GET_DEVICE_INFO
def get_device_info():
    return _prepare("get_device_info")

# Command: GET_SCHEDULE
# TODO

# Command: SET_SCHEDULE
# TODO

# Command: SET_SCHEDULE_DEFAULT
# TODO

# Command: GET_METER_LIST
def get_meter_list():
    return _prepare("get_meter_list")

# ================================================================
# Meter Feature

# Command: GET_METER_INFO
# TODO

# Command: GET_NETWORK_INFO
def get_network_info():
    return _prepare("get_network_info")

# Command: SET_METER_INFO
# TODO

# ================================================================
# Time Feature

# Command: GET_TIME
# TODO

# ================================================================
# Message Feature

# Command: GET_MESSAGE
# TODO

# Command: CONFIRM_MESSAGE
# TODO

# ================================================================
# Price Feature

# Command: GET_CURRENT_PRICE
# TODO

# Command: SET_CURRENT_PRICE
# TODO

# ================================================================
# Simple Metering Feature

# Command: GET_INSTANTANEOUS_DEMAND
# TODO

# Command: GET_CURRENT_SUMMATION_DELIVERED
# TODO

# Command: GET_CURRENT_PERIOD_USAGE
# TODO

# Command: GET_LAST_PERIOD_USAGE
# TODO

# Command: CLOSE_CURRENT_PERIOD
# TODO

# Command: SET_FAST_POLL
# TODO

# Command: GET_PROFILE_DATA
# TODO
