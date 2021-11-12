"""
Sets the variables
"""
from world import alerts,constants,iterate, errors,utils,balance,unparse
from evennia.utils.search import search_object
from evennia import gametime
import math

def do_set_coords_manual(self,obj,x,y,z):
    if (errors.error_on_console(self,obj)):
        return 0
    else:
        obj.db.coords["xo"] = obj.db.coords["x"] - utils.pc2su(x)
        obj.db.coords["yo"] = obj.db.coords["y"] - utils.pc2su(y)
        obj.db.coords["zo"] = obj.db.coords["z"] - utils.pc2su(z)
        alerts.do_console_notify(self,["helm"],alerts.ansi_cmd(self.name,"Relative coordinates set to " + str("{:10.3f}".format(x)) + " " +  str("{:10.3f}".format(y)) + " " + str("{:10.3f}".format(z))))
        return 1
    return 0

def do_set_coords_reset(self,obj):
    if (errors.error_on_console(self,obj)):
        return 0
    else:
        obj.db.coords["xo"] = 0
        obj.db.coords["yo"] = 0
        obj.db.coords["zo"] = 0
        alerts.do_console_notify(self,["helm"],alerts.ansi_cmd(self.name,"Relative coordinates reset to " + str("{:10.3f}".format(utils.su2pc(obj.db.coords["x"]))) + " " +  str("{:10.3f}".format(utils.su2pc(obj.db.coords["x"]))) + " " + str("{:10.3f}".format(utils.su2pc(obj.db.coords["x"])))))
        return 1
    return 0

def do_set_coords_layin(self,obj,x,y,z):
    if (errors.error_on_console(self,obj)):
        return 0
    elif (obj.db.status["connected"]):
        alerts.notify(self,alerts.ansi_red(obj.name + " is still connected."))
    elif (not obj.db.engine["warp_exist"] and not obj.db.engine["impulse_exist"]):
        alerts.notify(self,alerts.ansi_red(obj.name + " cannot be maneuvered."))
    else:
        obj.db.coords["xd"] = utils.pc2su(x) + obj.db.coords["xo"];
        obj.db.coords["yd"] = utils.pc2su(y) + obj.db.coords["yo"];
        obj.db.coords["zd"] = utils.pc2su(z) + obj.db.coords["zo"];
        alerts.do_console_notify(self,["helm"],alerts.ansi_cmd(self.name,"Coordinates " + str("{:10.3f}".format(utils.su2pc(obj.db.coords["xd"]))) + " " +  str("{:10.3f}".format(utils.su2pc(obj.db.coords["yd"]))) + " " + str("{:10.3f}".format(utils.su2pc(obj.db.coords["zd"]))) + " laid in"))
        return 1
    return 0

