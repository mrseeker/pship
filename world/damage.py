from world import alerts,constants,unparse,format,iterate, utils
from evennia.utils.search import search_object,search_tag
import random

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

def damage_aux(obj,damage):
    if(obj.db.aux["exist"] == 0 or obj.db.aux["damage"] == -1.0):
        return 0
    if(obj.db.power["aux"] != 0.0 and obj.db.aux["damage"] > 0.0 and (obj.db.aux["damage"] - damage / obj.db.aux["gw"] <= 0.0)):
        alerts.aux_overload(obj)
    obj.db.aux["damage"] -= damage / obj.db.aux["gw"]
    if(obj.db.aux["damage"] < -1.0):
        obj.db.aux["damage"] = -1.0
        if(obj.db.power["aux"] != 0.0):
            alerts.do_all_console_notify(obj,alerts.ansi_warn("{:s} core breach.".format(constants.system_name[1])))
            damage_structure(obj,obj.db.power["aux"] * (random.random() * 10.0 + 1.0))
    alerts.console_message(obj,["damage","engineering"],alerts.ansi_alert("|c{:s}|w: {:s} {:s}".format(constants.system_name[1],unparse.unparse_percent(obj.db.aux["damage"]),unparse.unparse_damage(obj.db.aux["damage"]))))
    return 1

def damage_batt(obj,damage):
    if(obj.db.batt["exist"] == 0 or obj.db.batt["damage"] == -1.0):
        return 0
    obj.db.batt["damage"] -= damage / obj.db.batt["gw"]
    if(obj.db.batt["damage"] < -1.0):
        obj.db.batt["damage"] = -1.0
    alerts.console_message(obj,["damage","engineering"],alerts.ansi_alert("|c{:s}|w: {:s} {:s}".format(constants.system_name[2],unparse.unparse_percent(obj.db.batt["damage"]),unparse.unparse_damage(obj.db.batt["damage"]))))
    if(obj.db.batt["damage"] <= 0.0):
        obj.db.batt["in"] = 0.0
        obj.db.batt["out"] = 0.0
        obj.db.power["batt"] = 0.0
        obj.db.power["version"] = 1
    return 1

def damage_beam(obj,beam,damage):
    if(obj.db.beam["exist"] == 0 or obj.db.blist[beam]["damage"] == -1.0):
        return 0
    obj.db.blist[beam]["damage"] -= damage / (obj.db.blist[beam]["cost"] + obj.db.blist[beam]["bonus"]) / 10.0
    if (obj.db.blist[beam]["damage"] < -1.0):
        obj.db.blist[beam]["damage"] = -1.0
    alerts.console_message(obj,["damage","tactical"],alerts.ansi_alert("|c{:s} {:d}|w: {:s} {:s}".format(constants.system_name[3],beam+1,unparse.unparse_percent(obj.db.blist[beam]["damage"]),unparse.unparse_damage(obj.db.blist[beam]["damage"]))))
    if(obj.db.blist[beam]["damage"] <= 0.0):
        if (obj.db.blist[beam]["active"] == 1):
            obj.db.beam["in"] -= 10.0 * obj.db.blist[beam]["cost"]
            obj.db.blist[beam]["active"] = 0
            obj.db.blist[beam]["lock"] = 0
    return 1

def damage_cloak(obj,damage):
    if(obj.db.cloak["exist"] == 0 or obj.db.cloak["damage"] == -1.0):
        return 0
    obj.db.cloak["damage"] -= damage / (1.0 + (obj.db.structure["max_structure"] / 100.0))
    if (obj.db.cloak["damage"] < -1.0):
        obj.db.cloak["damage"] = -1.0
    alerts.console_message(obj,["damage","helm"],alerts.ansi_alert("|c{:s}|w: {:s} {:s}".format(constants.system_name[4],unparse.unparse_percent(obj.db.cloak["damage"]),unparse.unparse_damage(obj.db.cloak["damage"]))))
    if(obj.db.cloak["damage"] <= 0.0):
        if (obj.db.cloak["active"] == 1):
            obj.db.cloak["active"] = 0
            obj.db.engine["version"] = 1
            alerts.ship_cloak_offline(obj)
    obj.db.sensor["version"] = 1
    return 1

