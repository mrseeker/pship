"""
Handles all tactical-related commands
"""

from evennia import default_cmds
from commands import science
from world import constants, set as setter
from world import alerts, errors ,unparse
from evennia import CmdSet
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
            self.add(CmdEnable())
            self.add(CmdDisable())
            self.add(CmdTarget())
            self.add(CmdUnlock())
            self.add(science.CmdIdent())

class CmdAlloc(default_cmds.MuxCommand):
    """
    Commands related to the allocation of the tactical systems.

    Usage: alloc <command> <value>
    
    Command list:
    status - Gives a full status of the allocations
    BMS - Sets the allocation of the Beams, Missiles and Sensors
    sensors - Allocation of the sensors (ECM and ECCM)

    """

    key = "alloc"
    help_category = "Tactical"
    
    def func(self):
        self.args = self.args.split(" ")
        caller = self.caller
        obj_x = search_object(self.caller.location)[0]
        obj = search_object(obj_x.db.ship)[0]
        if(errors.error_on_console(self.caller,obj)):
                return 0
        if (self.args[0] == "BMS" and len(self.args) == 4):
            setter.do_set_tactical_alloc(self.caller,obj,float(self.args[1]),float(self.args[2]),float(self.args[3]))
        elif (self.args[0] == "sensors" and len(self.args) == 3):
            setter.do_set_sensor_alloc(self.caller,obj,float(self.args[1]),float(self.args[2]))
        elif (self.args[0] == "status"):
            #Give a full report back
            buffer = "|y|[bTactical Allocation Report|n\n"
            table = evtable.EvTable("|cAllocation|n","|cEPS Power|n","|cPercentage|n","")
            table.add_row("|cTotal Tactical|n",unparse.unparse_power(obj.db.alloc["tactical"]*obj.db.power["total"]),unparse.unparse_percent(obj.db.alloc["tactical"]))
            table.add_row("|cBeams|n",unparse.unparse_power(obj.db.alloc["beams"]*obj.db.power["total"]),unparse.unparse_percent(obj.db.alloc["beams"]),alerts.ansi_rainbow_scale(obj.db.alloc["beams"],35))
            table.add_row("|cMissiles|n",unparse.unparse_power(obj.db.alloc["missiles"]*obj.db.power["total"]),unparse.unparse_percent(obj.db.alloc["missiles"]),alerts.ansi_rainbow_scale(obj.db.alloc["missiles"],35))
            table.add_row("|cSensors|n",unparse.unparse_power(obj.db.alloc["sensors"]*obj.db.power["total"]),unparse.unparse_percent(obj.db.alloc["sensors"]),alerts.ansi_rainbow_scale(obj.db.alloc["sensors"],35))
            alerts.notify(self.caller,buffer + str(table) + "\n")
        else:    
            self.caller.msg("Command not found: " + str(self.args))


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

class CmdEnable(default_cmds.MuxCommand):
    """
    Commands related to the enabling of the weapons.

    Usage: enable <weapon> <first> <last>

    Command list:
    weapon - Type of weapon (0 = all, 1 = beam, 2 = missiles)
    first - First beam/missile
    last - Last beam/missile
    """

    key="enable"
    aliases=["select"]

    def func(self):
        self.args = self.args.split(" ")
        caller = self.caller
        obj_x = search_object(self.caller.location)[0]
        obj = search_object(obj_x.db.ship)[0]

        if(errors.error_on_console(self.caller,obj)):
            return 0
    
        if(len(self.args) == 3):
            setter.do_set_weapon(self,obj,int(self.args[0]),int(self.args[1]),int(self.args[2]),1)
        else:
            alerts.notify(self,alerts.ansi_red("Wrong command entered."))

class CmdDisable(default_cmds.MuxCommand):
    """
    Commands related to the disabling of the weapons.

    Usage: disable <weapon> <first> <last>

    Command list:
    weapon - Type of weapon (0 = all, 1 = beam, 2 = missiles)
    first - First beam/missile
    last - Last beam/missile
    """

    key="disable"
    aliases=["unselect"]

    def func(self):
        self.args = self.args.split(" ")
        caller = self.caller
        obj_x = search_object(self.caller.location)[0]
        obj = search_object(obj_x.db.ship)[0]

        if(errors.error_on_console(self.caller,obj)):
            return 0
    
        if(len(self.args) == 3):
            setter.do_set_weapon(self,obj,int(self.args[0]),int(self.args[1]),int(self.args[2]),0)
        else:
            alerts.notify(self,alerts.ansi_red("Wrong command entered."))

class CmdTarget(default_cmds.MuxCommand):
    """
    Commands related to the targeting system.

    Usage: target <target> <weapon> <first> <last>

    Command list:
    target - ID of the target
    weapon - Type of weapon (0 = all, 1 = beam, 2 = missiles)
    first - First beam/missile
    last - Last beam/missile
    """

    key="target"
    aliases = ["lock","lock on"]

    def func(self):
        self.args = self.args.split(" ")
        caller = self.caller
        obj_x = search_object(self.caller.location)[0]
        obj = search_object(obj_x.db.ship)[0]

        if(errors.error_on_console(self.caller,obj)):
            return 0
    
        if(len(self.args) == 4):
            setter.do_lock_weapon(self,obj,int(self.args[0]),int(self.args[1]),int(self.args[2]),int(self.args[3]))
        else:
            alerts.notify(self,alerts.ansi_red("Wrong command entered."))

class CmdUnlock(default_cmds.MuxCommand):
    """
    Commands related to the targeting system.

    Usage: unlock <weapon> <first> <last>

    Command list:
    weapon - Type of weapon (0 = all, 1 = beam, 2 = missiles)
    first - First beam/missile
    last - Last beam/missile
    """

    key="unlock"
    aliases = []

    def func(self):
        self.args = self.args.split(" ")
        caller = self.caller
        obj_x = search_object(self.caller.location)[0]
        obj = search_object(obj_x.db.ship)[0]

        if(errors.error_on_console(self.caller,obj)):
            return 0
    
        if(len(self.args) == 3):
            setter.do_unlock_weapon(self,obj,int(self.args[0]),int(self.args[1]),int(self.args[2]))
        else:
            alerts.notify(self,alerts.ansi_red("Wrong command entered."))


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
    aliases=["shoot"]

    def func(self):
        self.args = self.args.split(" ")
        caller = self.caller
        obj_x = search_object(self.caller.location)[0]
        obj = search_object(obj_x.db.ship)[0]

        if(errors.error_on_console(self.caller,obj)):
            return 0
        
        if(self.args[0] == ""):
            setter.do_set_fire(caller,obj,0,constants.MAX_BEAM_BANKS,0,0)
        elif(len(self.args) == 4):
            setter.do_set_fire(caller,obj,int(self.args[1]),int(self.args[2]),int(self.args[0]),int(self.args[3]))
        else:
            alerts.notify(self,alerts.ansi_red("Wrong command entered."))

