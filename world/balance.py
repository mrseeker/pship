"""
The world must be in balance, else we are having issues.
"""

from world import constants

def balance_eng_power(obj):
    total = obj.db.alloc["helm"] + obj.db.alloc["tactical"] + obj.db.alloc["operations"]
    if (total > 0.0):
        obj.db.alloc["helm"] /= total
        obj.db.alloc["tactical"] /= total
        obj.db.alloc["operations"] /= total
    else:
        obj.db.alloc["helm"] = 0.0
        obj.db.alloc["tactical"] = 0.0
        obj.db.alloc["operations"] = 1.0

def balance_helm_power(obj):
    if (obj.db.alloc["helm"] > 0.0):
        total = obj.db.alloc["movement"] + obj.db.alloc["shields"] + obj.db.alloc["cloak"]
        if (total > 0.0):
            total /= obj.db.alloc["helm"]
            obj.db.alloc["movement"] /= total
            obj.db.alloc["shields"] /= total
            obj.db.alloc["cloak"] /= total
        else:
            obj.db.alloc["shields"] = obj.db.alloc["helm"]
            obj.db.alloc["movement"] = 0.0
            obj.db.alloc["cloak"] = 0.0
    else:
        obj.db.alloc["movement"] = 0.0
        obj.db.alloc["shields"] = 0.0
        obj.db.alloc["cloak"] = 0.0

def balance_shield_power(obj):
    total = 0.0
    if(obj.db.alloc["shields"] > 0.0):
        for i in range(constants.MAX_SHIELD_NAME):
            total += obj.db.alloc["shield"][i]
        if (total > 0.0):
            total /= obj.db.alloc["shields"]
            for i in range(constants.MAX_SHIELD_NAME):
                obj.db.alloc["shield"][i] /= total
        else:
            for i in range(constants.MAX_SHIELD_NAME):
                obj.db.alloc["shield"][i] = obj.db.alloc["shields"] / constants.MAX_SHIELD_NAME
    else:
        for i in range(constants.MAX_SHIELD_NAME):
            obj.db.alloc["shield"][i] = 0

def balance_tact_power(obj):
    if (obj.db.alloc["tactical"] > 0.0):
        total = obj.db.alloc["beams"] + obj.db.alloc["missiles"] + obj.db.alloc["sensors"]
        if (total > 0.0):
            total /= obj.db.alloc["tactical"]
            obj.db.alloc["beams"] /= total
            obj.db.alloc["missiles"] /= total
            obj.db.alloc["sensors"] /= total
        else:
            obj.db.alloc["beams"] = 0
            obj.db.alloc["missiles"] = 0
            obj.db.alloc["sensors"] = obj.db.alloc["tactical"]
    else:
        obj.db.alloc["beams"] = 0.0
        obj.db.alloc["missiles"] = 0.0
        obj.db.alloc["sensors"] = 0.0

def balance_sensor_power(obj):
    if (obj.db.alloc["sensors"] > 0.0):
        total = obj.db.alloc["ecm"] + obj.db.alloc["eccm"]
        if (total > 0.0):
            total /= obj.db.alloc["sensors"]
            obj.db.alloc["ecm"] /= total
            obj.db.alloc["eccm"] /= total
        else:
            obj.db.alloc["ecm"] = obj.db.alloc["sensors"] / 2.0
            obj.db.alloc["eccm"] = obj.db.alloc["sensors"] / 2.0 
    else:
        obj.db.alloc["ecm"] = 0.0
        obj.db.alloc["eccm"] = 0.0

def balance_ops_power(obj):
    if (obj.db.alloc["operations"] > 0.0):
        total = obj.db.alloc["transporters"] + obj.db.alloc["tractors"] + obj.db.alloc["miscellaneous"]
        if (total > 0.0):
            total /= obj.db.alloc["operations"]
            obj.db.alloc["transporters"] /= total
            obj.db.alloc["tractors"] /= total
            obj.db.alloc["miscellaneous"] /= total
        else:
            obj.db.alloc["transporters"] = 0.0
            obj.db.alloc["tractors"] = 0.0
            obj.db.alloc["miscellaneous"] = obj.db.alloc["operations"]
    else:
        obj.db.alloc["transporters"] = 0.0
        obj.db.alloc["tractors"] = 0.0
        obj.db.alloc["miscellaneous"] = 0.0