def damage_ew(obj,damage):
    if(obj.db.sensor["ew_exist"] == 0 or obj.db.sensor["ew_damage"] == -1.0):
        return 0
    obj.db.sensor["ew_damage"] -= damage / (1.0 + (obj.db.structure["max_structure"] / 10.0))
    if (obj.db.sensor["ew_damage"] < -1.0):
        obj.db.sensor["ew_damage"] = -1.0
    alerts.console_message(obj,["damage","science","tactical"],alerts.ansi_alert("|c{:s}|w: {:s} {:s}".format(constants.system_name[5],unparse.unparse_percent(obj.db.sensor["ew_damage"]),unparse.unparse_damage(obj.db.sensor["ew_damage"]))))
    if(obj.db.sensor["ew_damage"] <= 0.0):
        if (obj.db.sensor["ew_active"] == 1):
            obj.db.sensor["ew_active"] = 0
    obj.db.sensor["version"] = 1
    return 1

def damage_impulse(obj,damage):
    if(obj.db.engine["impulse_exist"] == 0 or obj.db.engine["impulse_damage"] == -1.0):
        return 0
    obj.db.engine["impulse_damage"] -= damage / (1.0 + (obj.db.structure["max_structure"] / 10.0))
    if (obj.db.engine["impulse_damage"] < -1.0):
        obj.db.engine["impulse_damage"] = -1.0
    alerts.console_message(obj,["damage","engineering"],alerts.ansi_alert("|c{:s}|w: {:s} {:s}".format(constants.system_name[6],unparse.unparse_percent(obj.db.engine["impulse_damage"]),unparse.unparse_damage(obj.db.engine["impulse_damage"]))))
    obj.db.engine["version"] = 1
    return 1

def damage_lrs(obj,damage):
    if(obj.db.sensor["lrs_exist"] == 0 or obj.db.sensor["lrs_damage"] == -1.0):
        return 0
    obj.db.sensor["lrs_damage"] -= damage / (1.0 + (obj.db.structure["max_structure"] / 10.0))
    if (obj.db.sensor["lrs_damage"] < -1.0):
        obj.db.sensor["lrs_damage"] = -1.0
    alerts.console_message(obj,["damage","science","tactical"],alerts.ansi_alert("|c{:s}|w: {:s} {:s}".format(constants.system_name[7],unparse.unparse_percent(obj.db.sensor["lrs_damage"]),unparse.unparse_damage(obj.db.sensor["lrs_damage"]))))
    if(obj.db.sensor["lrs_damage"] <= 0.0):
        if (obj.db.sensor["lrs_active"] == 1):
            obj.db.sensor["lrs_active"] = 0
    obj.db.sensor["version"] = 1
    return 1

def damage_main(obj,damage):
    if(obj.db.main["exist"] == 0 or obj.db.main["damage"] == -1.0):
        return 0
    if(obj.db.power["main"] != 0.0 and obj.db.main["damage"] > 0.0 and (obj.db.main["damage"] - damage / obj.db.main["gw"] <= 0.0)):
        alerts.main_overload(obj)
    obj.db.main["damage"] -= damage / obj.db.main["gw"]
    if(obj.db.main["damage"] < -1.0):
        obj.db.main["damage"] = -1.0
        if(obj.db.power["main"] != 0.0):
            alerts.do_all_console_notify(obj,alerts.ansi_warn("{:s} core breach.".format(constants.system_name[8])))
            damage_structure(obj,obj.db.power["aux"] * (random.random() * 100.0 + 1.0))
    alerts.console_message(obj,["damage","engineering"],alerts.ansi_alert("|c{:s}|w: {:s} {:s}".format(constants.system_name[8],unparse.unparse_percent(obj.db.main["damage"]),unparse.unparse_damage(obj.db.main["damage"]))))
    return 1

