"""
Sets the variables
"""
from evennia.utils import ansi
from typeclasses.characters import Character
from typeclasses.objects import Object
from world import alerts,constants,iterate, errors,utils,balance,unparse,damage
from evennia.utils.search import search_object
from evennia import gametime
import math
import random

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

def do_set_yaw(self,obj,value):

    if (errors.error_on_console(self,obj)):
        return 0
    elif(obj.db.status["docked"]):
        alerts.notify(self, alerts.ansi_red("{:s} is in dock.".format(obj.name)))
    elif(obj.db.status["landed"]):
        alerts.notify(self, alerts.ansi_red("{:s} is on a landing pad.".format(obj.name)))
    elif(obj.db.status["connected"]):
        alerts.notify(self, alerts.ansi_red("{:s} is still connected.".format(obj.name)))
    elif(obj.db.engine["warp_exist"] == 0 and obj.db.engine["impulse_exist"] == 0):
        alerts.notify(self, alerts.ansi_red("{:s} cannot be maneuvered.".format(obj.name)))
    elif(math.fabs(value) > 360.0):
        alerts.notify(self, alerts.ansi_red("That is not a valid yaw value."))
    else:
        if(obj.db.status["autopilot"] != 0):
            obj.db.status["autopilot"] = 0
            alerts.console_message(obj,["helm"],alerts.ansi_cmd(self.name,"Autopilot disengaged"))
        obj.db.course["yaw_in"] = math.fmod(obj.db.course["yaw_in"] + value,360)
        if(obj.db.course["yaw_in"] < 0.0):
            obj.db.course["yaw_in"] += 360.0
        alerts.console_message(obj,["helm"],"Yaw adjusted {:+.3f} to {:.3f}".format(value,obj.db.course["yaw_in"]))
        return 1
    return 0

def do_set_pitch(self,obj,value):

    if (errors.error_on_console(self,obj)):
        return 0
    elif(obj.db.status["docked"]):
        alerts.notify(self, alerts.ansi_red("{:s} is in dock.".format(obj.name)))
    elif(obj.db.status["landed"]):
        alerts.notify(self, alerts.ansi_red("{:s} is on a landing pad.".format(obj.name)))
    elif(obj.db.status["connected"]):
        alerts.notify(self, alerts.ansi_red("{:s} is still connected.".format(obj.name)))
    elif(obj.db.engine["warp_exist"] == 0 and obj.db.engine["impulse_exist"] == 0):
        alerts.notify(self, alerts.ansi_red("{:s} cannot be maneuvered.".format(obj.name)))
    elif(math.fabs(value) > 360.0):
        alerts.notify(self, alerts.ansi_red("That is not a valid pitch value."))
    else:
        if(obj.db.status["autopilot"] != 0):
            obj.db.status["autopilot"] = 0
            alerts.console_message(obj,["helm"],alerts.ansi_cmd(self.name,"Autopilot disengaged"))
        obj.db.course["pitch_in"] = math.fmod(obj.db.course["pitch_in"] + value,360)
        if(obj.db.course["pitch_in"] < 0.0):
            obj.db.course["pitch_in"] += 360.0
        alerts.console_message(obj,["helm"],"Pitch adjusted {:+.3f} to {:.3f}".format(value,obj.db.course["pitch_in"]))
        return 1
    return 0

def do_set_roll(self,obj,value):

    if (errors.error_on_console(self,obj)):
        return 0
    elif(obj.db.status["docked"]):
        alerts.notify(self, alerts.ansi_red("{:s} is in dock.".format(obj.name)))
    elif(obj.db.status["landed"]):
        alerts.notify(self, alerts.ansi_red("{:s} is on a landing pad.".format(obj.name)))
    elif(obj.db.status["connected"]):
        alerts.notify(self, alerts.ansi_red("{:s} is still connected.".format(obj.name)))
    elif(obj.db.engine["warp_exist"] == 0 and obj.db.engine["impulse_exist"] == 0):
        alerts.notify(self, alerts.ansi_red("{:s} cannot be maneuvered.".format(obj.name)))
    elif(math.fabs(value) > 360.0):
        alerts.notify(self, alerts.ansi_red("That is not a valid roll value."))
    else:
        if(obj.db.status["autopilot"] != 0):
            obj.db.status["autopilot"] = 0
            alerts.console_message(obj,["helm"],alerts.ansi_cmd(self.name,"Autopilot disengaged"))
        obj.db.course["roll_in"] = math.fmod(obj.db.course["roll_in"] + value,360)
        if(obj.db.course["roll_in"] < 0.0):
            obj.db.course["roll_in"] += 360.0
        alerts.console_message(obj,["helm"],"Roll adjusted {:+.3f} to {:.3f}".format(value,obj.db.course["roll_in"]))
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
        obj.db.missile["in"] = 0.0
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

def do_set_tactical_alloc(self,obj,beams,missiles,sensors):
    if (errors.error_on_console(self,obj)):
        return 0
    else:
        obj.db.alloc["beams"] = math.fabs(beams)
        obj.db.alloc["missiles"] = math.fabs(missiles)
        obj.db.alloc["sensors"] = math.fabs(sensors)
        balance.balance_tact_power(obj)
        balance.balance_sensor_power(obj)
        alerts.report_tact_power(obj)
        obj.db.sensor["version"] = 1
        return 1    

def do_set_sensor_alloc(self,obj,ecm,eccm):
    if (errors.error_on_console(self,obj)):
        return 0
    else:
        obj.db.alloc["ecm"] = math.fabs(ecm)
        obj.db.alloc["eccm"] = math.fabs(eccm)
        balance.balance_sensor_power(obj)
        alerts.report_sensor_power(obj)
        obj.db.sensor["version"] = 1
        return 1

def do_set_shield_freq(self,obj,value):
    if (errors.error_on_console(self,obj)):
        return 0
    elif(obj.db.shield["exist"] == 0):
        alerts.notify(self,alerts.ansi_red("{:s} has no shields.".format(obj.name)))
    elif(value < 1.0 or value >= 1000.0):
        alerts.notify(self,alerts.ansi_red("Valid shield frequencies are from 1.00 to 999.999 Ghz"))
    else:
        obj.db.shield["freq"] = value
        alerts.console_message(obj,["engineering","helm"],"Shield frequencies set to {:.3f} Ghz".format(obj.db.shield["freq"]))
        alerts.write_spacelog(self,obj,"LOG: Shield frequencies set to {:.6f} Ghz".format(obj.db.shield["freq"]))
        return 1
    return 0

def do_set_cloak_freq(self,obj,value):
    if (errors.error_on_console(self,obj)):
        return 0
    elif(obj.db.cloak["exist"] == 0):
        alerts.notify(self,alerts.ansi_red("{:s} has no cloaking device.".format(obj.name)))
    elif(value < 1.0 or value >= 1000.0):
        alerts.notify(self,alerts.ansi_red("Valid cloaking device frequencies are from 1.00 to 999.999 Ghz"))
    else:
        obj.db.cloak["freq"] = value
        alerts.console_message(obj,["engineering","helm"],"Cloaking device frequencies set to {:.3f} Ghz".format(obj.db.cloak["freq"]))
        alerts.write_spacelog(self,obj,"LOG: Cloaking device frequency set to {:.6f} Ghz".format(obj.db.cloak["freq"]))
        return 1
    return 0

def do_set_beam_freq(self,obj,value):
    if (errors.error_on_console(self,obj)):
        return 0
    elif(obj.db.beam["exist"] == 0):
        alerts.notify(self,alerts.ansi_red("{:s} has no beam weapons.".format(obj.name)))
    elif(value < 1.0 or value >= 1000.0):
        alerts.notify(self,alerts.ansi_red("Valid beam weapon frequencies are from 1.00 to 999.999 Ghz"))
    else:
        obj.db.beam["freq"] = value
        alerts.console_message(obj,["engineering","tactical"],"Beam weapon frequencies set to {:.3f} Ghz".format(obj.db.beam["freq"]))
        alerts.write_spacelog(self,obj,"LOG: Beam weapon frequencies set to {:.6f} Ghz".format(obj.db.beam["freq"]))
        return 1
    return 0

