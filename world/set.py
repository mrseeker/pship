"""
Sets the variables
"""
from world import alerts,constants,iterate, errors
from evennia.utils.search import search_object
from evennia import gametime


def do_set_inactive(self,obj):
    if (obj.db.structure["type"] == 0):
        alerts.notify(self, alerts.ansi_red("Space object not loaded."))
    elif (obj.db.status["crippled"] == 2):
        alerts.notify(self, alerts.ansi_red("Space object destroyed."))
    elif(not obj.db.status["active"]):
        alerts.notify(self, alerts.ansi_red(obj.name + " systems are already inactive."))
    elif(obj.db.power["total"] != 0):
        alerts.notify(self, alerts.ansi_red(obj.name + " power systems are still online."))
    else:
        alerts.do_all_console_notify(obj, alerts.ansi_cmd(self.name,"All systems shutting down"))
        alerts.do_ship_notify(obj, self.name + " deactivates all systems")
        alerts.do_space_notify_one(obj, ["helm","tactical","science"],obj.name + " deactivates all systems")
        for i in range(constants.MAX_SHIELD_NAME):
            obj.db.shield[i]["active"] = 0
        obj.db.beam["in"] = 0.0
        obj.db.beam["out"] = 0.0
        for i in range(obj.db.beam["banks"]):
            obj.ndb.blist["lock"][i] = 0
            obj.ndb.blist["active"][i] = 0
        obj.db.missile["in"] = 0.0
        obj.db.missile["out"] = 0.0
        for i in range(obj.db.missile["tubes"]):
            obj.ndb.mlist["lock"][i] = 0
            obj.ndb.mlist["active"][i] = 0
        obj.db.main["in"] = 0.0
        obj.db.main["out"] = 0.0
        obj.db.batt["in"] = 0.0
        obj.db.batt["out"] = 0.0
        obj.db.aux["in"] = 0.0
        obj.db.aux["out"] = 0.0
        obj.db.move["in"] = 0.0
        obj.db.move["out"] = 0.0
        obj.db.move["v"] = 0.0
        obj.db.engine["warp_max"] = 0.0
        obj.db.engine["impulse_max"] = 0.0
        obj.db.power["main"] = 0.0
        obj.db.power["aux"] = 0.0
        obj.db.power["batt"] = 0.0
        obj.db.power["total"] = 0.0
        obj.db.sensor["lrs_active"] = 0
        obj.db.sensor["srs_active"] = 0
        obj.db.sensor["ew_active"] = 0
        obj.db.sensor["contacts"] = 0
        obj.db.sensor["counter"] = 0
        obj.db.cloak["active"] = 0
        obj.db.trans["active"] = 0
        obj.db.trans["d_lock"] = 0
        obj.db.trans["s_lock"] = 0
        obj.db.tract["active"] = 0
        obj.db.tract["lock"] = 0
        if (obj.db.status["tractoring"]):
            x = self.db.status["tractoring"]
            obj_x = search_object(x)[0]
            obj_x.db.status["tractored"] = 0
            obj.db.status["tractoring"] = 0
        obj.db.status["active"] = 0
        obj.db.status["time"] = obj.db.move["time"]
        obj.db.status["autopilot"] = 0
        iterate.up_cochranes(self)
        iterate.up_empire(self)
        iterate.up_vectors(self)
        iterate.up_resolution(self)
        iterate.up_signature(self)
        iterate.up_visibility(self)
        return 1
    return 0
    