def do_set_coords_engage(self,obj):

    if (errors.error_on_console(self,obj)):
        return 0
    elif(obj.db.status["docked"]):
        alerts.notify(self, alerts.ansi_red(obj.name + " is in dock."))
    elif(obj.db.status["landed"]):
        alerts.notify(self, alerts.ansi_red(obj.name + " is on a landing pad."))
    elif(obj.db.status["connected"]):
        alerts.notify(self, alerts.ansi_red(obj.name + " is still connected."))
    elif(obj.db.engine["warp_exist"] == 0 and obj.db.engine["impulse_exist"] == 0):
        alerts.notify(self, alerts.ansi_red(obj.name + " cannot be maneuvered."))
    else:
        delta_x = obj.db.coords["xd"] - obj.db.coords["x"]
        delta_y = obj.db.coords["yd"] - obj.db.coords["y"]
        yaw_in = utils.xy2bearing(delta_x,delta_y)
        obj.db.course["yaw_in"] = yaw_in
        obj.db.course["pitch_in"] = float(utils.xyz2elevation(obj.db.coords["xd"] - obj.db.coords["x"],obj.db.coords["yd"] - obj.db.coords["y"],obj.db.coords["zd"] - obj.db.coords["z"]))
        alerts.do_console_notify(self,["helm"],alerts.ansi_cmd(self.name,"Course " + str("{:3.3f}".format(obj.db.course["yaw_in"])) + " " +  str("{:3.3f}".format(obj.db.course["pitch_in"])) + " engaged"))
        return 1
    return 0


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
            obj.db.blist[i]["lock"] = 0
            obj.db.blist[i]["active"] = 0
        obj.db.missile["in"] = 0.0
        obj.db.missile["out"] = 0.0
        for i in range(obj.db.missile["tubes"]):
            obj.db.mlist[i]["lock"] = 0
            obj.db.mlist[i]["active"] = 0
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
            x = obj.db.status["tractoring"]
            obj_x = search_object(x)[0]
            obj_x.db.status["tractored"] = 0
            obj.db.status["tractoring"] = 0
        obj.db.status["active"] = 0
        obj.db.status["time"] = obj.db.move["time"]
        obj.db.status["autopilot"] = 0
        iterate.up_cochranes(obj)
        iterate.up_empire(obj)
        iterate.up_vectors(obj)
        iterate.up_resolution(obj)
        iterate.up_signature(obj)
        iterate.up_visibility(obj)
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
            obj.db.blist[i]["lock"] = 0
            obj.db.blist[i]["active"] = 0
        obj.db.missile["in"] = 0.0
        obj.db.missile["out"] = 0.0
        for i in range(obj.db.missile["tubes"]):
            obj.db.mlist[i]["lock"] = 0
            obj.db.mlist[i]["active"] = 0
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
            x = obj.db.status["tractoring"]
            obj_x = search_object(x)[0]
            obj_x.db.status["tractored"] = 0
            obj.db.status["tractoring"] = 0
        obj.db.status["active"] = 1
        obj.db.status["time"] = obj.db.move["time"]
        obj.db.status["autopilot"] = 0
        iterate.up_cochranes(obj)
        iterate.up_empire(obj)
        iterate.up_vectors(obj)
        iterate.up_resolution(obj)
        iterate.up_signature(obj)
        iterate.up_visibility(obj)
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
            alerts.console_message(obj,["engineering"],alerts.ansi_cmd(self.name,"M/A reactor set at " + "{:10.3f}".format(obj.db.main["in"] * 100.0) + alerts.ansi_blink(" |rOVERLOAD|n")))
        else:
            alerts.console_message(obj,["engineering"],alerts.ansi_cmd(self.name,"M/A reactor set at " + "{:10.3f}".format(obj.db.main["in"] * 100.0)))
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
            alerts.console_message(obj,["engineering"],alerts.ansi_cmd(self.name,"Fusion reactor set at " + "{:10.3f}".format(obj.db.aux["in"] * 100.0) + alerts.ansi_blink(" |rOVERLOAD|n")))
        else:
            alerts.console_message(obj,["engineering"],alerts.ansi_cmd(self.name,"Fusion reactor set at " + "{:10.3f}".format(obj.db.aux["in"] * 100.0)))
        return 1
    return 0
    
def do_set_battery(self,level,obj):
    if(errors.error_on_console(self,obj)):
        return 0
    elif(not obj.db.batt["exist"]):
        alerts.notify(self,alerts.ansi_red(obj.name + " has no batteries."))
    elif(obj.db.main["damage"] <= 0.0):
        alerts.notify(self,alerts.ansi_red("Batteries are inoperative."))
    elif(obj.db.fuel["reserves"] <= 0.0):
        alerts.notify(self,alerts.ansi_red("There is no battery power."))
    else:
        if (level < 0.0):
            obj.db.batt["in"] = 0.0
        elif(level > 1.0):
            obj.db.batt["in"] = 1.0
        else:
            obj.db.batt["in"] = level
            alerts.console_message(obj,["engineering"],alerts.ansi_cmd(self.name,"Batteries set at " + "{:10.3f}".format(obj.db.batt["in"] * 100.0)))
        return 1
    return 0