def do_set_missile_freq(self,obj,value):
    if (errors.error_on_console(self,obj)):
        return 0
    elif(obj.db.missile["exist"] == 0):
        alerts.notify(self,alerts.ansi_red("{:s} has no missile weapons.".format(obj.name)))
    elif(value < 1.0 or value >= 1000.0):
        alerts.notify(self,alerts.ansi_red("Valid missile weapon frequencies are from 1.00 to 999.999 Ghz"))
    else:
        obj.db.missile["freq"] = value
        alerts.console_message(obj,["engineering","tactical"],"Missile weapon frequencies set to {:.3f} Ghz".format(obj.db.missile["freq"]))
        alerts.write_spacelog(self,obj,"LOG: Shield frequencies set to {:.6f} Ghz".format(obj.db.missile["freq"]))
        return 1
    return 0

def do_set_trans_freq(self,obj,value):
    if (errors.error_on_console(self,obj)):
        return 0
    elif(obj.db.trans["exist"] == 0):
        alerts.notify(self,alerts.ansi_red("{:s} has no transporter.".format(obj.name)))
    elif(value < 1.0 or value >= 1000.0):
        alerts.notify(self,alerts.ansi_red("Valid transporter frequencies are from 1.00 to 999.999 Ghz"))
    else:
        obj.db.trans["freq"] = value
        alerts.console_message(obj,["engineering","operation","transporter"],"Transporter frequency set to {:.3f} Ghz".format(obj.db.trans["freq"]))
        alerts.write_spacelog(self,obj,"LOG: Transporter frequency set to {:.6f} Ghz".format(obj.db.trans["freq"]))
        return 1
    return 0

def do_set_tract_freq(self,obj,value):
    if (errors.error_on_console(self,obj)):
        return 0
    elif(obj.db.tract["exist"] == 0):
        alerts.notify(self,alerts.ansi_red("{:s} has no tractor beam.".format(obj.name)))
    elif(value < 1.0 or value >= 1000.0):
        alerts.notify(self,alerts.ansi_red("Valid tractor beam frequencies are from 1.00 to 999.999 Ghz"))
    else:
        obj.db.tract["freq"] = value
        alerts.console_message(obj,["engineering","operation"],"Tractor beam frequency set to {:.3f} Ghz".format(obj.db.tract["freq"]))
        alerts.write_spacelog(self,obj,"LOG: Tractor beam frequency set to {:.6f} Ghz".format(obj.db.tract["freq"]))
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
                alerts.console_message(obj,["engineering","operation"],alerts.ansi_cmd(self.name,"{:f} tons of antimatter transferred to {:s}".format(amount,receiver.name)))
                alerts.console_message(receiver,["engineering","operation"],alerts.ansi_cmd(self.name,"{:f} tons of antimatter transferred from {:s}".format(amount,obj.name)))
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
                alerts.console_message(obj,["engineering","operation"],alerts.ansi_cmd(self.name,"{:f} tons of deuterium transferred to {:s}".format(amount,receiver.name)))
                alerts.console_message(receiver,["engineering","operation"],alerts.ansi_cmd(self.name,"{:f} tons of deuterium transferred from {:s}".format(amount,obj.name)))
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
                alerts.console_message(obj,["engineering","operation"],alerts.ansi_cmd(self.name,"{:f} GW hours of reserves transferred to {:s}".format(amount,receiver.name)))
                alerts.console_message(receiver,["engineering","operation"],alerts.ansi_cmd(self.name,"{:f} GW hours of reserves transferred from {:s}".format(amount,obj.name)))
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
            alerts.console_message(obj,["engineering","operation"],alerts.ansi_cmd(self.name,"{:f} tons of antimatter dumped into space".format(amount)))
            return 1
        elif(type == 2):
            amount = tons * 1000000.0
            available = obj.db.fuel["deuterium"]
            if (amount > available):
                amount = available
            obj.db.fuel["deuterium"] -= amount
            alerts.console_message(obj,["engineering","operation"],alerts.ansi_cmd(self.name,"{:f} tons of deuterium dumped into space".format(amount)))
        elif(type == 3):
            amount = tons * 3600.0
            available = obj.db.fuel["reserves"]
            if (amount > available):
                amount = available
            obj.db.fuel["reserves"] -= amount
            alerts.console_message(obj,["engineering","operation"],alerts.ansi_cmd(self.name,"{:f} GW hours of reserves dumped into space".format(amount)))
            return 1
    return 0

