"""
All things to make it look better
"""
from world import constants,utils
from evennia.utils.search import search_object
import math

def unparse_power(value):
    buffer = "None"
    if (value == 0.0):
        buffer = "None"
    elif(value < 0.001):
        buffer = "{:.3f}".format(value * 1000000.0) + " KW"
    elif(value < 1.0):
        buffer = "{:.3f}".format(value * 1000.0) + " MW"
    elif(value < 1000.0):
        buffer = "{:.3f}".format(value) + " GW"
    elif(value < 1000000.0):
        buffer = "{:.3f}".format(value / 1000.0) + " TW"
    else:
        buffer = "{:.3f}".format(value / 1000000.0) + " PW"
    return buffer

def unparse_class(obj):
    return str(obj.__class__.__name__).replace("_"," ")

def unparse_type(obj):
    return str(constants.type_name[obj.db.structure["type"]])

def unparse_percent(value):
   return "{:.0f}".format(value * 100) + "%"

def unparse_range(value):
    if (value > 999.9 * constants.PARSEC):
        return "[{:5.0f}]".format(value / constants.PARSEC)
    elif (value > 99.99 * constants.PARSEC):
        return "[{:5.1f}]".format(value / constants.PARSEC)
    elif (value > 9.999 * constants.PARSEC):
        return "[{:5.2f}]".format(value / constants.PARSEC)
    elif (value > 9999999.0):
        return"[{:5.3f}]".format(value / constants.PARSEC)
    elif (value > 99999.9):
        return"{:7.0f}".format(value)
    elif (value > 9999.99):
        return "{:7.1f}".format(value)
    elif (value > 999.999):
        return "{:7.2f}".format(value)
    elif (value > 99.9999):
        return "{:7.3f}".format(value)
    elif (value > 9.99999):
        return "{:7.4f}".format(value)
    else:
        return "{:7.5f}".format(value)

def unparse_distance(value):
    type = "SU"
    if (value > 9999999.0):
        type = "PC"
    return unparse_range(value) + " " + type

def unparse_freq(value):
    return "{:.3f}".format(value) + " GHz"

def unparse_percent_3(value):
   return "{:.3f}".format(value * 100) + "%"

def unparse_quadrant(obj):
    if(obj.db.move["quadrant"] < 0 or obj.db.move["quadrant"] >= constants.MAX_QUADRANT_NAME):
        return "#-1 BAD QUADRANT"
    else:
        return constants.quadrant_name[obj.db.move["quadrant"]]

def unparse_empire(obj):
    if (obj.db.move["empire"] == ''):
        return "Neutral"
    else:
        empire = search_object(obj.db.move["empire"])[0]
        if(empire is not None):
            return empire.db.sdesc
        else:
            return "#-1 BAD TERRITORY"

def unparse_course(obj):
    if (obj.db.course["roll_out"] != 0.0):
        return "{:.2f}".format(obj.db.course["yaw_out"]) + " " + "{:.2f}".format(obj.db.course["pitch_out"]) + "{:.2f}".format(obj.db.course["roll_out"])
    else:
        return "{:.3f}".format(obj.db.course["yaw_out"]) + " " + "{:.3f}".format(obj.db.course["pitch_out"])

def unparse_speed(value):
    
    if (value > 0.0):
        if (value >= 100.0):
            return (f'w{value:5.1f}')
        elif(value >= 10.0):
            return (f'w{value:5.2f}')
        elif(value >= 1.0):
            return (f'w{value:5.3f}')
        elif(value >= 0.1):
            return (f'{value*100:5.2f}i')
        else:
            return (f'{value*100:5.3f}i')
    elif(value < 0.0):
        if (value <= -100.0):
            return (f'w{value:5.0f}')
        elif(value <= -10.0):
            return (f'w{value:5.1f}')
        elif(value <= -1.0):
            return (f'w{value:5.2f}')
        elif(value <= -0.1):
            return (f'{value*100:5.1f}i')
        else:
            return (f'{value*100:5.2f}i')
    else:
        return "None"

def unparse_bearing(obj1, obj2):
    return f'{utils.sdb2bearing(obj1,obj2):.3f} {utils.sdb2elevation(obj1,obj2):.3f}'

def unparse_movement(obj):
    if (obj.db.move["out"] == 0.0):
        return "Stationary"
    elif(math.fabs(obj.db.move["out"]) >= 1.0):
        return "Warp " + "{:.0f}".format(obj.db.move["out"])
    else:
        return "{:.3f}".format(obj.db.move["out"] * 100) + "% Impulse"