def do_set_lrs(self,active,obj):
    if(errors.error_on_console(self,obj)):
        return 0
    elif(not obj.db.sensor["lrs_exist"]):
        alerts.notify(self,alerts.ansi_red(obj.name + " has no long-range sensors."))
    elif(obj.db.sensor["lrs_damage"] <= 0.0):
        alerts.notify(self,alerts.ansi_red("Long-range sensors are inoperative."))
    else:
        if (active):
            if(obj.db.sensor["lrs_active"]):
                alerts.notify(self,alerts.ansi_red("Long-range sensors are already online."))
            else:
                obj.db.sensor["lrs_active"] = 1
                obj.db.sensor["version"] = 1
                alerts.console_message(obj,["helm","science","tactical"],alerts.ansi_cmd(self.name,"Long-range sensors online"))
                return 1
        else:
            if(not obj.db.sensor["lrs_active"]):
                alerts.notify(self,alerts.ansi_red("Long-range sensors are already offline."))
            else:
                obj.db.sensor["lrs_active"] = 0
                obj.db.sensor["version"] = 1
                alerts.console_message(obj,["helm","science","tactical"],alerts.ansi_cmd(self.name,"Long-range sensors offline"))
                return 1
    return 0
    
def do_set_srs(self,active,obj):
    if(errors.error_on_console(self,obj)):
        return 0
    elif(not obj.db.sensor["srs_exist"]):
        alerts.notify(self,alerts.ansi_red(obj.name + " has no short-range sensors."))
    elif(obj.db.sensor["srs_damage"] <= 0.0):
        alerts.notify(self,alerts.ansi_red("Short-range sensors are inoperative."))
    elif(obj.db.cloak["active"] and obj.db.tech["cloak"] < 2.0):
        alerts.notify(self,alerts.ansi_red(obj.name + " cannot use short-range sensors while cloaked."))
    else:
        if (active):
            if(obj.db.sensor["srs_active"]):
                alerts.notify(self,alerts.ansi_red("Short-range sensors are already online."))
            else:
                obj.db.sensor["srs_active"] = 1
                obj.db.sensor["version"] = 1
                alerts.console_message(obj,["helm","science","tactical"],alerts.ansi_cmd(self.name,"Short-range sensors online"))
                return 1
        else:
            if(not obj.db.sensor["srs_active"]):
                alerts.notify(self,alerts.ansi_red("Short-range sensors are already offline."))
            else:
                obj.db.sensor["srs_active"] = 0
                obj.db.sensor["version"] = 1
                alerts.console_message(obj,["helm","science","tactical"],alerts.ansi_cmd(self.name,"Short-range sensors offline"))
                return 1
    return 0
    
def do_set_ew(self,active,obj):
    if(errors.error_on_console(self,obj)):
        return 0
    elif(not obj.db.sensor["ew_exist"]):
        alerts.notify(self,alerts.ansi_red(obj.name + " has no electronic warfare systems."))
    elif(obj.db.sensor["ew_damage"] <= 0.0):
        alerts.notify(self,alerts.ansi_red("Electronic warfare systems are inoperative."))
    elif(obj.db.cloak["active"] and obj.db.tech["cloak"] < 2.0):
        alerts.notify(self,alerts.ansi_red(obj.name + " cannot use electronic warfare systems while cloaked."))
    else:
        if (active):
            if(obj.db.sensor["ew_active"]):
                alerts.notify(self,alerts.ansi_red("Electronic warfare systems are already online."))
            else:
                obj.db.sensor["ew_active"] = 1
                obj.db.sensor["version"] = 1
                alerts.console_message(obj,["helm","science","tactical"],alerts.ansi_cmd(self.name,"Electronic warfare systems online"))
                return 1
        else:
            if(not obj.db.sensor["ew_active"]):
                alerts.notify(self,alerts.ansi_red("Electronic warfare systems are already offline."))
            else:
                obj.db.sensor["ew_active"] = 0
                obj.db.sensor["version"] = 1
                alerts.console_message(obj,["helm","science","tactical"],alerts.ansi_cmd(self.name,"Electronic warfare systems offline"))
                return 1
    return 0
    