def damage_missile(obj,missile,damage):
    if(obj.db.missile["exist"] == 0 or obj.db.mlist[missile]["damage"] == -1.0):
        return 0
    obj.db.mlist[missile]["damage"] -= damage / (obj.db.mlist[missile]["cost"] + obj.db.mlist[missile]["warhead"]) / 10.0
    if (obj.db.mlist[missile]["damage"] < -1.0):
        obj.db.mlist[missile]["damage"] = -1.0
    alerts.console_message(obj,["damage","tactical"],alerts.ansi_alert("|c{:s} {:d}|w: {:s} {:s}".format(constants.system_name[9],missile+1,unparse.unparse_percent(obj.db.mlist[missile]["damage"]),unparse.unparse_damage(obj.db.mlist[missile]["damage"]))))
    if(obj.db.mlist[missile]["damage"] <= 0.0):
        if (obj.db.mlist[missile]["active"] == 1):
            obj.db.missile["in"] -= 10.0 * obj.db.mlist[missile]["cost"]
            obj.db.mlist[missile]["active"] = 0
            obj.db.mlist[missile]["lock"] = 0
    return 1

def damage_shield(obj,shield,damage):
    if(obj.db.shield["exist"] == 0 or obj.db.shield[shield]["damage"] == -1.0):
        return 0
    obj.db.shield[shield]["damage"] -= damage / (1.0 + (obj.db.structure["max_structure"] / 10.0))
    if (obj.db.shield[shield]["damage"] < -1.0):
        obj.db.shield[shield]["damage"] = -1.0
    alerts.console_message(obj,["damage","helm"],alerts.ansi_alert("|c{:s}|w: {:s} {:s}".format(unparse.unparse_shield(shield),unparse.unparse_percent(obj.db.shield[shield]["damage"]),unparse.unparse_damage(obj.db.shield[shield]["damage"]))))
    if(obj.db.shield[shield]["damage"] <= 0.0):
        if (obj.db.shield[shield]["active"] == 1):
            obj.db.shield[shield]["active"] = 0
            obj.db.engine["version"] = 1
    return 1

def damage_srs(obj,damage):
    if(obj.db.sensor["srs_exist"] == 0 or obj.db.sensor["srs_damage"] == -1.0):
        return 0
    obj.db.sensor["srs_damage"] -= damage / (1.0 + (obj.db.structure["max_structure"] / 10.0))
    if (obj.db.sensor["srs_damage"] < -1.0):
        obj.db.sensor["srs_damage"] = -1.0
    alerts.console_message(obj,["damage","science","tactical"],alerts.ansi_alert("|c{:s}|w: {:s} {:s}".format(constants.system_name[11],unparse.unparse_percent(obj.db.sensor["srs_damage"]),unparse.unparse_damage(obj.db.sensor["srs_damage"]))))
    if(obj.db.sensor["srs_damage"] <= 0.0):
        if (obj.db.sensor["srs_active"] == 1):
            obj.db.sensor["srs_active"] = 0
    obj.db.sensor["version"] = 1
    return 1

def damage_tract(obj,damage):
    if(obj.db.tract["exist"] == 0 or obj.db.tract["damage"] == -1.0):
        return 0
    obj.db.tract["damage"] -= damage / (1.0 + (obj.db.structure["max_structure"] / 10.0))
    if (obj.db.tract["damage"] < -1.0):
        obj.db.tract["damage"] = -1.0
    alerts.console_message(obj,["damage","operation"],alerts.ansi_alert("|c{:s}|w: {:s} {:s}".format(constants.system_name[12],unparse.unparse_percent(obj.db.tract["damage"]),unparse.unparse_damage(obj.db.tract["damage"]))))
    if(obj.db.tract["damage"] <= 0.0):
        if (obj.db.tract["active"] == 1):
            if(obj.db.status["tractoring"] != 0):
                alerts.tract_lost(obj,obj.db.status["tractoring"])
                obj.db.tract["lock"] = 0
                obj_tract = search_object(obj.db.status["tractoring"])
                obj_tract.db.status["tractored"] = 0
                obj_tract.db.power["version"] = 1
                obj.db.status["tractoring"] = 0
            obj.db.tract["active"] = 0
    obj.db.power["version"] = 1
    return 1

