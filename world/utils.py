"""
Utilities to get things going

"""

from evennia.utils.search import search_object
from world import constants
import math

#Space objects and others

def SpaceObj(x):
    obj = search_object(x)[0]
    if (obj.type == constants.SDB_ATTR_NAME):
        return constants.SHIP_ATTR_NAME
    elif (obj.type == constants.MISSILE_ATTR_NAME):
        return constants.MISSILE_ATTR_NAME
    elif (obj.type == CONSOLE_USER_ATTR_NAME):
        return constants.CONSOLE_USER_ATTR_NAME
    return constants.SPACE_ATTR_NAME


#Distances

def ly2pc(dist):
    return (dist * constants.LIGHTYEAR / constants.PARSEC)

def pc2ly(dist):
    return (dist * constants.PARSEC / constants.LIGHTYEAR)

def ly2su(dist):
    return (dist * constants.LIGHTYEAR)

def pc2su(dist):
    return (dist * constants.PARSEC)

def su2ly(dist):
    return (dist / constants.LIGHTYEAR)

def su2pc(dist):
    return (dist / constants.PARSEC)
    
#Bearings

def xy2bearing(x,y):
    if (y == 0.0):
        if (x == 0.0):
            return 0.0
        elif (x > 0.0):
            return 0.0
        else:
            return 180.0
    elif (x == 0.0):
        if (y > 0.0):
            return 90.0
        else:
            return 270.0
    elif(x > 0.0):
        if (y > 0.0):
            return math.atan(y / x) * 180.0 / math.pi
        else:
            return math.atan(y / x) * 180.0 / math.pi + 360.0
    elif(x < 0.0):
        return math.atan(y / x) * 180 / math.pi + 180.0
    return 0.0

def xyz2elevation(x,y,z):
    r = math.sqrt(x * x + y * y)
    
    if (r == 0.0):
        if (z == 0.0):
            return 0.0
        elif(z > 0.0):
            return 90.0
        else:
            return 270.0
    elif(z > 0.0):
        return math.atan(z / r) * 180.0 / math.pi
    elif(z < 0.0):
        return math.atan(z / r) * 180 / math.pi + 360
    else:
        return 0.0
        
def xyz2range(xa,ya,za,xb,yb,zb):
    x = xb - xa
    y = yb - ya
    z = zb - za
    return math.sqrt(x * x + y * y + z * z)

def xyz2vis(x,y,z):
    px = x / constants.PARSEC
    py = y / constants.PARSEC
    pz = z / constants.PARSEC
    dx = math.fabs(px - math.round(px / 100.0) * 100.0)
    dy = math.fabs(px - math.round(py / 100.0) * 100.0)
    dz = math.fabs(px - math.round(pz / 100.0) * 100.0)
    
    vis = 1.1 - (1.0 / (1.0 + dx * dx + dy * dy + dz * dz))
    
    if (vis < 0.0):
        return 0.0
    elif(vis > 1.0):
        return 1.0
    else:
        return vis
        
def sdb2bearing(obj1,obj2):
   x = obj2.db.coords["x"] - obj1.db.coords["x"]
   y = obj2.db.coords["x"] - obj1.db.coords["y"]
   return xy2bearing(x,y)
   
def sdb2elevation(obj1,obj2):
    x = obj2.db.coords["x"] - obj1.db.coords["x"]
    y = obj2.db.coords["y"] - obj1.db.coords["y"]
    z = obj2.db.coords["z"] - obj1.db.coords["z"]
    return xyz2elevation(x,y,z)

def sdb2range(obj1,obj2):
    return xyz2range(obj1.db.coords["x"],obj1.db.coords["y"],obj1.db.coords["z"],obj2.db.coords["x"],obj2.db.coords["y"],obj2.db.coords["z"])
    