def do_set_cloak(self,active,obj):
    if(errors.error_on_console(self,obj)):
        return 0
    elif(not obj.db.cloak["exist"]):
        alerts.notify(self,alerts.ansi_red(obj.name + " has no cloaking device."))
    elif(obj.db.cloak["damage"] <= 0.0):
        alerts.notify(self,alerts.ansi_red("Cloaking device is inoperative."))
    else:
        if (active):
            if(obj.db.cloak["active"]):
                alerts.notify(self,alerts.ansi_red("Cloaking device is already online"))
                return 0
            elif(obj.db.alloc["cloak"] * obj.db.power["total"] < obj.db.cloak["cost"]):
                alerts.notify(self,alerts.ansi_red("Insufficient power for cloaking device."))
                return 0
            elif(obj.db.tech["cloak"] < 2.0):
                if(obj.db.sensor["srs_active"]):
                    obj.db.sensor["srs_active"] = 0
                    alerts.console_message(self,["helm","science","tactical"],alerts.ansi_cmd(self.name,"Short-range sensors offline"))
                if(obj.db.sensor["ew_active"]):
                    obj.db.sensor["ew_active"] = 0
                    alerts.console_message(self,["helm","science","tactical"],alerts.ansi_cmd(self.name,"Electronic warfare systems offline"))
                if(obj.db.trans["active"]):
                    obj.db.trans["active"] = 0
                    obj.db.trans["d_lock"] = 0
                    obj.db.trans["s_lock"] = 0
                    alerts.console_message(self,["helm","operation","transporter"],alerts.ansi_cmd(self.name,"Transporters offline"))
                if(obj.db.tract["active"]):
                    obj.db.tract["active"] = 0
                    obj.db.tract["lock"] = 0
                    if obj.db.status["tractoring"]:
                        x = obj.db.status["tractoring"]
                        obj_x = search_object(x)[0]
                        alerts.tract_unlock(self,obj,obj_x)
                        obj_x.db.status["tractored"] = 0
                        obj.power["version"] = 1
                        obj_x.power["version"] = 1
                    alerts.console_message(self,["helm","operation"],alerts.ansi_cmd(self.name,"Tractor beams offline"))
                if(obj.db.beam["exist"]):
                    for i in range(obj.db.beam["banks"]):
                        obj.db.blist[i]["lock"] = 0
                if(obj.db.missile["exist"]):
                    for i in range(obj.db.missile["tubes"]):
                        obj.db.mlist[i]["lock"] = 0
                if (obj.db.shield["exist"]):
                    flag = 0
                    buffer = ""
                    for i in range(constants.MAX_SHIELD_NAME):
                        if(obj.db.shield[i]["active"]):
                            if (flag):
                                buffer += "\n"
                            obj.db.shield[i]["active"] = 0
                            buffer += alerts.ansi_cmd(self.name,constants.SHIELD_NAME[i] + " offline")
                            flag += 1
                    if (flag):
                        alerts.console_message(self,["helm"],buffer)
                obj.db.cloak["active"] = 1
                obj.db.sensor["version"] = 1
                alerts.console_message(self,["helm","tactical"],alerts.ansi_cmd(self.name,"Cloaking device online"))
                alerts.ship_cloak_online(obj)
                return 1
        else:
            if (not obj.db.cloak["active"]):
                alerts.notify(self,alerts.ansi_red("Cloaking device is already offline"))
                return 0
            else:
                if(obj.db.tech["cloak"] < 2.0):
                    if(not obj.db.sensor["srs_active"]):
                        obj.db.sensor["srs_active"] = 1
                        alerts.console_message(self,["helm","science","tactical"],alerts.ansi_cmd(self.name,"Short-range sensors online"))
                    if(not obj.db.sensor["ew_active"]):
                        obj.db.sensor["ew_active"] = 1
                        alerts.console_message(self,["helm","science","tactical"],alerts.ansi_cmd(self.name,"Electronic warfare systems online"))
                obj.db.cloak["active"] = 0
                obj.db.sensor["version"] = 1
                obj.db.engine["version"] = 1
                alerts.console_message(self,["helm","tactical"],alerts.ansi_cmd(self.name,"Cloaking device offline"))
                alerts.ship_cloak_offline(obj)
                return 1
                