def damage_trans(obj,damage):
    if(obj.db.trans["exist"] == 0 or obj.db.trans["damage"] == -1.0):
        return 0
    obj.db.trans["damage"] -= damage / (1.0 + (obj.db.structure["max_structure"] / 10.0))
    if (obj.db.trans["damage"] < -1.0):
        obj.db.trans["damage"] = -1.0
    alerts.console_message(obj,["damage","operation","transporter"],alerts.ansi_alert("|c{:s}|w: {:s} {:s}".format(constants.system_name[13],unparse.unparse_percent(obj.db.trans["damage"]),unparse.unparse_damage(obj.db.trans["damage"]))))
    if(obj.db.trans["damage"] <= 0.0):
        if (obj.db.trans["active"] == 1):
            obj.db.trans["d_lock"] = 0
            obj.db.trans["s_lock"] = 0
            obj.db.trans["active"] = 0
    return 1

def damage_warp(obj,damage):
    if(obj.db.engine["warp_exist"] == 0 or obj.db.engine["warp_damage"] == -1.0):
        return 0
    obj.db.engine["warp_damage"] -= damage / (1.0 + (obj.db.structure["max_structure"] / 10.0))
    if (obj.db.engine["warp_damage"] < -1.0):
        obj.db.engine["warp_damage"] = -1.0
    alerts.console_message(obj,["damage","engineering"],alerts.ansi_alert("|c{:s}|w: {:s} {:s}".format(constants.system_name[14],unparse.unparse_percent(obj.db.engine["warp_damage"]),unparse.unparse_damage(obj.db.engine["warp_damage"]))))
    obj.db.engine["version"] = 1
    return 1

def repair_everything(obj):
    if(obj.db.aux["exist"] == 1):
        obj.db.aux["damage"] = 1.0
    if(obj.db.batt["exist"] == 1):
        obj.db.batt["damage"] = 1.0
    if(obj.db.beam["exist"] == 1):
        for i in range(obj.db.beam["banks"]):
            obj.db.blist[i]["damage"] = 1.0
    if(obj.db.missile["exist"] == 1):
        for i in range(obj.db.missile["tubes"]):
            obj.db.mlist[i]["damage"] = 1.0
    if(obj.db.cloak["exist"] == 1):
        obj.db.cloak["damage"] == 1.0
    if(obj.db.engine["warp_exist"] == 1):
        obj.db.engine["warp_damage"] == 1.0
    if(obj.db.engine["impulse_exist"] == 1):
        obj.db.engine["impulse_damage"] == 1.0
    if(obj.db.main["exist"] == 1):
        obj.db.main["damage"] = 1.0
    if(obj.db.sensor["ew_exist"] == 1):
        obj.db.sensor["ew_damage"] = 1.0
    if(obj.db.sensor["lrs_exist"] == 1):
        obj.db.sensor["lrs_damage"] = 1.0
    if(obj.db.sensor["srs_exist"] == 1):
        obj.db.sensor["srs_damage"] = 1.0
    if(obj.db.shield["exist"] == 1):
        for i in range(constants.MAX_SHIELD_NAME):
            obj.db.shield[i]["damage"] = 1.0
    
    obj.db.status["crippled"] = 0
    obj.db.structure["superstructure"] = obj.db.structure["max_structure"]
    obj.db.structure["repair"] = obj.db.structure["max_repair"]

    if(obj.db.trans["exist"] == 1):
        obj.db.trans["damage"] = 1.0
    
    if(obj.db.tract["exist"] == 1):
        obj.db.tract["damage"] = 1.0
    
    obj.db.sensor["version"] = 1
    obj.db.engine["version"] = 1
    obj.db.power["version"] = 1
    obj.db.cloak["version"] = 1

    iterate.up_cochranes(obj)
    iterate.up_empire(obj)
    iterate.up_quadrant(obj)
    iterate.up_vectors(obj)
    iterate.up_resolution(obj)
    iterate.up_signature(obj)
    iterate.up_visibility(obj)
    return utils.debug_space(obj)