def do_set_fire(self,obj,first,last,weapon,mode):
    dmg_b = [0.0] * constants.MAX_BEAM_BANKS
    dmg_m = [0.0] * constants.MAX_MISSILE_TUBES
    buff_x = [""] * constants.MAX_SENSOR_CONTACTS
    d_shield = [0.0] * constants.MAX_SHIELD_NAME
    d_system = [0.0] * 15
    d_beam = [0.0] * constants.MAX_BEAM_BANKS
    d_missile = [0.0] * constants.MAX_MISSILE_TUBES
    buff_n = ""
    is_b_active = 0
    is_b_lock = 0
    is_b_load = 0
    is_b_arm = 0
    is_b_arc = 0
    is_b_range = 0

    is_m_active = 0
    is_m_lock = 0
    is_m_load = 0
    is_m_arm = 0
    is_m_arc = 0
    is_m_range = 0

    if (errors.error_on_console(self,obj)):
        return 0
    elif(weapon < 0 or weapon > 2 or mode < 0 or mode > 6):
        return 0
    elif(weapon == 1 and obj.db.beam["exist"] == 0):
        alerts.notify(self,alerts.ansi_red("{:s} has no {:s}s.".format(obj.name,constants.system_name[3])))
        return 0
    elif(weapon == 2 and obj.db.missile["exist"] == 0):
        alerts.notify(self,alerts.ansi_red("{:s} has no {:s}s.".format(obj.name,constants.system_name[9])))
        return 0
    elif (obj.db.beam["exist"] == 0 and obj.db.missile["exist"] == 0):
        alerts.notify(self,alerts.ansi_red("{:s} has no weapons.".format(obj.name)))
        return 0
    elif(obj.db.status["docked"] > 0):
        alerts.notify(self,alerts.ansi_red("{:s} is in dock.".format(obj.name)))
        return 0
    elif(obj.db.status["landed"] > 0):
        alerts.notify(self,alerts.ansi_red("{:s} is on a landing pad.".format(obj.name)))
        return 0
    elif(obj.db.cloak["active"] > 0 and obj.db.tech["cloak"] < 2.0):
        alerts.notify(self,alerts.ansi_red("{:s} cannot fire weapons while cloaked.".format(obj.name)))
        return 0
    
    #check beam weapon list
    if (weapon == 1 or (weapon == 0 and obj.db.beam["exist"] == 1)):
        a = first
        b = last
        if (a < 1 or a > obj.db.beam["banks"]):
            a = 0
            b = obj.db.beam["banks"] - 1
        else:
            a-=1
            b-=1
            if (b >= obj.db.beam["banks"]):
                b = obj.db.beam["banks"] - 1
            if (b < a):
                b = a
        for i in range(obj.db.beam["banks"]):
            dmg_b[i] = 0.0
        for i in range(a,b+1):
            if(obj.db.blist[i]["damage"] <= 0.0):
                continue
            if(obj.db.blist[i]["active"] == 0):
                continue
            is_b_active += 1
            if (obj.db.blist[i]["lock"] == 0):
                continue
            obj_x = search_object(obj.db.blist[i]["lock"])[0]
            if (obj_x.ndb.i0 != obj.name):
                obj_x.ndb.i0 = obj.name                     #initial marker
                obj_x.ndb.i1 = utils.sdb2slist(obj,obj_x.name)   #slist number
                obj_x.ndb.i2 = 0                            #firing arc
                obj_x.ndb.i3 = 0                            #facing shield
                obj_x.ndb.i4 = 0                            #multiple hit flag
                obj_x.ndb.i5 = 0                            #hit flag of target
                obj_x.ndb.d0 = 0.0                          #range to target & shield damage
                obj_x.ndb.d1 = 0.0                          #target shield GW
                obj_x.ndb.d2 = 0.0                          #internal damage
            if (obj_x.ndb.i1 == constants.SENSOR_FAIL):
                continue
            is_b_lock += 1
            if (obj.db.beam["out"] < obj.db.blist[i]["cost"]):
                continue
            is_b_arm += 1
            if (obj_x.ndb.i2 == 0):
                obj_x.ndb.i2 = utils.sdb2arc(obj,obj_x)
            if(utils.arc_check(obj_x.ndb.i2,obj.db.blist[i]["arcs"]) == constants.ARC_FAIL):
                continue
            if(obj.db.status["tractored"] != 0):
                if (obj.db.status["tractored"] != obj_x.name):
                    continue
            is_b_arc +=1
            if(obj_x.ndb.d0 == 0.0):
                obj_x.ndb.d0 = utils.sdb2range(obj,obj_x)
            if(math.fabs(obj.db.move["out"]) < 1.0):
                fire_range = obj.db.blist[i]["range"]
            else:
                fire_range = obj.db.blist[i]["range"] * constants.PARSEC / 10000.0
            if(obj_x.ndb.d0 > fire_range * 10.0):
                continue
            if(math.fabs(obj.db.move["out"]) >= 1.0 and math.fabs(obj_x.db.move["out"]) < 1.0):
                if(obj.db.status["tractoring"] != obj_x.name and obj.db.status["tractored"] != obj_x.name):
                    continue
            if(math.fabs(obj.db.move["out"]) < 1.0 and math.fabs(obj_x.db.move["out"]) >= 1.0):
                if(obj.db.status["tractoring"] != obj_x.name and obj.db.status["tractored"] != obj_x.name):
                    continue
            is_b_range += 1
            if(obj.db.blist[i]["load"] + obj.db.blist[i]["recycle"] > gametime.gametime(absolute=True)):
                continue
            is_b_load += 1
            obj.db.blist[i]["load"] = gametime.gametime(absolute=True)
            obj.db.beam["out"] -= obj.db.blist[i]["cost"]
            prob = obj.db.slist[obj_x.ndb.i1]["lev"]
            prob *= obj.db.blist[i]["damage"] * obj.db.tech["firing"]
            if (obj_x.ndb.d0 > fire_range):
                prob *= 0.01 + 0.99 * fire_range / obj_x.ndb.d0
            prob /= 1.0 + (utils.sdb2angular(obj,obj_x) * 10.0 * (1.0 + obj.db.move["ratio"] / obj_x.db.move["ratio"]))
            if (prob > 1.0):
                prob = 1.0
            elif (prob < 0.01):
                prob = 0.01
            if(obj_x.ndb.i4 != 0):
                buff_x[obj_x.ndb.i1] += " "
            obj_x.ndb.i4 += 1
            if(random.randrange(0,101) < (100 * prob)):
                dmg_b[i] = obj.db.blist[i]["cost"] + obj.db.blist[i]["bonus"]
                if(obj_x.ndb.d0 > fire_range and obj.db.blist[i]["name"] != 19): #mass driver cludge
                    dmg_b[i] *= (1.0 - (obj_x.ndb.d0 - fire_range) / (18.0 * fire_range))
                buff_x[obj_x.ndb.i1] += "B{:d}:|r{:d}|n".format(i+1,int(dmg_b[i] + 0.5))
                if(obj_x.ndb.i5 == 0):
                    obj_x.ndb.i5 += 1
            else:
                buff_x[obj_x.ndb.i1] += "B{:d}:--|n".format(i+1)

    #check missile weapon list
    if (weapon == 2 or (weapon == 0 and obj.db.missile["exist"] == 1)):
        a = first
        b = last
        if (a < 1 or a > obj.db.missile["tubes"]):
            a = 0
            b = obj.db.missile["tubes"] - 1
        else:
            a-=1
            b-=1
            if (b >= obj.db.missile["tubes"]):
                b = obj.db.missile["tubes"] - 1
            if (b < a):
                b = a
        for i in range(obj.db.missile["tubes"]):
            dmg_m[i] = 0.0
        for i in range(a,b+1):
            if(obj.db.mlist[i]["damage"] <= 0.0):
                continue
            if(obj.db.mlist[i]["active"] == 0):
                continue
            is_m_active += 1
            if (obj.db.mlist[i]["lock"] == 0):
                continue
            obj_x = search_object(obj.db.mlist[i]["lock"])[0]
            if (obj_x.ndb.i0 != obj.name):
                obj_x.ndb.i0 = obj.name                     #initial marker
                obj_x.ndb.i1 = utils.sdb2slist(obj,obj_x.name)   #slist number
                obj_x.ndb.i2 = 0                            #firing arc
                obj_x.ndb.i3 = 0                            #facing shield
                obj_x.ndb.i4 = 0                            #multiple hit flag
                obj_x.ndb.i5 = 0                            #hit flag of target
                obj_x.ndb.d0 = 0.0                          #range to target & shield damage
                obj_x.ndb.d1 = 0.0                          #target shield GW
                obj_x.ndb.d2 = 0.0                          #internal damage
            if (obj_x.ndb.i1 == constants.SENSOR_FAIL):
                continue
            is_m_lock += 1
            if (obj.db.missile["out"] < obj.db.mlist[i]["cost"]):
                continue
            is_m_arm += 1
            if (obj_x.ndb.i2 == 0):
                obj_x.ndb.i2 = utils.sdb2arc(obj,obj_x)
            if(utils.arc_check(obj_x.ndb.i2,obj.db.mlist[i]["arcs"]) == constants.ARC_FAIL):
                continue
            if(obj.db.status["tractored"] != 0):
                if (obj.db.status["tractored"] != obj_x.name):
                    continue
            is_m_arc +=1
            if(obj_x.ndb.d0 == 0.0):
                obj_x.ndb.d0 = utils.sdb2range(obj,obj_x)
            if(math.fabs(obj.db.move["out"]) < 1.0):
                fire_range = obj.db.mlist[i]["range"]
            else:
                fire_range = obj.db.mlist[i]["range"] * constants.PARSEC / 10000.0
            if(obj_x.ndb.d0 > fire_range * 10.0):
                continue
            if(math.fabs(obj.db.move["out"]) >= 1.0 and math.fabs(obj_x.db.move["out"]) < 1.0):
                if(obj.db.status["tractoring"] != obj_x.name and obj.db.status["tractored"] != obj_x.name):
                    continue
            if(math.fabs(obj.db.move["out"]) < 1.0 and math.fabs(obj_x.db.move["out"]) >= 1.0):
                if(obj.db.status["tractoring"] != obj_x.name and obj.db.status["tractored"] != obj_x.name):
                    continue
            is_m_range += 1
            if(obj.db.mlist[i]["load"] + obj.db.mlist[i]["recycle"] > gametime.gametime(absolute=True)):
                continue
            is_m_load += 1
            obj.db.mlist[i]["load"] = gametime.gametime(absolute=True)
            obj.db.missile["out"] -= obj.db.mlist[i]["cost"]
            prob = obj.db.slist[obj_x.ndb.i1]["lev"]
            prob *= obj.db.mlist[i]["damage"] * obj.db.tech["firing"]
            if (obj_x.ndb.d0 > fire_range):
                prob *= 0.01 + 0.99 * fire_range / obj_x.ndb.d0
            prob /= 1.0 + (utils.sdb2angular(obj,obj_x) * 10.0 * (1.0 + obj.db.move["ratio"] / obj_x.db.move["ratio"]))
            if (prob > 1.0):
                prob = 1.0
            elif (prob < 0.01):
                prob = 0.01
            if(obj_x.ndb.i4 != 0):
                buff_x[obj_x.ndb.i1] += " "
            obj_x.ndb.i4 += 1
            if(random.randrange(0,101) < (100 * prob)):
                dmg_m[i] = obj.db.mlist[i]["warhead"]
                if(obj_x.ndb.d0 > fire_range and obj.db.mlist[i]["name"] == 3): #mass driver cludge
                    dmg_m[i] *= (1.0 - (obj_x.ndb.d0 - fire_range) / (18.0 * fire_range))
                buff_x[obj_x.ndb.i1] += "M{:d}:|r{:d}|n".format(i+1,int(dmg_m[i] + 0.5))
                if(obj_x.ndb.i5 != 0):
                    obj_x.ndb.i5 += 1
            else:
                buff_x[obj_x.ndb.i1] += "M{:d}:--|n".format(i+1)

    #report weapon status
    if (is_b_load == 0 or is_m_load == 0):
        if (is_b_load == 0 and (weapon == 1 or (weapon == 0 and obj.db.beam["exist"] == 1))):
            if (is_b_active == 0):
                alerts.notify(self,alerts.ansi_red("No {:s}s are online.".format(constants.system_name[3])))
            elif (is_b_lock == 0):
                alerts.notify(self,alerts.ansi_red("No {:s}s are locked.".format(constants.system_name[3])))
            elif (is_b_arm == 0):
                alerts.notify(self,alerts.ansi_red("No {:s}s are armed.".format(constants.system_name[3])))
            elif (is_b_arc == 0):
                alerts.notify(self,alerts.ansi_red("No {:s}s have targets in firing arc.".format(constants.system_name[3])))
            elif (is_b_range == 0):
                alerts.notify(self,alerts.ansi_red("No {:s}s have targets in range.".format(constants.system_name[3])))
            elif (is_b_load == 0):
                alerts.notify(self,alerts.ansi_red("No {:s}s are recycled.".format(constants.system_name[3])))
            for i in range(obj.db.sensor["contacts"]):
                obj_x = search_object(obj.db.slist[i]["key"])
                if (len(obj_x) > 0):
                    obj_x = obj_x[0]
                    if(obj_x.ndb.i0 == obj.name):
                        obj_x.ndb.i0 = 0
                        obj_x.ndb.i1 = 0
                        obj_x.ndb.i2 = 0
                        obj_x.ndb.i3 = 0
                        obj_x.ndb.i4 = 0
                        obj_x.ndb.i5 = 0
                        obj_x.ndb.d0 = 0.0
                        obj_x.ndb.d1 = 0.0
                        obj_x.ndb.d2 = 0.0
            return 0

        if (is_m_load == 0 and (weapon == 2 or (weapon == 0 and obj.db.missile["exist"] == 1))):    
            if (is_m_active == 0):
                alerts.notify(self,alerts.ansi_red("No {:s}s are online.".format(constants.system_name[9])))
            elif (is_m_lock == 0):
                alerts.notify(self,alerts.ansi_red("No {:s}s are locked.".format(constants.system_name[9])))
            elif (is_m_arm == 0):
                alerts.notify(self,alerts.ansi_red("No {:s}s are powered.".format(constants.system_name[9])))
            elif (is_m_arc == 0):
                alerts.notify(self,alerts.ansi_red("No {:s}s have targets in firing arc.".format(constants.system_name[9])))
            elif (is_m_range == 0):
                alerts.notify(self,alerts.ansi_red("No {:s}s have targets in range.".format(constants.system_name[9])))
            elif (is_m_load == 0):
                alerts.notify(self,alerts.ansi_red("No {:s}s are recycled.".format(constants.system_name[9])))
            for i in range(obj.db.sensor["contacts"]):
                obj_x = search_object(obj.db.slist[i]["key"])
                if (len(obj_x) > 0):
                    obj_x = obj_x[0]
                    if(obj_x.ndb.i0 == obj.name):
                        obj_x.ndb.i0 = 0
                        obj_x.ndb.i1 = 0
                        obj_x.ndb.i2 = 0
                        obj_x.ndb.i3 = 0
                        obj_x.ndb.i4 = 0
                        obj_x.ndb.i5 = 0
                        obj_x.ndb.d0 = 0.0
                        obj_x.ndb.d1 = 0.0
                        obj_x.ndb.d2 = 0.0
            return 0

    #report firing messages
    flag = 0
    for i in range(obj.db.sensor["contacts"]):
        obj_x = search_object(obj.db.slist[i]["key"])[0]
        if (obj_x.ndb.i0 == obj.name):
            if (obj_x.ndb.i4 != 0):
                if (flag > 0):
                    buff_n += "\n"
                flag +=1
                buff_n += "Firing at {:s}: {:s}".format(unparse.unparse_identity(obj,obj_x),buff_x[i])
                if (obj_x.ndb.i5 != 0):
                    alerts.do_space_notify_two(obj,obj_x,["helm","tactical","science"],"fires and hits")
                    alerts.write_spacelog(self,obj,"LOG: Fired and hit, Beam {:.6f} GHz, Missile {:.6f} GHz".format(obj.db.beam["freq"],obj.db.missile["freq"]))
                else:
                    alerts.do_space_notify_two(obj,obj_x,["helm","tactical","science"],"fires and misses")
                if(obj_x.db.status["active"] == 1 and obj_x.db.status["crippled"] == 0):
                    alerts.console_message(obj_x,["helm","science","tactical"],"{:s} firing: {:s}".format(unparse.unparse_identity(obj_x,obj),buff_x[i]))
                    obj_x.ndb.i3 = utils.sdb2shield(obj_x,obj)
                    obj_x.ndb.d1 = utils.sdb2dissipation(obj_x,obj_x.ndb.i3)
            obj_x.ndb.d0 = 0.0 #shield damage
            obj_x.ndb.d2 = 0.0 #ship damage
    
    alerts.console_message(obj,["helm","science","tactical"],buff_n)

    #compute damage
    if(weapon == 0 or weapon == 1):
        for i in range(obj.db.beam["banks"]):
            obj_x = search_object(obj.db.blist[i]["lock"])
            if (len(obj_x) == 0):
                continue
            else:
                obj_x = obj_x[0]
                if (obj_x.ndb.i0 == obj.name):
                    if(dmg_b[i] > 0):
                        if(obj_x.db.shield["exist"] != 0):
                            if(obj_x.ndb.d1 > 0.0):
                                if(obj_x.db.shield["freq"] == obj.db.beam["freq"]):
                                    pdmg = dmg_b[i]
                                else:
                                    pdmg = 0.0
                                dmg_b[i] -= pdmg
                                if (dmg_b[i] > 0.0):
                                    obj_x.ndb.d0 += dmg_b[i] / obj_x.ndb.d1 / 10.0
                                dmg_b[i] /= obj_x.ndb.d1
                                dmg_b[i] += pdmg
                        #dmg_b[i] -= obj_x.db.tech["armor"]
                        #dmg_b[i] /= obj_x.db.tech["armor"]
                        if (dmg_b[i] > 0):
                            obj_x.ndb.d2 += dmg_b[i]
        
    if(weapon == 0 or weapon == 2):
        for i in range(obj.db.missile["tubes"]):
            obj_x = search_object(obj.db.mlist[i]["lock"])
            if (len(obj_x) == 0):
                continue
            else:
                obj_x = obj_x[0]
                if (obj_x.ndb.i0 == obj.name):
                    if(dmg_m[i] > 0):
                        if(obj_x.db.shield["exist"] != 0):
                            if(obj_x.ndb.d1 > 0.0):
                                if(obj_x.db.shield["freq"] == obj.db.missile["freq"]):
                                    pdmg = dmg_m[i]
                                else:
                                    pdmg = 0.0
                                dmg_m[i] -= pdmg
                                if (dmg_m[i] > 0.0):
                                    obj_x.ndb.d0 += dmg_m[i] / obj_x.ndb.d1 / 10.0
                                dmg_m[i] /= obj_x.ndb.d1
                                dmg_m[i] += pdmg
                        #dmg_m[i] -= obj_x.db.tech["armor"]
                        #dmg_m[i] /= obj_x.db.tech["armor"]
                        if (dmg_m[i] > 0):
                            obj_x.ndb.d2 += dmg_m[i]

    #assess damage
    for i in range(obj.db.sensor["contacts"]):
        obj_x = search_object(obj.db.slist[i]["key"])[0]
        if (obj_x.ndb.i0 == obj.name):
            d_shield = [0.0] * constants.MAX_SHIELD_NAME
            d_system = [0.0] * 15
            d_beam = [0.0] * constants.MAX_BEAM_BANKS
            d_missile = [0.0] * constants.MAX_MISSILE_TUBES
            obj_x.ndb.d2 -= obj_x.db.tech["armor"]
            obj_x.ndb.d2 /= obj_x.db.tech["armor"]
            if(obj_x.ndb.d0 > 0.0):
                d_shield[obj_x.ndb.i3] += obj_x.ndb.d0
                if(obj_x.ndb.d2 > 0.0):
                    alerts.ship_hurt(obj_x)
                else:
                    alerts.ship_hit(obj_x)
            if(obj_x.ndb.d2 > 0.0):
                if (mode == 0 or mode == 6):
                    d_system[0] += obj_x.ndb.d2
                else:
                    d_system[0] += obj_x.ndb.d2 / 100
                k = int(obj_x.ndb.d2 / 5.0 + 1.0)
                for j in range(k):
                    pdmg = (random.random() * 500) / 100.0
                    rand = random.randrange(0,10) + random.randrange(0,10) + 2
                    if (mode == 0): #normal damage
                        if (rand == 2):
                            d_shield[random.randrange(0,constants.MAX_SHIELD_NAME)] += pdmg
                        elif (rand == 3):
                            d_system[11] += pdmg
                        elif (rand == 4):
                            d_system[7] += pdmg
                        elif (rand == 5):
                            d_system[5] += pdmg
                        elif (rand == 6):
                            d_system[1] += pdmg
                        elif (rand == 7):
                            d_system[8] += pdmg
                        elif (rand == 8):
                            d_missile[random.randrange(0,constants.MAX_MISSILE_TUBES)] += pdmg
                        elif (rand == 14):
                            d_beam[random.randrange(0,constants.MAX_BEAM_BANKS)] += pdmg
                        elif (rand == 15):
                            d_system[14] += pdmg
                        elif (rand == 16):
                            d_system[6] += pdmg
                        elif (rand == 17):
                            d_system[13] += pdmg
                        elif (rand == 18):
                            d_system[12] += pdmg
                        elif (rand == 19):
                            d_system[4] += pdmg
                        elif (rand == 20):
                            d_system[2] += pdmg
                    elif (mode == 2): #engine damage
                        if (rand == 15):
                            d_system[14] += pdmg
                        elif (rand == 16):
                            d_system[6] += pdmg
                    elif (mode == 3): #weapon damage
                        if (rand == 2):
                            d_shield[random.randrange(0,constants.MAX_SHIELD_NAME)] += pdmg
                        elif (rand == 5):
                            d_system[5] += pdmg
                        elif (rand == 8):
                            d_missile[random.randrange(0,constants.MAX_MISSILE_TUBES)] += pdmg
                        elif (rand == 14):
                            d_beam[random.randrange(0,constants.MAX_BEAM_BANKS)] += pdmg
                        elif (rand == 17):
                            d_system[13] += pdmg
                        elif (rand == 18):
                            d_system[12] += pdmg
                        elif (rand == 19):
                            d_system[4] += pdmg
                    elif (mode == 4): #sensor damage
                        if (rand == 3):
                            d_system[11] += pdmg
                        elif (rand == 4):
                            d_system[7] += pdmg
                        elif (rand == 5):
                            d_system[5] += pdmg
                        elif (rand == 19):
                            d_system[4] += pdmg
                    elif(mode == 5): #power damage
                        if (rand == 6):
                            d_system[1] += pdmg
                        elif (rand == 7):
                            d_system[8] += pdmg
                        elif (rand == 20):
                            d_system[2] += pdmg
            if (obj_x.ndb.d0 > 0.0 or obj_x.ndb.d2 > 0.0):
                if (obj_x.db.shield["exist"] != 0):
                    for j in range(constants.MAX_SHIELD_NAME):
                        if (d_shield[j] > 0.0):
                            damage.damage_shield(obj_x,j,d_shield[j])
            if (obj_x.ndb.d2 > 0.0):
                ss = obj_x.db.structure["max_structure"]
                if (d_system[0] > 0.0):
                    pdmg = obj_x.db.structure["superstructure"]
                    damage.damage_structure(obj_x,d_system[0])
                    if (obj_x.db.structure["superstructure"] <= -ss):
                        #killed message here
                        continue
                    if (pdmg > 0.0 and obj_x.db.structure["superstructure"] <= 0.0):
                        for j in range(obj.db.beam["banks"]):
                            if (obj.blist[j]["lock"] == obj_x.name):
                                obj.blist[j]["lock"] = 0
                        for j in range(obj.db.missile["tubes"]):
                            if (obj.mlist[j]["lock"] == obj_x.name):
                                obj.mlist[j]["lock"] = 0
                if (d_system[1] > 0.0 and obj_x.db.aux["exist"] != 0):
                    damage.damage_aux(obj_x,d_system[1])
                    if (obj_x.db.structure["superstructure"] <= -ss):
                        continue
                if (d_system[8] > 0.0 and obj_x.db.main["exist"] != 0):
                    damage.damage_main(obj_x,d_system[8])
                    if (obj_x.db.structure["superstructure"] <= -ss):
                        continue
                if (d_system[2] > 0.0 and obj_x.db.batt["exist"] != 0):
                    damage.damage_batt(obj_x,d_system[2])
                if (obj_x.db.beam["exist"] != 0):
                    for j in range(obj_x.db.beam["banks"]):
                        if (d_beam[j] > 0.0):
                            damage.damage_beam(obj_x,j,d_beam[j])
                if (d_system[4] > 0.0 and obj_x.db.cloak["exist"] != 0):
                    damage.damage_cloak(obj_x,d_system[4])
                if (d_system[5] > 0.0 and obj_x.db.sensor["ew_exist"] != 0):
                    damage.damage_ew(obj_x,d_system[5])
                if (d_system[6] > 0.0 and obj_x.db.engine["impulse_exist"] != 0):
                    damage.damage_impulse(obj_x,d_system[6])
                if (d_system[7] > 0.0 and obj_x.db.sensor["lrs_exist"] != 0):
                    damage.damage_lrs(obj_x,d_system[7])
                if (obj_x.db.missile["exist"] != 0):
                    for j in range(obj_x.db.missile["tubes"]):
                        if (d_missile[j] > 0.0):
                            damage.damage_missile(obj_x,j,d_missile[j])
                if (d_system[11] > 0.0 and obj_x.db.sensor["srs_exist"] != 0):
                    damage.damage_srs(obj_x,d_system[11])
                if (d_system[12] > 0.0 and obj_x.db.tract["exist"] != 0):
                    damage.damage_tract(obj_x,d_system[12])
                if (d_system[13] > 0.0 and obj_x.db.trans["exist"] != 0):
                    damage.damage_trans(obj_x,d_system[13])
                if (d_system[14] > 0.0 and obj_x.db.engine["warp_exist"] != 0):
                    damage.damage_warp(obj_x,d_system[14])
            obj_x.ndb.i0 = 0
            obj_x.ndb.i1 = 0
            obj_x.ndb.i2 = 0
            obj_x.ndb.i3 = 0
            obj_x.ndb.i4 = 0
            obj_x.ndb.i5 = 0
            obj_x.ndb.d0 = 0.0
            obj_x.ndb.d1 = 0.0
            obj_x.ndb.d2 = 0.0    
    return 1    