def do_set_eng_alloc(self, helm, tactical, operations, obj):
    if (errors.error_on_console(self,obj)):
        return 0
    else:
        obj.db.alloc["helm"] = math.fabs(helm)
        obj.db.alloc["tactical"] = math.fabs(tactical)
        obj.db.alloc["operations"] = math.fabs(operations)
        balance.balance_eng_power(obj)
        balance.balance_helm_power(obj);
        balance.balance_shield_power(obj)
        balance.balance_tact_power(obj)
        balance.balance_sensor_power(obj)
        balance.balance_ops_power(obj)
        alerts.report_eng_power(obj)
        alerts.report_helm_power(obj)
        alerts.report_tact_power(obj)
        alerts.report_ops_power(obj)
        obj.db.engine["version"] = 1
        obj.db.sensor["version"] = 1
        obj.db.cloak["version"] = 1
        return 1
    return 0
    
def do_set_helm_alloc (self, movement, shields, cloak, obj):
    if (errors.error_on_console(self,obj)):
        return 0
    else:
        obj.db.alloc["movement"] = math.fabs(movement)
        obj.db.alloc["shields"] = math.fabs(shields)
        obj.db.alloc["cloak"] = math.fabs(cloak)
        balance.balance_helm_power(obj)
        balance.balance_shield_power(obj)
        alerts.report_helm_power(obj)
        obj.db.engine["version"] = 1
        obj.db.sensor["version"] = 1
        obj.db.cloak["version"] = 1
        return 1
    return 0
    
def do_set_shield_alloc (self, forward, starboard, aft, port, dorsal, ventral, obj):
    if (errors.error_on_console(self,obj)):
        return 0
    else:
        obj.db.alloc["shield"][0] = math.fabs(forward)
        obj.db.alloc["shield"][1] = math.fabs(starboard)
        obj.db.alloc["shield"][2] = math.fabs(aft)
        obj.db.alloc["shield"][3] = math.fabs(port)
        obj.db.alloc["shield"][4] = math.fabs(dorsal)
        obj.db.alloc["shield"][5] = math.fabs(ventral)
        balance.balance_shield_power(obj)
        alerts.report_shield_power(obj)
        self.db.engine["version"] = 1
        return 1
    return 0

def do_set_autopilot (self, obj, flag):
    if (errors.error_on_console(self,obj)):
        return 0
    elif (obj.db.status["docked"] == 1):
        alerts.notify(self,alerts.ansi_red(obj.name + " is in dock."))
    elif(obj.db.status["landed"] == 1):
        alerts.notify(self,alerts.ansi_red(obj.name + " is on a landing pad."))
    elif(obj.db.status["connected"] == 1):
        alerts.notify(self,alerts.ansi_red(obj.name + " is still connected."))
    elif(not obj.db.engine["warp_exist"] and not obj.db.engine["impulse_exist"]):
        alerts.notify(self,alerts.ansi_red(obj.name + " cannot be maneuvered."))
    elif(obj.db.status["autopilot"] > 0):
        if (flag == 1):
            alerts.notify(self,alerts.ansi_red("Autopilot is already engaged."))
        else:
            obj.db.status["autopilot"] = 0
            alerts.console_message(self,["helm"],alerts.ansi_cmd(self.name,"Autopilot disengaged"))
            return 1
    else:
        if (flag == 0):
            alerts.notify(self,alerts.ansi_red("Autopilot is already disengaged."))
        elif(obj.db.coords["xd"] == obj.db.coords["x"] and obj.db.coords["yd"] == obj.db.coords["y"] and obj.db.coords["zd"] == obj.db.coords["z"]):
            alerts.notify(self,alerts.ansi_red(obj.name + " is already there."))
        else:
            obj.db.status["autopilot"] = 100
            alerts.console_message(self,["helm"],alerts.ansi_cmd(self.name,"Autopilot engaged"))
            return 1
    return 0
    