def sdb2arc(obj1,obj2):
    firing_arc = 0
    x = obj2.db.coords["x"] - obj1.db.coords["x"]
    y = obj2.db.coords["y"] - obj1.db.coords["y"]
    z = obj2.db.coords["z"] - obj1.db.coords["z"]
    r = math.sqrt(x * x + y * y + z * z)
    
    if (r == 0.0):
        firing_arc = 63
    else:
        v1 = (x * obj1.db.course["d"][0][0] + y * obj1.db.course["d"][0][1] + z * obj1.db.course["d"][0][2]) / r / math.sqrt(obj1.db.course["d"][0][0] * obj1.db.course["d"][0][0] + obj1.db.course["d"][0][1] * obj1.db.course["d"][0][1] + obj1.db.course["d"][0][2] * obj1.db.course["d"][0][2])
        v2 = (x * obj1.db.course["d"][1][0] + y * obj1.db.course["d"][1][1] + z * obj1.db.course["d"][1][2]) / r / math.sqrt(obj1.db.course["d"][1][0] * obj1.db.course["d"][1][0] + obj1.db.course["d"][1][1] * obj1.db.course["d"][0][1] + obj1.db.course["d"][1][2] * obj1.db.course["d"][1][2])
        v3 = (x * obj1.db.course["d"][2][0] + y * obj1.db.course["d"][2][1] + z * obj1.db.course["d"][2][2]) / r / math.sqrt(obj1.db.course["d"][2][0] * obj1.db.course["d"][2][0] + obj1.db.course["d"][2][1] * obj1.db.course["d"][0][1] + obj1.db.course["d"][2][2] * obj1.db.course["d"][2][2])
        if (v1 > 1.0):
            v1 = 1.0
        elif(v1 < -1.0):
            v1 = -1.0
        if (v2 > 1.0):
            v2 = 1.0
        elif(v2 < -1.0):
            v2 = -1.0
        if (v3 > 1.0):
            v3 = 1.0
        elif(v3 < -1.0):
            v3 = -1.0
        forward_arc = math.acos(v1) * 180 / math.pi
        starboard_arc = math.acos(v2) * 180 / math.pi
        up_arc = math.acos(v3) * 180 / math.pi
        
        if (forward_arc < 89.0):
            firing_arc += 1
        elif(forward_arc > 91.0):
            firing_arc += 4
        else:
            firing_arc += 5
        
        if (starboard_arc < 89.0):
            firing_arc += 2
        elif(forward_arc > 91.0):
            firing_arc += 8
        else:
            firing_arc += 10
        
        if (up_arc < 89.0):
            firing_arc += 16
        elif(up_arc > 91.0):
            firing_arc += 32
        else:
            firing_arc += 48
    return firing_arc

def sdb2true_speed(obj):

    v1 = math.fabs(obj.db.move["out"])

    if (obj.db.status["tractored"]):
        obj_tract = search_object(obj.db.status["tractored"])[0]
        v2 = math.fabs(obj_tract.db.move["out"]);
        if (v1 > v2):
            v1 = v1 
        else:
            v1 = v2
    elif(obj.db.status["tractoring"]):      
        obj_tract = search_object(obj.db.status["tractoring"])[0]
        v2 = math.fabs(obj_tract.db.move["out"]);
        if (v1 > v2):
            v1 = v1
        else: 
            v1 = v2
        
    return v1

def contact2sdb(obj,c):
    for i in range(int(obj.db.sensor["contacts"])):
        if (c == obj.db.slist["num"][i]):
            return (obj.db.slist["key"][i])
            break
    return constants.SENSOR_FAIL


def sdb2contact(obj,s):
    for i in range(int(obj.db.sensor["contacts"])):
        if (s.name == obj.db.slist["key"][i]):
            return (obj.db.slist["num"][i])
            break
    return constants.SENSOR_FAIL

def contact2slist(obj,c):
    for i in range(int(obj.db.sensor["contacts"])):
        if (c == obj.db.slist["num"][i]):
            return i
            break
    return constants.SENSOR_FAIL

def sdb2slist(obj,s):
    for i in range(int(obj.db.sensor["contacts"])):
        if (s == obj.db.slist["key"][i]):
            return i
            break
    return constants.SENSOR_FAIL

def sdb2shield(n1,n2):
    obj1 = search_object(n1)[0]
    obj2 = search_object(n2)[0]
    
    x = obj2.db.coords["x"] - obj1.db.coords["x"]
    y = obj2.db.coords["y"] - obj1.db.coords["y"]
    z = obj2.db.coords["z"] - obj1.db.coords["z"]
    r = math.sqrt(x * x + y * y + z * z)
    
    if (r == 0.0):
        return 0
    else:
        v1 = (x * obj1.db.course["d"][0][0] + y * obj1.db.course["d"][0][1] + z * obj1.db.course["d"][0][2]) / r / math.sqrt(obj1.db.course["d"][0][0] * obj1.db.course["d"][0][0] + obj1.db.course["d"][0][1] * obj1.db.course["d"][0][1] + obj1.db.course["d"][0][2] * obj1.db.course["d"][0][2])
        v2 = (x * obj1.db.course["d"][1][0] + y * obj1.db.course["d"][1][1] + z * obj1.db.course["d"][1][2]) / r / math.sqrt(obj1.db.course["d"][1][0] * obj1.db.course["d"][1][0] + obj1.db.course["d"][1][1] * obj1.db.course["d"][0][1] + obj1.db.course["d"][1][2] * obj1.db.course["d"][1][2])
        v3 = (x * obj1.db.course["d"][2][0] + y * obj1.db.course["d"][2][1] + z * obj1.db.course["d"][2][2]) / r / math.sqrt(obj1.db.course["d"][2][0] * obj1.db.course["d"][2][0] + obj1.db.course["d"][2][1] * obj1.db.course["d"][0][1] + obj1.db.course["d"][2][2] * obj1.db.course["d"][2][2])
        if (v1 > 1.0):
            v1 = 1.0
        elif(v1 < -1.0):
            v1 = -1.0
        if (v2 > 1.0):
            v2 = 1.0
        elif(v2 < -1.0):
            v2 = -1.0
        if (v3 > 1.0):
            v3 = 1.0
        elif(v3 < -1.0):
            v3 = -1.0
        forward_arc = math.acos(v1) * 180 / math.pi
        starboard_arc = math.acos(v2) * 180 / math.pi
        up_arc = math.acos(v3) * 180 / math.pi
        
        if (up_arc < 45.0):
            return 4
        elif(up_arc > 135.0):
            return 5
        elif(starboard_arc < 60.0):
            return 1
        elif(starboard_arc > 120.0):
            return 3
        elif(forward_arc > 90.0):
            return 2
        else:
            return 0
    return 0