def do_set_weapon(self,obj,weapon,first, last,active):
    if (errors.error_on_console(self,obj)):
        return 0
    elif(weapon == 1 and obj.db.beam["exist"] != 1):
        alerts.notify(self,alerts.ansi_red("{:s} has no {:s}s.".format(obj.name,constants.system_name[3])))
    elif(weapon == 2 and obj.db.missile["exist"] != 1):
        alerts.notify(self,alerts.ansi_red("{:s} has no {:s}s.".format(obj.name,constants.system_name[9])))
    elif(weapon == 0 and obj.db.missile["exist"] != 1 and obj.db.beam["exist"] != 1):
        alerts.notify(self,alerts.ansi_red("{:s} has no weapons.".format(obj.name)))
    
    buffer = ""
    flag_b = 0
    flag_m = 0
    if(weapon == 1 or (weapon == 0 and obj.db.beam["exist"] == 1)):
        a = first
        b = last
        if (a < 1 or a > obj.db.beam["banks"]):
            a = 0
            b = obj.db.beam["banks"] - 1
        else:
            a -= 1
            b -= 1
            if(b >= obj.db.beam["banks"]):
                b = obj.db.beam["banks"] - 1
            if (b < a):
                b = a
        for i in range(a,b+1):
            if(obj.db.blist[i]["damage"] <= 0.0):
                alerts.notify(self,alerts.ansi_red("{:s} {:d} is inoperative.".format(unparse.unparse_beam(obj.db.blist[i]["name"]),i + 1)))
            elif(active == 1 and obj.db.blist[i]["active"] == 1):
                alerts.notify(self,alerts.ansi_red("{:s} {:d} is already online.".format(unparse.unparse_beam(obj.db.blist[i]["name"]),i + 1)))
            elif(active == 0 and obj.db.blist[i]["active"] == 0):
                alerts.notify(self,alerts.ansi_red("{:s} {:d} is already offline.".format(unparse.unparse_beam(obj.db.blist[i]["name"]),i + 1)))
            elif(active == 1):
                obj.db.blist[i]["lock"] = 0
                obj.db.blist[i]["active"] = 1
                obj.db.beam["in"] += obj.db.blist[i]["cost"] * 10.0
                if(flag_b == 0):
                    buffer += str(constants.system_name[3])
                buffer += " "
                buffer += unparse.unparse_integer(i + 1)
                flag_b += 1
            else:
                obj.db.blist[i]["lock"] = 0
                obj.db.blist[i]["active"] = 0
                obj.db.beam["in"] -= obj.db.blist[i]["cost"] * 10.0
                if(flag_b == 0):
                    buffer += str(constants.system_name[3])
                buffer += " "
                buffer += unparse.unparse_integer(i+1)
                flag_b += 1

    if(weapon == 2 or (weapon == 0 and obj.db.missile["exist"] == 1)):
        a = first
        b = last
        if (a < 1 or a > obj.db.missile["tubes"]):
            a = 0
            b = obj.db.missile["tubes"] - 1
        else:
            a -= 1
            b -= 1
            if(b >= obj.db.missile["tubes"]):
                b = obj.db.missile["tubes"] - 1
            if (b < a):
                b = a
        for i in range(a,b+1):
            if(obj.db.mlist[i]["damage"] <= 0.0):
                alerts.notify(self,alerts.ansi_red("{:s} {:d} is inoperative.".format(unparse.unparse_missile(obj.db.mlist[i]["name"]),i + 1)))
            elif(active == 1 and obj.db.mlist[i]["active"] == 1):
                alerts.notify(self,alerts.ansi_red("{:s} {:d} is already online.".format(unparse.unparse_missile(obj.db.mlist[i]["name"]),i + 1)))
            elif(active == 0 and obj.db.mlist[i]["active"] == 0):
                alerts.notify(self,alerts.ansi_red("{:s} {:d} is already offline.".format(unparse.unparse_missile(obj.db.mlist[i]["name"]),i + 1)))
            elif(active == 1):
                obj.db.mlist[i]["lock"] = 0
                obj.db.mlist[i]["active"] = 1
                obj.db.missile["in"] += obj.db.mlist[i]["cost"] * 10.0
                if(flag_m == 0):
                    buffer += str(constants.system_name[9])
                buffer += " "
                buffer += unparse.unparse_integer(i + 1)
                flag_m += 1
            else:
                obj.db.mlist[i]["lock"] = 0
                obj.db.mlist[i]["active"] = 0
                obj.db.missile["in"] -= obj.db.mlist[i]["cost"] * 10.0
                if(flag_m == 0):
                    buffer += str(constants.system_name[9])
                buffer += " "
                buffer += unparse.unparse_integer(i+1)
                flag_m += 1
    
    if(flag_m > 0 or flag_b > 0):
        if(active == 1):
            alerts.console_message(obj,["tactical"],"{:s} is online".format(buffer))
        else:
            alerts.console_message(obj,["tactical"],"{:s} is offline".format(buffer))
    
    return 1

