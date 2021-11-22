"""
Utilities to get things going

"""

import random
from evennia.utils.search import search_object
from world import constants,iterate
import math

#Space objects and others

def SpaceObj(x):
    obj = search_object(x)[0]
    if (obj.type == constants.SDB_ATTR_NAME):
        return constants.SHIP_ATTR_NAME
    elif (obj.type == constants.MISSILE_ATTR_NAME):
        return constants.MISSILE_ATTR_NAME
    elif (obj.type == constants.CONSOLE_USER_ATTR_NAME):
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
    dx = math.fabs(px - round(px / 100.0) * 100.0)
    dy = math.fabs(px - round(py / 100.0) * 100.0)
    dz = math.fabs(px - round(pz / 100.0) * 100.0)
    
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
        v2 = (x * obj1.db.course["d"][1][0] + y * obj1.db.course["d"][1][1] + z * obj1.db.course["d"][1][2]) / r / math.sqrt(obj1.db.course["d"][1][0] * obj1.db.course["d"][1][0] + obj1.db.course["d"][1][1] * obj1.db.course["d"][1][1] + obj1.db.course["d"][1][2] * obj1.db.course["d"][1][2])
        v3 = (x * obj1.db.course["d"][2][0] + y * obj1.db.course["d"][2][1] + z * obj1.db.course["d"][2][2]) / r / math.sqrt(obj1.db.course["d"][2][0] * obj1.db.course["d"][2][0] + obj1.db.course["d"][2][1] * obj1.db.course["d"][2][1] + obj1.db.course["d"][2][2] * obj1.db.course["d"][2][2])
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
        if (c == obj.db.slist[i]["num"]):
            return search_object(obj.db.slist[i]["key"])[0]
            break
    return constants.SENSOR_FAIL


def sdb2contact(obj,s):
    for i in range(int(obj.db.sensor["contacts"])):
        if (s.name == obj.db.slist[i]["key"]):
            return (obj.db.slist[i]["num"])
            break
    return constants.SENSOR_FAIL

def contact2slist(obj,c):
    for i in range(int(obj.db.sensor["contacts"])):
        if (c == obj.db.slist[i]["num"]):
            return i
            break
    return constants.SENSOR_FAIL

def sdb2slist(obj,s):
    for i in range(int(obj.db.sensor["contacts"])):
        if (s == obj.db.slist[i]["key"]):
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
        return constants.ARC_FAIL

def name2sdb(name):
    obj = search_object(name)
    if (len(obj) > 0):
        return obj[0]
    else:
        return constants.SENSOR_FAIL

def get_empty_sdb():
#NOT IMPLEMENTED!
    return constants.VACANCY_FAIL    

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
    if (obj.db.status["tractoring"]):
        obj_tractoring = search_object(obj.db.status["tractoring"])[0]
        a *= (obj.db.structure["displacement"] + obj_tractoring.db.structure["displacement"] + 0.1) / (obj.db.structure["displacement"] + 0.1)
    elif(obj.db.status["tractored"]):
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
    if (obj.db.status["tractoring"]):
        obj_tractoring = search_object(obj.db.status["tractoring"])[0]
        a *= (obj.db.structure["displacement"] + obj_tractoring.structure.displacement + 0.1) / (obj.db.structure["displacement"] + 0.1)
    elif(obj.db.status["tractored"]):
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
    
    a = math.sqrt(10.0 * obj.db.main["gw"]  / obj.db.move["ratio"])
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
    
    a = [0.0,0.0,0.0]
    b = [0.0,0.0,0.0]

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
        
def sdb2eccm_srs(obj):
    if (obj.db.sensor["ew_active"] == 1):
        return math.sqrt(1.0 + obj.db.power["total"] * obj.db.alloc["eccm"] * obj.db.sensor["ew_damage"] * obj.db.tech["sensors"])
    else:
        return 1.0

