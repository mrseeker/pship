from world import alerts,constants,unparse,format,iterate
from evennia.utils.search import search_object,search_tag

def damage_structure(obj, damage):
    s = obj.db.structure["superstructure"]
    if (obj.db.structure["superstructure"] == -obj.db.structure["max_structure"]):
        return
    obj.db.structure["superstructure"] -= damage
    if (obj.db.structure["superstructure"] < -obj.db.structure["max_structure"]):
        obj.db.structure["superstructure"] = -obj.db.structure["max_structure"]
    alerts.console_message(obj,["damage","engineering"],alerts.ansi_alert("|c" + constants.system_name[0] + "|w: "+unparse.unparse_percent(obj.db.structure["superstructure"]/obj.db.structure["max_structure"])+ " " + unparse.unparse_damage(obj.db.structure["superstructure"]/obj.db.structure["max_structure"])))
    if (obj.db.structure["superstructure"] <= -obj.db.structure["max_structure"]) and (s > -obj.db.structure["max_structure"]):
        alerts.do_ship_notify(obj,"|*|r" + format.name(obj) + " explodes into white hot vapor|n")
        alerts.do_space_notify_one(obj,["helm","tactical","science"], "has been destroyed")
        obj.db.space = -1
        obj.db.status["active"] = 0
        obj.db.status["crippled"] = 2
        objects = search_tag(category="space_object")
        for obj_x in objects:
            if (obj_x.db.location == obj.db.name):
                if (obj_x.db.structure["type"] > 0):
                    alerts.do_ship_notify(obj_x,"|*|r" + format.name(obj) + " explodes into white hot vapor. Goodbye!|n")
                    obj_x.space = -1                    
                    obj_x.db.status["active"] = 0
                    obj_x.db.status["crippled"] = 2
    elif (obj.db.structure["superstructure"] <= 0.0) and (s > 0.0):
        alerts.do_all_console_notify(obj,alerts.ansi_warn("Excessive damage. All systems shutting down"))
        alerts.do_ship_notify(obj,format.name(obj) + " experiences total systems failure.")
        obj.db.status["crippled"] = 1
        alerts.do_space_notify_one(obj,["helm","tactical","science"],"has been disabled")
    if ((obj.db.structure["superstructure"] <= 0.0) and (s > 0.0)) or (obj.db.structure["superstructure"] <= -obj.db.structure["max_structure"]) and (s > -obj.db.structure["max_structure"]):
        if (obj.db.main["damage"] > 0.0):
            obj.db.main["in"] = 0.0
        if (obj.db.aux["damage"] > 0.0):
            obj.db.aux["in"] = 0.0
        for i in range(constants.MAX_SHIELD_NAME):
            obj.db.shield[i]["active"] = 0
        obj.db.beam["in"] = 0.0
        obj.db.beam["out"] = 0.0
        for i in range(obj.db.beam["banks"]):
            obj.db.blist[i]["lock"] = 0
            obj.db.blist[i]["active"] = 0
        obj.db.missile["in"] = 0.0
        obj.db.missile["out"] = 0.0
        for i in range(obj.db.missile["tubes"]):
            obj.db.mlist[i]["lock"] = 0
            obj.db.mlist[i]["active"] = 0
        obj.db.batt["in"] = 0.0
        obj.db.batt["out"] = 0.0
        obj.db.move["in"] = 0.0
        obj.db.move["out"] = 0.0
        obj.db.move["v"] = 0.0
        obj.db.engine["warp_max"] = 0.0
        obj.db.engine["impulse_max"] = 0.0
        obj.db.power["batt"] = 0.0
        obj.db.sensor["lrs_active"] = 0
        obj.db.sensor["srs_active"] = 0
        obj.db.sensor["ew_active"] = 0
        obj.db.cloak["active"] = 0
        obj.db.trans["active"] = 0
        obj.db.trans["d_lock"] = 0
        obj.db.trans["s_lock"] = 0
        obj.db.tract["active"] = 0
        obj.db.tract["lock"] = 0
        if (obj.db.status["tractoring"]):
            obj_x = search_object(obj.db.status["tractoring"])[0]
            obj_x.db.status["tractored"] = 0
            obj.db.status["tractoring"] = 0
        iterate.up_cochranes()
        iterate.up_empire(obj)
        iterate.up_quadrant()
        iterate.up_vectors()
        iterate.up_resolution()
        iterate.up_signature(obj)
        iterate.up_visibility()
    return