def do_lock_weapon(self,obj,contact,weapon,first,last):
    flag_b = 0
    flag_m = 0
    flag_lock = 0

    if (errors.error_on_console(self,obj)):
        return 0
    elif(weapon == 1 and obj.db.beam["exist"] != 1):
        alerts.notify(self,alerts.ansi_red("{:s} has no {:s}s.".format(obj.name,constants.system_name[3])))
        return 0
    elif(weapon == 2 and obj.db.missile["exist"] != 1):
        alerts.notify(self,alerts.ansi_red("{:s} has no {:s}s.".format(obj.name,constants.system_name[9])))
        return 0
    elif(weapon == 0 and obj.db.missile["exist"] != 1 and obj.db.beam["exist"] != 1):
        alerts.notify(self,alerts.ansi_red("{:s} has no weapons.".format(obj.name)))
        return 0
    elif(obj.db.status["docked"] != 0):
        alerts.notify(self,alerts.ansi_red("{:s} is in dock.".format(obj.name)))
        return 0
    elif(obj.db.status["landed"] != 0):
        alerts.notify(self,alerts.ansi_red("{:s} is on a landing pad.".format(obj.name)))
        return 0
    elif(obj.db.cloak["active"] != 0 and obj.db.tech["cloak"] < 2.0):
        alerts.notify(self,alerts.ansi_red("{:s} cannot lock weapons while cloaked.".format(obj.name)))
        return 0
    
    obj_x = utils.contact2sdb(obj,contact)
    if(errors.error_on_contact(self,obj,obj_x)):
        return 0
    
    for i in range(obj.db.beam["banks"]):
        if(obj.db.blist[i]["lock"] == obj_x.name):
            flag_lock += 1
    
    for i in range(obj.db.missile["tubes"]):
        if(obj.db.mlist[i]["lock"] == obj_x.name):
            flag_lock += 1
    
    buffer = ""
    if(weapon == 1 or (weapon == 0 and obj.db.beam["exist"] == 1)):
        a = first
        b = last

        if (a < 0 or a > obj.db.beam["banks"]):
            a = 0
            b = obj.db.beam["banks"] - 1
        else:
            a -= 1
            b -= 1
            if (b >= obj.db.beam["banks"]):
                b = obj.db.beam["banks"] - 1
            if (b < a):
                b = a
        for i in range(a,b+1):
            if(obj.db.blist[i]["damage"] <= 0.0):
                alerts.notify(self,alerts.ansi_red("{:s} {:d} is inoperative.".format(unparse.unparse_beam(obj.db.blist[i]["name"]),i + 1)))
            elif(obj.db.blist[i]["active"] == 0):
                alerts.notify(self,alerts.ansi_red("{:s} {:d} is is not online.".format(unparse.unparse_beam(obj.db.blist[i]["name"]),i + 1)))
            elif(obj.db.blist[i]["lock"] > 0):
                alerts.notify(self,alerts.ansi_red("{:s} {:d} is already locked.".format(unparse.unparse_beam(obj.db.blist[i]["name"]),i + 1)))
            else:
                obj.db.blist[i]["lock"] = obj_x.name
                if(flag_b == 0):
                    buffer += str(constants.system_name[3])
                buffer += " "
                buffer += unparse.unparse_integer(i + 1)
                flag_b += 1
    
    if(weapon == 2 or (weapon == 0 and obj.db.missile["exist"] == 1)):
        a = first
        b = last

        if (a < 0 or a > obj.db.missile["tubes"]):
            a = 0
            b = obj.db.missile["tubes"] - 1
        else:
            a -= 1
            b -= 1
            if (b >= obj.db.missile["tubes"]):
                b = obj.db.missile["tubes"] - 1
            if (b < a):
                b = a
        for i in range(a,b+1):
            if(obj.db.mlist[i]["damage"] <= 0.0):
                alerts.notify(self,alerts.ansi_red("{:s} {:d} is inoperative.".format(unparse.unparse_missile(obj.db.mlist[i]["name"]),i + 1)))
            elif(obj.db.mlist[i]["active"] == 0):
                alerts.notify(self,alerts.ansi_red("{:s} {:d} is is not online.".format(unparse.unparse_missile(obj.db.mlist[i]["name"]),i + 1)))
            elif(obj.db.mlist[i]["lock"] != 0):
                alerts.notify(self,alerts.ansi_red("{:s} {:d} is already locked.".format(unparse.unparse_missile(obj.db.mlist[i]["name"]),i + 1)))
            else:
                obj.db.mlist[i]["lock"] = obj_x.name
                if(flag_m == 0):
                    buffer += str(constants.system_name[9])
                buffer += " "
                buffer += unparse.unparse_integer(i + 1)
                flag_m += 1
    
    if (flag_b > 0 or flag_m > 0):
        alerts.console_message(obj,["tactical"],alerts.ansi_cmd(self,"{:s} locked on {:s}".format(buffer,unparse.unparse_identity(obj,obj_x))))
        if(flag_lock == 0):
            obj_y = utils.sdb2contact(obj_x,obj)
            if (obj_y != constants.SENSOR_FAIL):
                alerts.console_message(obj_x,["helm","tactical","science"],alerts.ansi_warn("|^Weapon lock from {:s} detected".format(unparse.unparse_identity(obj_x,obj))))
    return 1

