from world import unparse, utils

def l_line():
    return '|b-------------------------------------------------------------------------------|w\n'

def l_end():
    return '|b|h-------------------------------------------------------------------------------|w|n\n'

def name(obj):
    return f'|c{"Name":16}:|w {obj.name:<20}'

def type(obj):
    return f'|c{"Type":16}:|w {unparse.unparse_type(obj):<20}'

def resolution(value):
    return f'|c{"Resolution":16}:|w {unparse.unparse_percent_3(value):<20}'

def cargo_cap(obj):
    return f'|c{"Cargo Capacity":16}:|w {unparse.unparse_cargo(obj.db.structure["cargo_hold"]):<20}'
    
def docking_doors(obj):
    if (obj.db.status["open_docking"] == 1):
        return f'|c{"Docking Doors":16}:|w {"Open":<20}'
    else:
        return f'|c{"Docking Doors":16}:|w {"Closed":<20}'

def landing_doors(obj):
    if (obj.db.status["open_landing"] == 1):
        return f'|c{"Landing Doors":16}:|w {"Open":<20}'
    else:
        return f'|c{"Landing Doors":16}:|w {"Closed":<20}'

def ship_class(obj):
    return f'|c{"Class":16}:|w {unparse.unparse_class(obj):<20}'

def displacement(obj):
    return f'|c{"Displacement":16}:|w {unparse.unparse_cargo(obj.db.structure["displacement"]):<20}'

def contact_arc(obj1,obj2):
    return f'|c{"Contact Arc":16}:|w {unparse.unparse_arc(utils.sdb2arc(obj1,obj2)):<20}'

def contact_shield(obj1,obj2):
    if (obj2.db.shield["exist"] == 0):
        return f'|c{"Contact Shield":16}:|w {"None":<20}'
    else:
        shield = utils.sdb2shield(obj1,obj2)
        if(utils.sdb2dissipation(obj2,shield) > 0):
            return f'|c{"Contact Shield":16}:|w {unparse.unparse_shield(shield):<17} UP'
        else:
            return f'|c{"Contact Shield":16}:|w {unparse.unparse_shield(shield):<20}'

def course(obj):
    return f'|c{"Course":16}:|w {unparse.unparse_course(obj):<20}'

def speed(obj):
    return f'|c{"Speed":16}:|w {unparse.unparse_movement(obj):<20}'

def bearing(obj1,obj2):
    return f'|c{"Bearing":16}:|w {unparse.unparse_bearing(obj1,obj2):<20}'

def ship_range(obj1, obj2):
    return f'|c{"Range":16}:|w {unparse.unparse_distance(utils.sdb2range(obj1,obj2)):<20}'

def firing_arc(obj1, obj2):
    return f'|c{"Firing Arc":16}:|w {unparse.unparse_arc(utils.sdb2arc(obj1,obj2)):<20}'

def facing_shield(obj1,obj2):
    if (obj1.db.shield["exist"] == 0):
        return f'|c{"Facing Shield":16}:|w {"None":<20}'
    else:
        shield = utils.sdb2shield(obj1,obj2)
        if(utils.sdb2dissipation(obj1,shield) > 0):
            return f'|c{"Facing Shield":16}:|w {unparse.unparse_shield(shield):<17} UP'
        else:
            return f'|c{"Facing Shield":16}:|w {unparse.unparse_shield(shield):<20}'

def location(obj):
    l = obj.db.location
    if (l == 0):
        if(obj.db.sensor["visibility"] < 0.1):
            return f'|c{"Location":16}:|w {"Opaque Nebula":<20}'
        elif(obj.db.sensor["visibility"] < 0.25):
            return f'|c{"Location":16}:|w {"Thick Nebula":<20}'
        elif(obj.db.sensor["visibility"] < 0.50):
            return f'|c{"Location":16}:|w {"Moderate Nebula":<20}'
        elif(obj.db.sensor["visibility"] < 0.90):
            return f'|c{"Location":16}:|w {"Light Nebula":<20}'
        else:
            return f'|c{"Location":16}:|w {"Open Space":<20}'
    elif(obj.db.status["docked"]):
        if(obj.db.status["connected"]):
            return f'|c{"Location":16}:|w D+C:{l:<17}'
        else:
            return f'|c{"Location":16}:|w D:{l:<18}'
    elif(obj.db.status["landed"]):
        if(obj.db.status["connected"]):
            return f'|c{"Location":16}:|w L+C:{l:<17}'
        else:
            return f'|c{"Location":16}:|w L:{l:<18}'
    else:
        return f'|c{"Location":16}:|w {"#-1 BAD UNKNOWN":<20}'
        
def velocity(obj):
    return f'|c{"Velocity":16}:|w {unparse.unparse_velocity(obj):<20}'
