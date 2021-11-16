"""
Handles all tactical-related commands
"""

from evennia import default_cmds
from commands import science
from world import constants, set as setter
from world import alerts, errors, status
from evennia import CmdSet, utils
from evennia.utils.search import search_object
from evennia.utils import evtable

class TacticalCmdSet(CmdSet):
        
        key = "TacticalCmdSet"
    
        def at_cmdset_creation(self):
            self.add(CmdCloak())
            self.add(CmdSrs())
            self.add(CmdLrs())
            self.add(CmdEW())
            self.add(CmdFire())
            self.add(science.CmdIdent())

class CmdCloak(default_cmds.MuxCommand):
    """
    Commands related to cloaking and uncloaking the ship.

    Usage: cloak <command>
    
    Command list:
    status - Gives the current status of the cloaking device
    on - Turns the cloaking device on
    off - Turns the cloaking device off
    freq - Changes the cloaking frequency

    """

    key = "cloak"
    help_category = "Tactical"
    
    def func(self):
        self.args = self.args.strip()
        caller = self.caller
        obj_x = search_object(self.caller.location)[0]
        obj = search_object(obj_x.db.ship)[0]
            
        if(errors.error_on_console(self.caller,obj)):
            return 0
        elif(not obj.db.cloak["exist"]):
            alerts.notify(self.caller,alerts.ansi_red(obj.name + " has no cloaking device."))
            return 0
        elif(obj.db.cloak["damage"] <= 0.0):
            alerts.notify(self.caller,alerts.ansi_red("Cloaking device is inoperative."))
            return 0
        
        if not self.args:
            self.caller.msg("You did not enter any commands.")    
        elif(self.args == "status"):
            buffer = "Cloaking status:\n"
            buffer += "Active: "
            if(obj.db.cloak["active"]):
                buffer += alerts.ansi_green("YES\n")
            else:
                buffer += alerts.ansi_red("NO\n")
            buffer += "Power: "
            if(obj.db.alloc["cloak"] * obj.db.power["total"] < obj.db.cloak["cost"]):
                buffer += alerts.ansi_red("Insufficient\n")
            else:
                buffer += alerts.ansi_green("OK\n")
            buffer += "Cost: " + str(obj.db.cloak["cost"])
            self.caller.msg(buffer)
        elif(self.args == "on"):
            self.caller.msg("Turning on cloak...")
            setter.do_set_cloak(obj,1,obj)
        elif(self.args == "off"):
            self.caller.msg("Turning off cloak...")
            setter.do_set_cloak(obj,0,obj)

class CmdSrs(default_cmds.MuxCommand):
    """
    Commands related to the short range scanners.

    Usage: srs <command>
    
    Command list:
    status - Gives the current status of the SRS
    on - Turns the SRS on
    off - Turns the SRS off

    """

    key = "srs"
    help_category = "Science"
    
    def func(self):
        self.args = self.args.strip()
        caller = self.caller
        obj_x = search_object(self.caller.location)[0]
        obj = search_object(obj_x.db.ship)[0]
            
        if not self.args:
            self.caller.msg("You did not enter any commands.")
        elif(errors.error_on_console(self.caller,obj)):
            return 0
        elif(not obj.db.sensor["srs_exist"]):
            alerts.notify(self.caller,alerts.ansi_red(obj.name + " has no Short-range sensors."))
            return 0
        elif(obj.db.sensor["srs_damage"] <= 0.0):
            alerts.notify(self.caller,alerts.ansi_red("Short-range sensors are inoperative."))
            return 0
            
        elif(self.args == "status"):
    
            buffer = "SRS status:\n"
            buffer += "Active: "
            if(obj.db.sensor["srs_active"]):
                buffer += alerts.ansi_green("YES\n")
            else:
                buffer += alerts.ansi_red("NO\n")
            buffer += "Power: "
            if(obj.db.alloc["sensors"] * obj.db.power["total"] > 0):
                buffer += alerts.ansi_red("Insufficient\n")
            else:
                buffer += alerts.ansi_green("OK\n")
            buffer += "SRS signature: " + str(obj.db.sensor["srs_signature"]) + "\n"
            buffer += "SRS resolution: " + str(obj.db.sensor["srs_resolution"])
            self.caller.msg(buffer)
        elif(self.args == "on"):
            self.caller.msg("Turning on Short-range sensors...")
            setter.do_set_srs(obj,1,obj)
        elif(self.args == "off"):
            if (obj.db.structure["type"] == 0):
                alerts.notify(self.caller, alerts.ansi_red("Space object not loaded."))
            elif (obj.db.status["crippled"] == 2):
                alerts.notify(self.caller, alerts.ansi_red("Space object destroyed."))
            else:
                self.caller.msg("Turning off Short-range sensors...")
                setter.do_set_srs(obj,0,obj)