def unparse_velocity(obj):
    obj_x = utils.name2sdb(obj.db.status["tractored"])
    if (obj_x == constants.SENSOR_FAIL):
        obj_x = utils.name2sdb(obj.db.status["tractoring"])
    if (obj.db.status["tractored"]):
        x = obj.db.status["tractored"]
    elif(obj.db.status["tractoring"]):
        x = obj.db.status["tractored"]
    
    if (math.fabs(obj.db.move["out"]) >= 1.0):
        v = obj.db.move["v"] * obj.db.move["cochranes"]
    else:
        v = obj.db.move["v"]
    
    if (obj_x != constants.SENSOR_FAIL):
        if (math.fabs(obj_x.db.move["out"]) >= 1.0):
            vx = obj_x.db.move["v"] * obj_x.db.move["cochranes"]
        else:
            vx = obj_x.db.move["v"]
        dx = v * obj.db.course["d"][0][0] + vx * obj_x.db.course["d"][0][0]
        dy = v * obj.db.course["d"][0][1] + vx * obj_x.db.course["d"][0][1]
        dz = v * obj.db.course["d"][0][2] + vx * obj_x.db.course["d"][0][2]
        v = math.sqrt(dx * dx + dy * dy + dz * dz)
        
    if (v == 0):
        return "Stationary"
    else:
        return unparse_distance(math.fabs(v)) + "/sec"
   
def unparse_damage(value):
    if(value == 1.0):
        return constants.damage_name[0]
    elif(value > 0.95):
        return constants.damage_name[1]
    elif(value > 0.90):
        return constants.damage_name[2]
    elif(value > 0.75):
        return constants.damage_name[3]
    elif(value > 0.5):
        return constants.damage_name[4]
    elif(value > 0.25):
        return constants.damage_name[5]
    elif(value > 0.0):
        return constants.damage_name[6]
    elif(value > -1.0):
        return constants.damage_name[7]
    else:
        return constants.damage_name[8]

def unparse_cargo(value):
    if (value > 0):
        return "{:.0f}".format(value) + " mt"
    else:
        return "None"

def unparse_contact(obj, obj2):
    if (obj == obj2):
        return obj.name
    if (obj.location == obj2):
        return obj2.name
    if (obj == obj2.location):
        return obj2.name
        
    slist = utils.sdb2list(obj,obj2)
    if (slist == constants.SENSOR_FAIL):
        return "unknown contact"
    else:
        if (obj.db.slist[slist]["lev"] >= 0.5 and not obj.db.cloak["active"]):
            return  obj2.name + " (" + unparse_integer(utils.sdb2contact(obj, obj2)) + ")"
        elif(obj.db.slist[slist]["lev"] >= 0.25 and not obj.db.cloak["active"]):
            return unparse_class(obj2) + " class (" + unparse_integer(utils.sdb2contact(obj, obj2)) + ")"
        else:
            return "contact (" + unparse_integer(utils.sdb2contact(obj, obj2)) + ")"

def unparse_integer(value):
    return (str(value))

def unparse_arc(value):
    buffer = ""
    if (value & 1):
        buffer += "F"
    if (value & 4):
        buffer += "A"
    if (value & 8):
        buffer += "P"
    if (value & 2):
        buffer += "S"
    if (value & 16):
        buffer += "U"
    if (value & 32):
        buffer += "D"
    return buffer

def unparse_shield(value):
    return constants.shield_name[value]
    
def unparse_identity(obj1,obj2):
    if (obj1.name == obj2.name):
        return obj1.name
    if (obj1.location == obj2):
        return obj2.name
    if (obj1 == obj2.location):
        return obj2.name
    
    slist = utils.sdb2slist(obj1,obj2)
    if (slist == constants.SENSOR_FAIL):
        return "unknown contact"
    else:
        if(obj1.slist["lev"][slist] >= 0.5 and obj2.db.cloak["active"] == 0):
            return obj2.name + " (" + str(int(utils.sdb2contact(obj1,obj2))) + ")"
        elif(obj1.slist["lev"][slist] >= 0.25 and obj2.db.cloak["active"] == 0):
            return unparse_class(obj2) + " class (" + str(int(utils.sdb2contact(obj1,obj2))) + ")"
        else:
            return "contact (" + str(int(utils.sdb2contact(obj1,obj2))) + ")"

def unparse_beam(value):
    if(value < 0 or value > constants.MAX_BEAM_NAME):
        return constants.beam_name[0]
    else:
        return constants.beam_name[value]

def unparse_missile(value):
    if(value < 0 or value > constants.MAX_MISSILE_NAME):
        return constants.missile_name[0]
    else:
        return constants.missile_name[value]