def do_unlock_weapon(self,obj,weapon,first,last):
    flag_b = 0
    flag_m = 0
    
    if (errors.error_on_console(self,obj)):
        return 0
    elif(weapon == 1 and obj.db.beam["exist"] != 1):
        alerts.notify(self,alerts.ansi_red("{:s} has no {:s}s.".format(obj.name,constants.system_name[3])))
        return 0
    elif(weapon == 2 and obj.db.missile["exist"] != 1):
        alerts.notify(self,alerts.ansi_red("{:s} has no {:s}s.".format(obj.name,constants.system_name[9])))
        return 0
    elif(weapon == 0 and obj.db.missile["exist"] != 1 and obj.db.beam["exist"] != 1):
        alerts.notify(self,alerts.ansi_red("{:s} has no weapons.".format(obj.name)))
        return 0
    elif(obj.db.status["docked"] != 0):
        alerts.notify(self,alerts.ansi_red("{:s} is in dock.".format(obj.name)))
        return 0
    elif(obj.db.status["landed"] != 0):
        alerts.notify(self,alerts.ansi_red("{:s} is on a landing pad.".format(obj.name)))
        return 0
    
    buffer = ""
    if(weapon == 1 or (weapon == 0 and obj.db.beam["exist"] == 1)):
        a = first
        b = last

        if (a < 0 or a > obj.db.beam["banks"]):
            a = 0
            b = obj.db.beam["banks"] - 1
        else:
            a -= 1
            b -= 1
            if (b >= obj.db.beam["banks"]):
                b = obj.db.beam["banks"] - 1
            if (b < a):
                b = a
        for i in range(a,b+1):
            if(obj.db.blist[i]["damage"] <= 0.0):
                alerts.notify(self,alerts.ansi_red("{:s} {:d} is inoperative.".format(unparse.unparse_beam(obj.db.blist[i]["name"]),i + 1)))
            elif(obj.db.blist[i]["active"] == 0):
                alerts.notify(self,alerts.ansi_red("{:s} {:d} is is not online.".format(unparse.unparse_beam(obj.db.blist[i]["name"]),i + 1)))
            elif(obj.db.blist[i]["lock"] == 0):
                alerts.notify(self,alerts.ansi_red("{:s} {:d} is already unlocked.".format(unparse.unparse_beam(obj.db.blist[i]["name"]),i + 1)))
            else:
                obj.db.blist[i]["lock"] = 0
                if(flag_b == 0):
                    buffer += str(constants.system_name[3])
                buffer += " "
                buffer += unparse.unparse_integer(i + 1)
                flag_b += 1
    
    if(weapon == 2 or (weapon == 0 and obj.db.missile["exist"] == 1)):
        a = first
        b = last

        if (a < 0 or a > obj.db.missile["tubes"]):
            a = 0
            b = obj.db.missile["tubes"] - 1
        else:
            a -= 1
            b -= 1
            if (b >= obj.db.missile["tubes"]):
                b = obj.db.missile["tubes"] - 1
            if (b < a):
                b = a
        for i in range(a,b+1):
            if(obj.db.mlist[i]["damage"] <= 0.0):
                alerts.notify(self,alerts.ansi_red("{:s} {:d} is inoperative.".format(unparse.unparse_missile(obj.db.mlist[i]["name"]),i + 1)))
            elif(obj.db.mlist[i]["active"] == 0):
                alerts.notify(self,alerts.ansi_red("{:s} {:d} is is not online.".format(unparse.unparse_missile(obj.db.mlist[i]["name"]),i + 1)))
            elif(obj.db.mlist[i]["lock"] == 0):
                alerts.notify(self,alerts.ansi_red("{:s} {:d} is already unlocked.".format(unparse.unparse_missile(obj.db.mlist[i]["name"]),i + 1)))
            else:
                obj.db.mlist[i]["lock"] = 0
                if(flag_m == 0):
                    buffer += str(constants.system_name[9])
                buffer += " "
                buffer += unparse.unparse_integer(i + 1)
                flag_m += 1
    
    if (flag_b > 0 or flag_m > 0):
        alerts.console_message(obj,["tactical"],alerts.ansi_cmd(self,"{:s} unlocked".format(buffer)))
    return 1