class CmdLrs(default_cmds.MuxCommand):
    """
    Commands related to the Long-range scanners.

    Usage: lrs <command>
    
    Command list:
    status - Gives the current status of the LRS
    on - Turns the LRS on
    off - Turns the LRS off

    """

    key = "lrs"
    help_category = "Science"
    
    def func(self):
        self.args = self.args.strip()
        caller = self.caller
        obj_x = search_object(self.caller.location)[0]
        obj = search_object(obj_x.db.ship)[0]
            
        if not self.args:
            self.caller.msg("You did not enter any commands.")
        elif(errors.error_on_console(self.caller,obj)):
            return 0  
        elif(not obj.db.sensor["lrs_exist"]):
            alerts.notify(self.caller,alerts.ansi_red(obj.name + " has no Long-range sensors."))
            return 0
        elif(obj.db.sensor["lrs_damage"] <= 0.0):
            alerts.notify(self.caller,alerts.ansi_red("Long-range sensors are inoperative."))
            return 0
    
        elif(self.args == "status"):
            buffer = "LRS status:\n"
            buffer += "Active: "
            if(obj.db.sensor["lrs_active"]):
                buffer += alerts.ansi_green("YES\n")
            else:
                buffer += alerts.ansi_red("NO\n")
            buffer += "Power: "
            if(obj.db.alloc["sensors"] * obj.db.power["total"] > 0):
                buffer += alerts.ansi_red("Insufficient\n")
            else:
                buffer += alerts.ansi_green("OK\n")
            buffer += "LRS signature: " + str(obj.db.sensor["lrs_signature"]) + "\n"
            buffer += "LRS resolution: " + str(obj.db.sensor["lrs_resolution"])
            self.caller.msg(buffer)
        elif(self.args == "on"):
            self.caller.msg("Turning on Long-range sensors...")
            setter.do_set_lrs(obj,1,obj)
        elif(self.args == "off"):
            self.caller.msg("Turning off Long-range sensors...")
            setter.do_set_lrs(obj,0,obj)

class CmdEW(default_cmds.MuxCommand):
    """
    Commands related to the Electronic Warfare.

    Usage: ew <command>
    
    Command list:
    status - Gives the current status of the EW
    on - Turns the EW on
    off - Turns the EW off

    """

    key = "ew"
    help_category = "Tactical"
    
    def func(self):
        self.args = self.args.strip()
        caller = self.caller
        obj_x = search_object(self.caller.location)[0]
        obj = search_object(obj_x.db.ship)[0]
            
        if not self.args:
            self.caller.msg("You did not enter any commands.")
        elif(errors.error_on_console(self.caller,obj)):
                return 0
        elif(not obj.db.sensor["ew_exist"]):
            alerts.notify(self.caller,alerts.ansi_red(obj.name + " has no Electronic Warfare systems."))
            return 0
        elif(obj.db.sensor["ew_damage"] <= 0.0):
            alerts.notify(self.caller,alerts.ansi_red("Electronic Warfare systems are inoperative."))
            return 0
        
        elif(self.args == "status"):
            buffer = "EW status:\n"
            buffer += "Active: "
            if(obj.db.sensor["ew_active"]):
                buffer += alerts.ansi_green("YES\n")
            else:
                buffer += alerts.ansi_red("NO\n")
            buffer += "Power: "
            if(obj.db.alloc["sensors"] * obj.db.power["total"] > 0):
                buffer += alerts.ansi_red("Insufficient\n")
            else:
                buffer += alerts.ansi_green("OK\n")
            self.caller.msg(buffer)
        elif(self.args == "on"):
            self.caller.msg("Turning on Electronic Warfare systems...")
            setter.do_set_ew(obj,1,obj)
        elif(self.args == "off"):
            self.caller.msg("Turning off Electronic Warfare systems...")
            setter.do_set_ew(obj,0,obj)

class CmdFire(default_cmds.MuxCommand):
    """
    Commands related to the Firing of the weapons.

    Usage: fire <weapon> <first> <last> <location>
    
    Command list:
    weapon - Type of weapon (0 = all, 1 = beam, 2 = missiles)
    first - First beam/missile
    last - Last beam/missile
    location - Target location (0 = all, 1 = hull, 2 = engine, 3 = weapons, 4 = sensors, 5 = power)
    """

    key="fire"
    alises=["shoot"]

    def func(self):
        self.args = self.args.split(" ")
        caller = self.caller
        obj_x = search_object(self.caller.location)[0]
        obj = search_object(obj_x.db.ship)[0]

        if(errors.error_on_console(self.caller,obj)):
            return 0
        
        if(len(self.args) == 0):
            setter.do_set_fire(caller,obj,0,constants.MAX_BEAM_BANKS,0,0)
        elif(len(self.args) == 4):
            setter.do_set_fire(caller,obj,int(self.args[1]),int(self.args[2]),int(self.args[0]),int(self.args[3]))
        else:
            alerts.notify(self,alerts.ansi_red("Wrong command entered."))