def do_set_active(self,obj):
    if (obj.db.structure["type"] == 0):
        alerts.notify(self, alerts.ansi_red("Space object not loaded."))
    elif (obj.db.status["crippled"] == 2):
        alerts.notify(self, alerts.ansi_red("Space object destroyed."))
    elif(obj.db.status["active"]):
        alerts.notify(self, alerts.ansi_red(obj.name + " systems are already active."))
    else:
        alerts.do_all_console_notify(obj, alerts.ansi_cmd(self.name,"All systems initializing and starting up"))
        alerts.do_ship_notify(obj, self.name + " activates all systems")
        alerts.do_space_notify_one(obj, ["helm","tactical","science"],obj.name + " activates all systems")
        for i in range(constants.MAX_SHIELD_NAME):
            obj.db.shield[i]["active"] = 0
        obj.db.beam["in"] = 0.0
        obj.db.beam["out"] = 0.0
        for i in range(obj.db.beam["banks"]):
            obj.db.blist["lock"][i] = 0
            obj.db.blist["active"][i] = 0
        obj.db.missile["in"] = 0.0
        obj.db.missile["out"] = 0.0
        for i in range(obj.db.missile["tubes"]):
            obj.ndb.mlist["lock"][i] = 0
            obj.ndb.mlist["active"][i] = 0
        obj.db.main["in"] = 0.0
        obj.db.main["out"] = 0.0
        obj.db.batt["in"] = 0.0
        obj.db.batt["out"] = 0.0
        obj.db.aux["in"] = 0.0
        obj.db.aux["out"] = 0.0
        obj.db.move["in"] = 0.0
        obj.db.move["out"] = 0.0
        obj.db.move["v"] = 0.0
        obj.db.move["time"] = gametime.gametime(absolute=True)
        obj.db.engine["warp_max"] = 0.0
        obj.db.engine["impulse_max"] = 0.0
        obj.db.power["main"] = 0.0
        obj.db.power["aux"] = 0.0
        obj.db.power["batt"] = 0.0
        obj.db.power["total"] = 0.0
        obj.db.sensor["lrs_active"] = 0
        obj.db.sensor["srs_active"] = 0
        obj.db.sensor["ew_active"] = 0
        obj.db.sensor["contacts"] = 0
        obj.db.sensor["counter"] = 0
        obj.db.cloak["active"] = 0
        obj.db.trans["active"] = 0
        obj.db.trans["d_lock"] = 0
        obj.db.trans["s_lock"] = 0
        obj.db.tract["active"] = 0
        obj.db.tract["lock"] = 0
        if (obj.db.status["tractoring"]):
            x = self.db.status["tractoring"]
            obj_x = search_object(x)[0]
            obj_x.db.status["tractored"] = 0
            obj.db.status["tractoring"] = 0
        obj.db.status["active"] = 1
        obj.db.status["time"] = obj.db.move["time"]
        obj.db.status["autopilot"] = 0
        iterate.up_cochranes(self)
        iterate.up_empire(self)
        iterate.up_vectors(self)
        iterate.up_resolution(self)
        iterate.up_signature(self)
        iterate.up_visibility(self)
        do_space_db_write(self,obj)
        return 1
    return 0
    
def do_set_main_reactor(self,level,obj):
    if(errors.error_on_console(self,obj)):
        return 0
    elif(not obj.db.main["exist"]):
        alerts.notify(self,alerts.ansi_red(obj.name + " has no M/A reactor."))
    elif(obj.db.main["damage"] <= -1.0):
        alerts.notify(self,alerts.ansi_red("M/A reactor controls are inoperative."))
    elif(obj.db.fuel["antimatter"] <= 0.0):
        alerts.notify(self,alerts.ansi_red("There is no antimattter fuel."))
    elif(obj.db.fuel["deuterium"] <= 0.0):
        alerts.notify(self,alerts.ansi_red("There is no deuterium fuel."))
    else:
        if (level < 0.0):
            obj.db.main["in"] = 0.0
        elif(level > obj.db.tech["main_max"]):
            obj.db.main["in"] = obj.db.tech["main_max"]
        else:
            obj.db.main["in"] = level
        if (obj.db.main["in"] > obj.db.main["damage"]):
            alerts.console_message(obj,["engineering"],ansi_cmd(self.name,"M/A reactor set at " + "{:10.3f}".format(obj.db.main["in"] * 100.0) + alerts.ansi_blink(" |rOVERLOAD|H")))
        else:
            alerts.console_message(obj,["engineering"],ansi_cmd(self.name,"M/A reactor set at " + "{:10.3f}".format(obj.db.main["in"] * 100.0)))
        return 1
    return 0
    
def do_set_aux_reactor(self,level,obj):
    if(errors.error_on_console(self,obj)):
        return 0
    elif(not obj.db.aux["exist"]):
        alerts.notify(self,alerts.ansi_red(obj.name + " has no Fusion reactor."))
    elif(obj.db.main["damage"] <= -1.0):
        alerts.notify(self,alerts.ansi_red("Fusion reactor controls are inoperative."))
    elif(obj.db.fuel["deuterium"] <= 0.0):
        alerts.notify(self,alerts.ansi_red("There is no deuterium fuel."))
    else:
        if (level < 0.0):
            obj.db.aux["in"] = 0.0
        elif(level > obj.db.tech["aux_max"]):
            obj.db.aux["in"] = obj.db.tech["aux_max"]
        else:
            obj.db.aux["in"] = level
        if (obj.db.aux["in"] > obj.db.aux["damage"]):
            alerts.console_message(obj,["engineering"],ansi_cmd(self.name,"Fusion reactor set at " + "{:10.3f}".format(obj.db.aux["in"] * 100.0) + alerts.ansi_blink(" |rOVERLOAD|H")))
        else:
            alerts.console_message(obj,["engineering"],ansi_cmd(self.name,"Fusion reactor set at " + "{:10.3f}".format(obj.db.aux["in"] * 100.0)))
        return 1
    return 0