def debug_space(obj):
    """
    This is a script to clean up any issues with an object. 
    """
    bug = 1

    #objects
    if(obj.db.structure["type"] <= 0):
        obj.db.structure["type"] = 0
        bug = 0
    
    #location
    obj_x = search_object(obj.db.location)
    if (len(obj_x) >0):
        obj_x = obj_x[0]
        if(obj.db.location == obj_x.name):
            obj_x.db.location = obj.name

    #main
    if(obj.db.main["exist"] != 1 or obj.db.main["gw"] <= 0):
        obj.db.main["damage"] = 0.0
        obj.db.main["exist"] = 0
        obj.db.main["gw"] = 0.0
        obj.db.main["in"] = 0.0
        obj.db.main["out"] = 0.0
        obj.db.power["main"] = 0.0
    
    #aux
    if(obj.db.aux["exist"] != 1 or obj.db.aux["gw"] <= 0):
        obj.db.aux["damage"] = 0.0
        obj.db.aux["exist"] = 0
        obj.db.aux["gw"] = 0.0
        obj.db.aux["in"] = 0.0
        obj.db.aux["out"] = 0.0
        obj.db.power["aux"] = 0.0
    
    #batt
    if(obj.db.batt["exist"] != 1 or obj.db.batt["gw"] <= 0):
        obj.db.batt["damage"] = 0.0
        obj.db.batt["exist"] = 0
        obj.db.batt["gw"] = 0.0
        obj.db.batt["in"] = 0.0
        obj.db.batt["out"] = 0.0
        obj.db.fuel["reserves"] = 0.0
        obj.db.power["batt"] = 0.0
    
    #allocate
    if(obj.db.main["exist"] == 0 or obj.db.aux["exist"] == 0 or obj.db.batt["exist"] == 0):
        obj.db.alloc["helm"] = 0.0
        obj.db.alloc["tactical"] = 0.0
        obj.db.alloc["operations"] = 0.0
        obj.db.alloc["movement"] = 0.0
        obj.db.alloc["shields"] = 0.0
        for i in range(constants.MAX_SHIELD_NAME):
            obj.db.alloc["shield"][i] = 0.0
        obj.db.alloc["cloak"] = 0.0
        obj.db.alloc["beams"] = 0.0
        obj.db.alloc["missiles"] = 0.0
        obj.db.alloc["sensors"] = 0.0
        obj.db.alloc["ecm"] = 0.0
        obj.db.alloc["eccm"] = 0.0
        obj.db.alloc["transporters"] = 0.0
        obj.db.alloc["tractors"] = 0.0
        obj.db.alloc["miscellaneous"] = 0.0
        obj.db.power["total"] = 0.0
        obj.db.beam["in"] = 0.0
        obj.db.beam["out"] = 0.0
        obj.db.missile["in"] = 0.0
        obj.db.missile["out"] = 0.0
    
    #beam
    if(obj.db.beam["exist"] != 1 or obj.db.beam["banks"] <= 0):
        obj.db.beam["banks"] = 0
        obj.db.beam["exist"] = 0
        obj.db.beam["freq"] = 0.0
        obj.db.beam["in"] = 0.0
        obj.db.beam["out"] = 0.0
        for i in range(constants.MAX_BEAM_BANKS):
            obj.db.blist[i]["name"] = 0
            obj.db.blist[i]["damage"] = 0.0
            obj.db.blist[i]["bonus"] = 0
            obj.db.blist[i]["cost"] = 0
            obj.db.blist[i]["range"] = 0
            obj.db.blist[i]["arcs"] = 0
            obj.db.blist[i]["active"] = 0
            obj.db.blist[i]["lock"] = 0
            obj.db.blist[i]["load"] = 0
            obj.db.blist[i]["recycle"] = 0
    else:
        if(obj.db.beam["in"] < 0.0):
            obj.db.beam["in"] = 0.0
            bug = 0
        if(obj.db.beam["out"] < 0.0):
            obj.db.beam["out"] = 0.0
            bug = 0
        if(obj.db.beam["banks"] > constants.MAX_BEAM_BANKS):
            obj.db.beam["banks"] = constants.MAX_BEAM_BANKS
            bug = 0
        if(obj.db.beam["freq"] <= 1.0 or obj.db.beam["freq"] > 1000.0):
            obj.db.beam["freq"] = random.random() * 10000 / 100.0
            bug = 0
        for i in range(constants.MAX_BEAM_BANKS):
            if((obj.db.blist[i]["arcs"] & 1) == 0 and (obj.db.blist[i]["arcs"] & 4) == 0):
                obj.db.blist[i] += 5
            if((obj.db.blist[i]["arcs"] & 2) == 0 and (obj.db.blist[i]["arcs"] & 8) == 0):
                obj.db.blist[i] += 10
            if((obj.db.blist[i]["arcs"] & 16) == 0 and (obj.db.blist[i]["arcs"] & 32) == 0):
                obj.db.blist[i] += 48
            if(obj.db.blist[i]["recycle"] < 1):
                obj.db.blist[i]["recycle"] = 1
            if(obj.db.beam["banks"] == 0):
                bug = 0

    #missile
    if(obj.db.missile["exist"] != 1 or obj.db.missile["tubes"] <= 0):
        obj.db.missile["tubes"] = 0
        obj.db.missile["exist"] = 0
        obj.db.missile["freq"] = 0.0
        obj.db.missile["in"] = 0.0
        obj.db.missile["out"] = 0.0
        for i in range(constants.MAX_BEAM_BANKS):
            obj.db.mlist[i]["name"] = 0
            obj.db.mlist[i]["damage"] = 0.0
            obj.db.mlist[i]["warhead"] = 0
            obj.db.mlist[i]["cost"] = 0
            obj.db.mlist[i]["range"] = 0
            obj.db.mlist[i]["arcs"] = 0
            obj.db.mlist[i]["active"] = 0
            obj.db.mlist[i]["lock"] = 0
            obj.db.mlist[i]["load"] = 0
            obj.db.mlist[i]["recycle"] = 0
    else:
        if(obj.db.missile["in"] < 0.0):
            obj.db.missile["in"] = 0.0
            bug = 0
        if(obj.db.missile["out"] < 0.0):
            obj.db.missile["out"] = 0.0
            bug = 0
        if(obj.db.missile["tubes"] > constants.MAX_MISSILE_TUBES):
            obj.db.missile["tubes"] = constants.MAX_MISSILE_TUBES
            bug = 0
        if(obj.db.missile["freq"] <= 1.0 or obj.db.missile["freq"] > 1000.0):
            obj.db.missile["freq"] = random.random() * 10000 / 100.0
            bug = 0
        for i in range(constants.MAX_MISSILE_TUBES):
            if((obj.db.mlist[i]["arcs"] & 1) == 0 and (obj.db.mlist[i]["arcs"] & 4) == 0):
                obj.db.mlist[i] += 5
            if((obj.db.mlist[i]["arcs"] & 2) == 0 and (obj.db.mlist[i]["arcs"] & 8) == 0):
                obj.db.mlist[i] += 10
            if((obj.db.mlist[i]["arcs"] & 16) == 0 and (obj.db.mlist[i]["arcs"] & 32) == 0):
                obj.db.mlist[i] += 48
            if(obj.db.mlist[i]["recycle"] < 1):
                obj.db.mlist[i]["recycle"] = 1
            if(obj.db.missile["tubes"] == 0):
                bug = 0
    #engine
    if(obj.db.engine["impulse_exist"] != 1):
        obj.db.engine["impulse_exist"] = 0
        obj.db.engine["impulse_damage"] = 0.0
        obj.db.engine["impulse_max"] = 0.0
        obj.db.engine["impulse_cruise"] = 0.0
    
    if(obj.db.engine["warp_exist"] != 1):
        obj.db.engine["warp_exist"] = 0
        obj.db.engine["warp_damage"] = 0.0
        obj.db.engine["warp_max"] = 0.0
        obj.db.engine["warp_cruise"] = 0.0

    if(obj.db.engine["warp_exist"] != 1 and obj.db.engine["impulse_exist"] != 1):
        obj.db.move["in"] = 0.0
        obj.db.move["out"] = 0.0
    
    #structure
    if(obj.db.structure["displacement"] < 0):
        obj.db.structure["displacement"] = 1
        bug = 0
    if(obj.db.structure["cargo_hold"] > obj.db.structure["displacement"]):
        obj.db.structure["cargo_hold"] = obj.db.structure["displacement"]
        bug = 0
    elif(obj.db.structure["cargo_hold"] < 0):
        obj.db.structure["cargo_hold"] = 0
        bug = 0
    if(obj.db.structure["max_structure"] <= 0):
        obj.db.structure["max_structure"] = 1
        bug = 0
    if(obj.db.structure["superstructure"] > obj.db.structure["max_structure"]):
        obj.db.structure["superstructure"] = obj.db.structure["max_structure"]
        bug = 0
    if(obj.db.structure["max_repair"] < 0):
        obj.db.structure["max_repair"] = 0
        bug = 0
    if(obj.db.structure["repair"] > obj.db.structure["max_repair"]):
        obj.db.structure["repair"] = obj.db.structure["max_repair"]
        bug = 0
    if (obj.db.structure["repair"] < 0.0):
        obj.db.structure["repair"] = 0.0
        bug = 0
    
    #sensor
    if(obj.db.sensor["lrs_exist"] != 1):
        obj.db.sensor["lrs_active"] = 0
        obj.db.sensor["lrs_exist"] = 0
        obj.db.sensor["lrs_damage"] = 0.0
        obj.db.sensor["lrs_resolution"] = 0.0

    if(obj.db.sensor["srs_exist"] != 1):
        obj.db.sensor["srs_active"] = 0
        obj.db.sensor["srs_exist"] = 0
        obj.db.sensor["srs_damage"] = 0.0
        obj.db.sensor["srs_resolution"] = 0.0

    if(obj.db.sensor["ew_exist"] != 1):
        obj.db.sensor["ew_active"] = 0
        obj.db.sensor["ew_exist"] = 0
        obj.db.sensor["ew_damage"] = 0.0
        
    if(obj.db.sensor["srs_exist"] == 0 and obj.db.sensor["lrs_exist"] == 0):
        obj.db.sensor["contacts"] = 0
        obj.db.sensor["counter"] = 0
        for i in range(constants.MAX_SENSOR_CONTACTS):
            obj.db.slist[i]["key"] = 0
            obj.db.slist[i]["num"] = 0
            obj.db.slist[i]["lev"] = 0
    
    #shield
    if(obj.db.shield["exist"] != 1 or obj.db.shield["ratio"] <= 0.0 or obj.db.shield["maximum"] <= 0):
        obj.db.shield["exist"] = 0
        obj.db.shield["ratio"] = 0
        obj.db.shield["maximum"] = 0
        obj.db.shield["freq"] = 0.0
        for i in range(constants.MAX_SHIELD_NAME):
            obj.db.shield[i]["damage"] = 0.0
            obj.db.shield[i]["active"] = 0
    
    #tech
    if(obj.db.tech["firing"] <= 0.0):
        obj.db.tech["firing"] = 1.0
        bug = 0
    if(obj.db.tech["fuel"] <= 0.0):
        obj.db.tech["fuel"] = 1.0
        bug = 0
    if(obj.db.tech["stealth"] <= 0.0):
        obj.db.tech["stealth"] = 1.0
        bug = 0
    if(obj.db.tech["cloak"] <= 0.0):
        obj.db.tech["cloak"] = 1.0
        bug = 0
    if(obj.db.tech["sensors"] <= 0.0):
        obj.db.tech["sensors"] = 1.0
        bug = 0
    if(obj.db.tech["main_max"] <= 0.0):
        obj.db.tech["main_max"] = 1.0
        bug = 0
    if (obj.db.tech["aux_max"] <= 0.0):
        obj.db.tech["aux_max"] = 1.0
        bug = 0
    if (obj.db.tech["armor"] <= 0.0):
        obj.db.tech["armor"] = 1.0
        bug = 0
    
    #move
    if(obj.db.move["ratio"] <= 0.0):
        obj.db.move["ratio"] = 1.0
        bug = 0
    
    #cloak
    if(obj.db.cloak["exist"] != 0 or obj.db.cloak["cost"] <= 0):
        obj.db.cloak["exist"] = 0
        obj.db.cloak["cost"] = 0
        obj.db.cloak["damage"] = 0
        obj.db.cloak["freq"] = 0.0
        obj.db.cloak["active"] = 0
    else:
        if(obj.db.cloak["freq"] <= 1.0 or obj.db.cloak["freq"] >= 1000.0):
            obj.db.cloak["freq"] = random.random() * 10000 / 100.0
            bug = 0
    
    #trans
    if(obj.db.trans["exist"] != 1):
        obj.db.trans["cost"] = 0
        obj.db.trans["damage"] = 0.0
        obj.db.trans["freq"] = 0.0
        obj.db.trans["exist"] = 0
        obj.db.trans["d_lock"] = 0
        obj.db.trans["s_lock"] = 0
    else:
        if(obj.db.trans["freq"] <= 1.0 or obj.db.trans["freq"] >= 1000.0):
            obj.db.trans["freq"] = random.random() * 10000 / 100.0
            bug = 0
    
    #if(obj.db.trans["d_lock"] != 0):
    #    if(obj.db.trans["d_lock"] != obj.name):
    #        if(sdb2contact(self,obj.db.trans["d_lock"]) == constants.SENSOR_FAIL):
    #            obj.db.trans["d_lock"] = 0
    #
    #if(obj.db.trans["s_lock"] != 0):
    #    if(obj.db.trans["s_lock"] != obj.name):
    #        if(sdb2contact(self,obj.db.trans["s_lock"]) == constants.SENSOR_FAIL):
    #            obj.db.trans["s_lock"] = 0
            
    #tract
    if(obj.db.tract["exist"]!= 1):
        obj.db.tract["cost"] = 0
        obj.db.tract["damage"] = 0
        obj.db.tract["freq"] = 0.0
        obj.db.tract["active"] = 0
        obj.db.tract["exist"] = 0
        obj.db.tract["lock"] = 0
        obj.db.status["tractoring"] = 0
    else:
        if(obj.db.tract["freq"] <= 1.0 or obj.db.tract["freq"] >= 1000.0):
            obj.db.tract["freq"] = random.random() * 10000 / 100.0
            bug = 0
    
    #fuel
    if(obj.db.fuel["antimatter"] < 0.0):
        obj.db.fuel["antimatter"] = 0.0
    if(obj.db.fuel["deuterium"] < 0.0):
        obj.db.fuel["deuterium"] = 0.0
    if(obj.db.fuel["reserves"] < 0.0):
        obj.db.fuel["reserves"] = 0.0
    if(obj.db.fuel["antimatter"] > sdb2max_antimatter(obj)):
        obj.db.fuel["antimatter"] = sdb2max_antimatter(obj)
    if(obj.db.fuel["deuterium"] > sdb2max_deuterium(obj)):
        obj.db.fuel["deuterium"] = sdb2max_deuterium(obj)
    if(obj.db.fuel["reserves"] > sdb2max_reserves(obj)):
        obj.db.fuel["reserves"] = sdb2max_reserves(obj)
    
    #status
    if(obj.db.structure["superstructure"] <= - obj.db.structure["max_structure"]):
        obj.db.status["crippled"] = 2
    elif(obj.db.structure["superstructure"] <= 0.0):
        obj.db.status["crippled"] = 1
    else:
        obj.db.status["crippled"] = 0
    
    iterate.up_cochranes(obj)
    iterate.up_turn_rate(obj)
    iterate.up_vectors(obj)
    iterate.up_empire(obj)
    iterate.up_quadrant(obj)
    iterate.up_resolution(obj)
    iterate.up_signature(obj)
    iterate.up_visibility(obj)
    return bug