def arc_check(contact, weapon):
    x = (contact & weapon)
    if (((x & 16) or (x & 32)) and ((x & 1) or (x & 4)) and ((x & 2) or (x & 8))):
        return x
    else:
        return ARC_FAIL

def get_empty_sdb():
#NOT IMPLEMENTED!
    return VACANCY_FAIL    

def sdb2max_antimatter(obj):
    return obj.db.move["ratio"] * obj.db.tech["ly_range"] * 320000000.0
    
def sdb2max_deuterium(obj):
    return obj.db.move["ratio"] * obj.db.tech["ly_range"] * 640000000.0
    
def sdb2max_reserves(obj):
    return obj.db.batt["gw"] * 3600.0

def sdb2language(obj):
    return obj.db.language
    
def sdb2max_warp(obj):
    a = obj.db.move["ratio"]
    p = (0.99 * obj.db.power["main"]) + (0.01 * obj.db.power["total"] * obj.db.alloc["movement"])
    
    if (a <= 0.0):
        return 0.0
    if (p <= 0.0):
        return 0.0
    if (obj.db.status["tractoring"] is not None):
        obj_tractoring = search_object(obj.db.status["tractoring"])[0]
        a *= (obj.db.structure["displacement"] + obj_tractoring.db.structure["displacement"] + 0.1) / (obj.db.structure["displacement"] + 0.1)
    elif(obj.db.status["tractored"] is not None):
        obj_tractored = search_object(obj.db.status["tractored"])[0]
        a *= (obj.db.structure.displacement + obj_tractored.structure["displacement"] + 0.1) / (obj.db.structure["displacement"] + 0.1)
    
    a = math.sqrt(10.0 * p/a)
    if (a < 1.0):
        return 0.0
    else:
        return a / 2
        
def sdb2max_impulse(x):
    obj = search_object(x)[0]
    
    a = obj.db.move["ratio"]
    p = (0.9 * obj.db.power["aux"]) + (0.1 * obj.db.power["total"] * obj.db.alloc["movement"])
    
    if (a <= 0.0):
        return 0.0
    if (p <= 0.0):
        return 0.0
    if (obj.db.status["tractoring"] is not None):
        obj_tractoring = search_object(obj.db.status["tractoring"])[0]
        a *= (obj.db.structure["displacement"] + obj_tractoring.structure.displacement + 0.1) / (ob.dbj.structure["displacement"] + 0.1)
    elif(obj.db.status["tractored"] is not None):
        obj_tractored = search_object(obj.db.status["tractored"])[0]
        a *= (obj.db.structure.displacement + obj_tractored.db.structure["displacement"] + 0.1) / (obj.db.structure["displacement"] + 0.1)
    
    a = 1.0 - 0.5 * a / p
    if (a <= 0.0 or a >= 1.0):
        return 0.0
    else:
        return a
        
def sdb2cruise_warp(x):
    obj = search_object(x)[0]
    
    if (obj.db.move["ratio"] <= 0.0):
        return 0.0
    if (obj.db.main["gw"] <= 0.0):
        return 0.0
    if (obj.db.engine["warp_damage"] <= 0.0):
        return 0.0
    
    a = sqrt(10.0 * obj.db.main["gw"]  / obj.db.move["ratio"])
    if (a < 1.0):
        return 0.0
        
    a *= obj.db.engine["warp_damage"]
    if (a < 1.0):
        return 0.0
    else:
        return a/2
        