def do_set_intercept(self, obj, contact):
    if (errors.error_on_console(self,obj)):
        return 0
    elif (obj.db.status["docked"] == 1):
        alerts.notify(self,alerts.ansi_red(obj.name + " is in dock."))
    elif(obj.db.status["landed"] == 1):
        alerts.notify(self,alerts.ansi_red(obj.name + " is on a landing pad."))
    elif(obj.db.status["connected"] == 1):
        alerts.notify(self,alerts.ansi_red(obj.name + " is still connected."))
    elif(not obj.db.engine["warp_exist"] and not obj.db.engine["impulse_exist"]):
        alerts.notify(self,alerts.ansi_red(obj.name + " cannot be maneuvered."))
    else:
        obj_x = utils.contact2sdb(obj,contact)
        if (errors.error_on_contact(self,obj,obj_x)):
            return 0
        else:
            obj.db.coords["xd"] = obj_x.db.coords["x"]
            obj.db.coords["yd"] = obj_x.db.coords["y"]
            obj.db.coords["zd"] = obj_x.db.coords["z"]
            obj.db.coords["yaw_in"] = utils.sdb2bearing(obj,obj_x)
            obj.db.coords["pitch_in"] = utils.sdb2elevation(obj,obj_x)
            if (obj.db.course["roll_in"] != 0):
                alerts.console_message(self,["helm"],alerts.ansi_cmd(self.name,"Intercept course to {:s} set {:.3f} {:.3f} {:.3f}".format(unparse.unparse_identity(obj,obj_x), obj.db.coords["yaw_in"], obj.db.coords["pitch_in"],obj.db.coords["roll_in"])))
            else:
                alerts.console_message(self,["helm"],alerts.ansi_cmd(self.name,"Intercept course to {:s} set {:.3f} {:.3f}".format(unparse.unparse_identity(obj,obj_x), obj.db.coords["yaw_in"], obj.db.coords["pitch_in"])))
            return 1
    return 0