def do_set_fix_damage(self,obj,sys1,sys2,type,name):
    dmg = 0
    unit = None
    flag = 0
    sys1 = str(sys1).lower()

    if(obj.db.structure["type"] == 0):
        alerts.notify(self,alerts.ansi_red("Space object not loaded."))
        return 0
    elif(obj.db.status["crippled"] == 2):
        alerts.notify(self,alerts.ansi_red("Space object destroyed."))
        return 0
    elif(obj.db.status["active"] != 1):
        alerts.notify(self,alerts.ansi_red("{:s} systems are inactive".format(obj.name)))
        return 0
    elif(obj.db.structure["max_repair"] <= 0):
        alerts.notify(self,alerts.ansi_red("{:s} has no repair capacity.".format(obj.name)))
        return 0

    if(type != 0):
        obj_x = utils.name2sdb(name)
        if(obj_x == constants.SENSOR_FAIL):
            alerts.notify(self,alerts.ansi_red("That is not a valid repair recipient"))
            return 0
        elif(obj_x.db.location != obj.name):
            alerts.notify(self,alerts.ansi_red("That is not a valid repair recipient"))
            return 0
        elif(obj_x.db.structure["type"] == 0):
            alerts.notify(self,alerts.ansi_red("That is not a valid repair recipient"))
            alerts.write_spacelog(self,obj_x,"BUG:Repair recipient has bad TYPE")
            return 0
        elif(obj_x.db.status["connected"] == 0):
            alerts.notify(self,alerts.ansi_red("{:s} is not connected.".format(obj_x.name)))
            return 0
    else:
        obj_x = obj
    
    if(sys1[0] == "a"):
        if(sys1[1] == "f"):
            if(obj_x.db.shield["exist"] == 1):
                num = 10
                unit = 2
        elif(sys1[1] == "u"):
            if(obj_x.db.aux["exist"] == 1):
                num = 1
        else:
            alerts.notify(self,alerts.ansi_red("Invalid system specification."))
            return 0
    elif(sys1[0] == "b"):
        if(sys1[1] == "a"):
            if(obj_x.db.batt["exist"] == 1):
                num = 2
        if(sys1[1] == "e"):
            if(obj_x.db.beam["exist"] == 1):
                unit = int(sys2)
                if (unit > 0 and unit <= obj_x.db.beam["banks"]):
                    num = 3
        else:
            alerts.notify(self,alerts.ansi_red("Invalid system specification."))
            return 0
    elif(sys1[0] == "c"):
        if(obj_x.db.cloak["exist"] == 1):
            num = 4
    elif(sys1[0] == "d"):
        if(obj_x.db.shield["exist"] == 1):
            num = 10
            unit = 4
    elif(sys1[0] == "e"):
        if(obj_x.db.sensor["ew_exist"] == 1):
            num = 5
    elif(sys1[0] == "f"):
        if(sys1[1] == "o"):
            if(obj_x.db.shield["exist"] == 1):
                num = 10
                unit = 0
        elif(sys1[1] == "u"):
            if(obj_x.db.aux["exist"] == 1):
                num = 1
        else:
            alerts.notify(self,alerts.ansi_red("Invalid system specification."))
            return 0
    elif(sys1[0] == "i"):
        if(obj_x.db.engine["impulse_exist"] == 1):
            num = 6
    elif(sys1[0] == "l"):
        if(obj_x.db.sensor["lrs_exist"] == 1):
            num = 7
    elif(sys1[0] == "m"):
        if(sys1[1] == "a"):
            if(obj_x.db.main["exist"] == 1):
                num = 8
        elif(sys1[1] == "i"):
            if(obj_x.db.missile["exist"] == 1):
                unit = int(sys2)
                if(unit > 0 and unit <= obj_x.db.missile["tubes"]):
                    num = 9
        else:
            alerts.notify(self,alerts.ansi_red("Invalid system specification."))
            return 0
    elif(sys1[0] == "p"):
        if(obj_x.db.shield["exist"] == 1):
            num = 10
            unit = 3
    elif(sys1[0] == "s"):
        if(sys1[1] == "r"):
            if(obj_x.db.sensor["srs_exist"] == 1):
                num = 11 
        elif(sys1[1] == "t"):
            if(obj_x.db.shield["exist"] == 1):
                num = 10
                unit = 1
        elif(sys1[1] == "u"):
            num = 0
        else:
            alerts.notify(self,alerts.ansi_red("Invalid system specification."))
            return 0
    elif(sys1[0] == "t"):
        if(sys1[3] == "c"):
            if(obj_x.db.tract["exist"] == 1):
                num = 12
        elif(sys1[3] == "n"):
            if(obj_x.db.trans["exist"] == 1):
                num = 13
        else:
            alerts.notify(self,alerts.ansi_red("Invalid system specification."))
            return 0
    elif(sys1[0] == "v"):
        if(obj_x.db.shield["exist"] == 1):
            num = 10
            unit = 5
    elif(sys1[0] == "w"):
        if(obj_x.db.engine["warp_exist"] == 1):
            num = 14
    else:
        alerts.notify(self,alerts.ansi_red("Invalid system specification."))
    
    dmg = damage_getter(num,unit)
    if (dmg >= 1.0):
        alerts.notify(self,alerts.ansi_red("{:s} on {:s} has no damage to repair.".format(constants.system_name[num],obj_x.name)))
        dmg = 1.0
        return 0
    elif((dmg <= -1.0) and (obj.db.structure["has_docking_bay"] != 1) and (num > 0)):
        alerts.notify(self,alerts.ansi_red("{:s} on {:s} has been totally destroyed.".format(constants.system_name[num],obj_x.name)))
        return 0
    
    if(num > 0):
        if(num == 1):
            mult = obj_x.db.aux["gw"]
        elif(num == 2):
            mult = obj_x.db.batt["gw"]
        elif(num == 3):
            mult = obj_x.db.blist[unit - 1]["cost"]
        elif(num == 8):
            mult = obj_x.db.main["gw"]
        elif(num == 9):
            mult = obj_x.db.blist[unit - 1]["warhead"]
        else:
            mult = (1.0 + (obj_x.db.structure["max_structure"] / 10.0))

        fix_cost = (1 - dmg) * constants.repair_mult[num] * mult * 100.0
        if(fix_cost > obj.db.structure["repair"]):
            dmg += obj.db.structure["repair"] / constants.repair_mult[num] / mult / 100.0
            damage_setter(obj,num,unit,dmg)
            obj.db.structure["repair"] = 0.0
            alerts.console_message(obj,["damage"],alerts.ansi_cmd(self.name,"{:s} repaired to {:s}".format(constants.system_name[num],unparse.unparse_percent(dmg))))
            if(type != 0):
                alerts.console_message(obj_x,["damage"],alerts.ansi_cmd("{:s} repaired to {:s} by {:s}".format(constants.system_name[num],unparse.unparse_percent(dmg),obj.name)))
        else:
            dmg = 1.0
            obj.db.structure["repair"] -= fix_cost
            damage_setter(obj,num,unit,dmg)
            alerts.console_message(obj,["damage"],alerts.ansi_cmd(self.name,"{:s} repairs complete.".format(constants.system_name[num])))
            if(type != 0):
                alerts.console_message(obj_x,["damage"],alerts.ansi_cmd("{:s} repairs completed by {:s}".format(constants.system_name[num],obj.name)))
        obj_x.db.sensor["version"] = 1
        obj_x.db.engine["version"] = 1
        obj_x.db.power["version"] = 1
        obj_x.db.cloak["version"] = 1
        obj_x.db.status["time"] = obj_x.db.move["time"]
        iterate.up_cochranes(obj_x)
        iterate.up_empire(obj_x)
        iterate.up_quadrant(obj_x)
        iterate.up_vectors(obj_x)
        iterate.up_resolution(obj_x)
        iterate.up_signature(obj_x)
        iterate.up_visibility(obj_x)
        utils.debug_space(obj_x)
        return 1
    else:
        if(obj_x.db.structure["superstructure"] < 0.0):
            flag = 1
        fix_cost = (obj_x.db.structure["max_structure"] - obj_x.db.structure["superstructure"]) * constants.repair_mult[0]
        if(fix_cost > obj.db.structure["repair"]):
            obj_x.db.structure["superstructure"] += obj.db.structure["repair"] / constants.repair_mult[0]
            obj.db.structure["repair"] = 0
            dmg = damage_getter(obj,num,unit)
            alerts.console_message(obj,["damage"],alerts.ansi_cmd(self.name,"{:s} repaired to {:s}".format(constants.system_name[num],unparse.unparse_percent(dmg))))
            if(type != 0):
                alerts.console_message(obj_x,["damage"],alerts.ansi_cmd("{:s} repaired to {:s} by {:s}".format(constants.system_name[num],unparse.unparse_percent(dmg),obj.name)))
        else:
            obj_x.db.structure["superstructure"] = obj_x.b.structure["max_structure"]
            obj.db.structure["repair"] -= fix_cost
            alerts.console_message(obj,["damage"],alerts.ansi_cmd(self.name,"{:s} repairs complete.".format(constants.system_name[num])))
            if(type != 0):
                alerts.console_message(obj_x,["damage"],alerts.ansi_cmd("{:s} repairs completed by {:s}".format(constants.system_name[num],obj.name)))
        if(flag == 1 and obj_x.structure["superstructure"] >= 0.0):
            obj_x.db.status["crippled"] = 0
            alerts.do_ship_notify(obj_x,"{:s} recovers from total systems failure.".format(obj_x.name))
        obj_x.db.sensor["version"] = 1
        obj_x.db.engine["version"] = 1
        obj_x.db.power["version"] = 1
        obj_x.db.cloak["version"] = 1
        obj_x.db.status["time"] = obj_x.db.move["time"]
        iterate.up_cochranes(obj_x)
        iterate.up_empire(obj_x)
        iterate.up_quadrant(obj_x)
        iterate.up_vectors(obj_x)
        iterate.up_resolution(obj_x)
        iterate.up_signature(obj_x)
        iterate.up_visibility(obj_x)
        utils.debug_space(obj_x)
        return 1