def sdb2cruise_impulse(x):
    obj = search_object(x)[0]
    
    if (obj.db.move["ratio"] <= 0.0):
        return 0.0
    if (obj.db.aux["gw"] <= 0.0):
        return 0.0
    if (obj.db.engine["impulse_damage"] <= 0.0):
        return 0.0
    
    a = 1.0 - 0.5 * obj.db.move["ratio"] / obj.db.aux["gw"]
    if (a <= 0.0 or a >= 1.0):
        return 0.0
    a *= obj.db.engine["impulse_damage"]
    if (a < 0.0):
        return 0.0
    else:
        return a

def sdb2ecm_lrs(x):
    obj = search_object(x)[0]
    
    if (obj.db.sensor["ew_active"]):
        return math.sqrt(1.0 + obj.db.power["total"] * obj.db.alloc["ecm"] * obj.db.sensor["ew_damage"] * obj.db.tech["sensors"] / 10.0)
    else:
        return 1.0
        
def sdb2eccm_lrs(x):
    obj = search_object(x)[0]
    
    if (obj.db.sensor["ew_active"]):
        return math.sqrt(1.0 + obj.db.power["total"] * obj.db.alloc["eccm"] * obj.db.sensor["ew_damage"] * obj.db.tech["sensors"] / 10.0)
    else:
        return 1.0
        
def sdb2ecm_srs(x):
    obj = search_object(x)[0]
    
    if (obj.db.sensor["ew_active"]):
        return math.sqrt(1.0 + obj.db.power["total"] * obj.db.alloc["ecm"] * obj.db.sensor["ew_damage"] * obj.db.tech["sensors"])
    else:
        return 1.0
        
def sdb2ecm_srs(x):
    obj = search_object(x)[0]
    
    if (obj.db.sensor["ew_active"]):
        return math.sqrt(1.0 + obj.db.power["total"] * obj.db.alloc["eccm"] * obj.db.sensor["ew_damage"] * obj.db.tech["sensors"])
    else:
        return 1.0
        
def sdb2dissipation(obj, shield):
    d = 0.0
    
    if (obj.db.shield[shield]["active"] and obj.db.shield[shield]["damage"] > 0.0):
        d = (2 - math.pow(2, (1 - obj.db.alloc["shield"][shield] * obj.db.power["total"] * obj.db.shield[shield]["damage"] * obj.db.shield["ratio"] * obj.db.shield["visibility"] / obj.db.shield["maximum"]))) * obj.db.shield["maximum"]
        if (d > 1.0):
            return d
        else:
            return 0.0
    else:
        return 0.0
        
def xyz2cochranes(x,y,z):
    px = x / constants.PARSEC
    py = y / constants.PARSEC
    pz = z / constants.PARSEC
    r = (px * px + py * py) / 256000000.0 + (pz * pz) / 240000.0
    
    if (r < 1.0):
        return ((1.0 - r) / 0.671223 * constants.COCHRANE) + 1.0
    else:
        return 1.0
        
def sdb2angular(n1, n2):
    obj1 = search_object(n1)[0]
    obj2 = search_object(n2)[0]
    
    a[0] = obj2.db.coords["x"] - obj1.db.coords["x"]
    a[1] = obj2.db.coords["y"] - obj1.db.coords["y"]
    a[2] = obj2.db.coords["z"] - obj1.db.coords["z"]
    
    b[0] = (obj2.db.move["v"] * obj2.db.course["d"][0][0]) - (obj1.db.move["v"] * obj1.db.course["d"][0][0]) + a[0]
    b[1] = (obj2.db.move["v"] * obj2.db.course["d"][0][1]) - (obj1.db.move["v"] * obj1.db.course["d"][0][1]) + a[1]
    b[2] = (obj2.db.move["v"] * obj2.db.course["d"][0][2]) - (obj1.db.move["v"] * obj1.db.course["d"][0][2]) + a[2]
    
    dot = a[0] * b[0] + a[1] * b[1] + a[2] * b[2]
    mag = math.sqrt((a[0] * a[0] + a[1] * a[1] + a[2] * a[2]) * (b[0] * b[0] + b[1] * b[1] + b[2] * b[2]))
    if (mag == 0):
        return 0
    x = dot / mag
    if (x > 1.0):
        x = 1.0
    elif (x < -1.0):
        x = -1.0
    return math.fabs(math.acos(x) * 180 / math.pi)
    
def sdb2friendly(n1,n2):
    obj1 = search_object(n1)[0]
    obj2 = search_object(n2)[0]
    
    if (math.fabs(obj1.db.iff["frequency"] - obj2.db.iff["frequency"] ) > 0.001):
        return 1
    else:
        return 0