def do_set_refuel(self, obj, receiver,type,tons):
    if (errors.error_on_console(self,obj)):
        return 0
    
    if(type[0].lower() == "a"):
        type = 1
    elif(type[0].lower() == "d"):
        type = 2
    elif(type[0].lower() == "r"):
        type = 3
    else:
        type = 0
    
    if (type == 0):
        alerts.notify(self,alerts.ansi_red("That is not a valid fuel type."))
        return 0
    elif (tons <= 0.0):
        alerts.notify(self,alerts.ansi_red("That is not a valid fuel amount."))
        return 0    
    elif (utils.sdb2contact(obj,receiver) == constants.SENSOR_FAIL):
        alerts.notify(self,alerts.ansi_red("That is not a valid fuel recepient"))
        return 0
    elif (receiver.db.location is not obj.name):
        alerts.notify(self,alerts.ansi_red("That is not a valid fuel recepient"))
        return 0
    elif (receiver.db.status["connected"] != 0):
        alerts.notify(self,alerts.ansi_red(receiver.name + " is not connected"))
        return 0
    elif(type == 1):
        amount = tons * 1000000.0
        available = obj.db.fuel["antimatter"]
        capacity = utils.sdb2max_antimatter(receiver) - receiver.db.fuel["antimatter"]
        if (amount > available):
            alerts.notify(self,alerts.ansi_red(" {:s} has only {:f} tons of antimatter available".format(obj.name,available / 1000000)))
        elif(capacity <= 0):
            alerts.notify(self,alerts.ansi_red(" {:s} has no antimatter capacity".format(receiver.name)))
        elif(amount > capacity):
            alerts.notify(self,alerts.ansi_red(" {:s} has only {:f} tons of antimatter capacity".format(receiver.name,capacity / 1000000)))
        else:
            receiver.db.fuel["antimatter"] += amount
            obj.db.fuel["antimatter"] -= amount
            alerts.console_message(obj,["engineering","operation"],alerts.ansi_cmd("{:f} tons of antimatter transferred to {:s}".format(amount,receiver.name)))
            alerts.console_message(receiver,["engineering","operation"],alerts.ansi_cmd("{:f} tons of antimatter transferred from {:s}".format(amount,obj.name)))
            return 1
    elif(type == 2):
        amount = tons * 1000000.0
        available = obj.db.fuel["deuterium"]
        capacity = utils.sdb2max_deuterium(receiver) - receiver.db.fuel["deuterium"]
        if (amount > available):
            alerts.notify(self,alerts.ansi_red(" {:s} has only {:f} tons of deuterium available".format(obj.name,available / 1000000)))
        elif(capacity <= 0):
            alerts.notify(self,alerts.ansi_red(" {:s} has no deuterium capacity".format(receiver.name)))
        elif(amount > capacity):
            alerts.notify(self,alerts.ansi_red(" {:s} has only {:f} tons of deuterium capacity".format(receiver.name,capacity / 1000000)))
        else:
            receiver.db.fuel["deuterium"] += amount
            obj.db.fuel["deuterium"] -= amount
            alerts.console_message(obj,["engineering","operation"],alerts.ansi_cmd("{:f} tons of deuterium transferred to {:s}".format(amount,receiver.name)))
            alerts.console_message(receiver,["engineering","operation"],alerts.ansi_cmd("{:f} tons of deuterium transferred from {:s}".format(amount,obj.name)))
            return 1
    elif(type == 3):
        amount = tons * 3600.0
        available = obj.db.fuel["reserves"]
        capacity = utils.sdb2max_reserves(receiver) - receiver.db.fuel["reserves"]
        if (amount > available):
            alerts.notify(self,alerts.ansi_red(" {:s} has only {:f} GW hours of reserve available".format(obj.name,available / 3600.0)))
        elif(capacity <= 0):
            alerts.notify(self,alerts.ansi_red(" {:s} has no reserve capacity".format(receiver.name)))
        elif(amount > capacity):
            alerts.notify(self,alerts.ansi_red(" {:s} has only {:f} GW hours of reserve capacity".format(receiver.name,capacity / 3600.0)))
        else:
            receiver.db.fuel["reserves"] += amount
            obj.db.fuel["reserves"] -= amount
            alerts.console_message(obj,["engineering","operation"],alerts.ansi_cmd("{:f} GW hours of reserves transferred to {:s}".format(amount,receiver.name)))
            alerts.console_message(receiver,["engineering","operation"],alerts.ansi_cmd("{:f} GW hours of reserves transferred from {:s}".format(amount,obj.name)))
            return 1
    return 0