def damage_getter(obj,num,unit):
    if(num == 0):
        return (obj.db.structure["superstructure"] / obj.db.structure["max_structure"])
    elif(num == 1):
        return obj.db.aux["damage"]
    elif(num == 2):
        return obj.db.batt["damage"]
    elif(num == 3):
        return obj.db.blist[unit - 1]["damage"]
    elif(num == 4):
        return obj.db.cloak["damage"]
    elif(num == 5):
        return obj.db.sensor["ew_damage"]
    elif(num == 6):
        return obj.db.engine["impulse_damage"]
    elif(num == 7):
        return obj.db.sensor["lrs_damage"]
    elif(num == 8):
        return obj.db.main["damage"]
    elif(num == 9):
        return obj.db.mlist[unit - 1]["damage"]
    elif (num == 10):
        return obj.db.shield[unit]["damage"]
    elif (num == 11):
        return obj.db.sensor["srs_damage"]
    elif(num == 12):
        return obj.db.tract["damage"]
    elif(num == 13):
        return obj.db.trans["damage"]
    elif(num == 14):
        return obj.db.engine["warp_engine"]
    else:
        raise ValueError("Bad value in damage_getter")

def damage_setter(obj,num,unit,value):
    if(num == 0):
        obj.db.structure["superstructure"] = value
    elif(num == 1):
        obj.db.aux["damage"] = value
    elif(num == 2):
        obj.db.batt["damage"] = value
    elif(num == 3):
        obj.db.blist[unit - 1]["damage"] = value
    elif(num == 4):
        obj.db.cloak["damage"] = value
    elif(num == 5):
        obj.db.sensor["ew_damage"] = value
    elif(num == 6):
        obj.db.engine["impulse_damage"] = value
    elif(num == 7):
        obj.db.sensor["lrs_damage"] = value
    elif(num == 8):
        obj.db.main["damage"] = value
    elif(num == 9):
        obj.db.mlist[unit - 1]["damage"] = value
    elif (num == 10):
        obj.db.shield[unit]["damage"] = value
    elif (num == 11):
        obj.db.sensor["srs_damage"] = value
    elif(num == 12):
        obj.db.tract["damage"] = value
    elif(num == 13):
        obj.db.trans["damage"] = value
    elif(num == 14):
        obj.db.engine["warp_engine"] = value
    else:
        raise ValueError("Bad value in damage_setter")