def do_set_defuel(self, obj, receiver,type,tons):
    if (errors.error_on_console(self,obj)):
        return 0
    
    if(type[0].lower() == "a"):
        type = 1
    elif(type[0].lower() == "d"):
        type = 2
    elif(type[0].lower() == "r"):
        type = 3
    else:
        type = 0
    
    if (type == 0):
        alerts.notify(self,alerts.ansi_red("That is not a valid fuel type."))
        return 0
    elif (tons <= 0.0):
        alerts.notify(self,alerts.ansi_red("That is not a valid fuel amount."))
        return 0    
    if (receiver is not None):
        if (utils.sdb2contact(obj,receiver) == constants.SENSOR_FAIL):
            alerts.notify(self,alerts.ansi_red("That is not a valid fuel recepient"))
            return 0
        elif (receiver.db.location is not obj.name):
            alerts.notify(self,alerts.ansi_red("That is not a valid fuel recepient"))
            return 0
        elif (receiver.db.status["connected"] != 0):
            alerts.notify(self,alerts.ansi_red(receiver.name + " is not connected"))
            return 0
        elif(type == 1):
            amount = tons * 1000000.0
            available = obj.db.fuel["antimatter"]
            capacity = utils.sdb2max_antimatter(receiver) - receiver.db.fuel["antimatter"]
            if (amount > available):
                alerts.notify(self,alerts.ansi_red(" {:s} has only {:f} tons of antimatter available".format(obj.name,available / 1000000)))
            elif(capacity <= 0):
                alerts.notify(self,alerts.ansi_red(" {:s} has no antimatter capacity".format(receiver.name)))
            elif(amount > capacity):
                alerts.notify(self,alerts.ansi_red(" {:s} has only {:f} tons of antimatter capacity".format(receiver.name,capacity / 1000000)))
            else:
                receiver.db.fuel["antimatter"] += amount
                obj.db.fuel["antimatter"] -= amount
                alerts.console_message(obj,["engineering","operation"],alerts.ansi_cmd("{:f} tons of antimatter transferred to {:s}".format(amount,receiver.name)))
                alerts.console_message(receiver,["engineering","operation"],alerts.ansi_cmd("{:f} tons of antimatter transferred from {:s}".format(amount,obj.name)))
                return 1
        elif(type == 2):
            amount = tons * 1000000.0
            available = obj.db.fuel["deuterium"]
            capacity = utils.sdb2max_deuterium(receiver) - receiver.db.fuel["deuterium"]
            if (amount > available):
                alerts.notify(self,alerts.ansi_red(" {:s} has only {:f} tons of deuterium available".format(obj.name,available / 1000000)))
            elif(capacity <= 0):
                alerts.notify(self,alerts.ansi_red(" {:s} has no deuterium capacity".format(receiver.name)))
            elif(amount > capacity):
                alerts.notify(self,alerts.ansi_red(" {:s} has only {:f} tons of deuterium capacity".format(receiver.name,capacity / 1000000)))
            else:
                receiver.db.fuel["deuterium"] += amount
                obj.db.fuel["deuterium"] -= amount
                alerts.console_message(obj,["engineering","operation"],alerts.ansi_cmd("{:f} tons of deuterium transferred to {:s}".format(amount,receiver.name)))
                alerts.console_message(receiver,["engineering","operation"],alerts.ansi_cmd("{:f} tons of deuterium transferred from {:s}".format(amount,obj.name)))
                return 1
        elif(type == 3):
            amount = tons * 3600.0
            available = obj.db.fuel["reserves"]
            capacity = utils.sdb2max_reserves(receiver) - receiver.db.fuel["reserves"]
            if (amount > available):
                alerts.notify(self,alerts.ansi_red(" {:s} has only {:f} GW hours of reserve available".format(obj.name,available / 3600.0)))
            elif(capacity <= 0):
                alerts.notify(self,alerts.ansi_red(" {:s} has no reserve capacity".format(receiver.name)))
            elif(amount > capacity):
                alerts.notify(self,alerts.ansi_red(" {:s} has only {:f} GW hours of reserve capacity".format(receiver.name,capacity / 3600.0)))
            else:
                receiver.db.fuel["reserves"] += amount
                obj.db.fuel["reserves"] -= amount
                alerts.console_message(obj,["engineering","operation"],alerts.ansi_cmd("{:f} GW hours of reserves transferred to {:s}".format(amount,receiver.name)))
                alerts.console_message(receiver,["engineering","operation"],alerts.ansi_cmd("{:f} GW hours of reserves transferred from {:s}".format(amount,obj.name)))
                return 1
        return 0
    else:
        #dumping...
        if(type == 1):
            amount = tons * 1000000.0
            available = obj.db.fuel["antimatter"]
            if (amount > available):
                amount = available
            obj.db.fuel["antimatter"] -= amount
            alerts.console_message(obj,["engineering","operation"],alerts.ansi_cmd("{:f} tons of antimatter dumped into space".format(amount)))
            return 1
        elif(type == 2):
            amount = tons * 1000000.0
            available = obj.db.fuel["deuterium"]
            if (amount > available):
                amount = available
            obj.db.fuel["deuterium"] -= amount
            alerts.console_message(obj,["engineering","operation"],alerts.ansi_cmd("{:f} tons of deuterium dumped into space".format(amount)))
        elif(type == 3):
            amount = tons * 3600.0
            available = obj.db.fuel["reserves"]
            if (amount > available):
                amount = available
            obj.db.fuel["reserves"] -= amount
            alerts.console_message(obj,["engineering","operation"],alerts.ansi_cmd("{:f} GW hours of reserves dumped into space".format(amount)))
            return 1
    return 0