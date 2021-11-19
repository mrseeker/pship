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
            self.add(CmdEW())
            self.add(CmdFire())
            self.add(CmdEnable())
            self.add(CmdDisable())
            self.add(CmdTarget())
            self.add(CmdUnlock())
            self.add(science.CmdIdent())
            self.add(CmdFreq())

class CmdAlloc(default_cmds.MuxCommand):
    """
    Commands related to the allocation of the tactical systems.

    Usage: alloc <command> <value>
    
    Command list:
    status - Gives a full status of the allocations
    BMS - Sets the allocation of the Beams, Missiles and Sensors
    sensor - Allocation of the sensors (ECM and ECCM)

    """

    key = "alloc"
    help_category = "Tactical"
    
    def func(self):
        self.args = self.args.split(" ")
        caller = self.caller
        obj_x = search_object(self.caller.location)[0]
        obj = search_object(obj_x.db.ship)[0]
        if(errors.error_on_console(caller,obj)):
                return 0
        if (self.args[0] == "BMS" and len(self.args) == 4):
            setter.do_set_tactical_alloc(caller,obj,float(self.args[1]),float(self.args[2]),float(self.args[3]))
        elif (self.args[0] == "sensor" and len(self.args) == 3):
            setter.do_set_sensor_alloc(caller,obj,float(self.args[1]),float(self.args[2]))
        elif (self.args[0] == "status"):
            #Give a full report back
            buffer = "|y|[bTactical Allocation Report|n\n"
            table = evtable.EvTable("|cAllocation|n","|cEPS Power|n","|cPercentage|n","")
            table.add_row("|cTotal Tactical|n",unparse.unparse_power(obj.db.alloc["tactical"]*obj.db.power["total"]),unparse.unparse_percent(obj.db.alloc["tactical"]))
            table.add_row("|cBeams|n",unparse.unparse_power(obj.db.alloc["beams"]*obj.db.power["total"]),unparse.unparse_percent(obj.db.alloc["beams"]),alerts.ansi_rainbow_scale(obj.db.alloc["beams"],35))
            table.add_row("|cMissiles|n",unparse.unparse_power(obj.db.alloc["missiles"]*obj.db.power["total"]),unparse.unparse_percent(obj.db.alloc["missiles"]),alerts.ansi_rainbow_scale(obj.db.alloc["missiles"],35))
            table.add_row("|cSensors|n",unparse.unparse_power(obj.db.alloc["sensors"]*obj.db.power["total"]),unparse.unparse_percent(obj.db.alloc["sensors"]),alerts.ansi_rainbow_scale(obj.db.alloc["sensors"],35))
            alerts.notify(caller,buffer + str(table) + "\n")
        else:    
            alerts.notify(caller,"Wrong command entered.")


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
            
        if(errors.error_on_console(caller,obj)):
            return 0
        elif(not obj.db.cloak["exist"]):
            alerts.notify(self.caller,alerts.ansi_red("{:s} has no cloaking device.".format(obj.name)))
            return 0
        elif(obj.db.cloak["damage"] <= 0.0):
            alerts.notify(self.caller,alerts.ansi_red("Cloaking device is inoperative."))
            return 0
        
        if not self.args:
            alerts.notify(caller,"You did not enter any commands.")    
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
            alerts.notify(caller,buffer)
        elif(self.args == "on"):
            alerts.notify(caller,"Turning on cloak...")
            setter.do_set_cloak(obj,1,obj)
        elif(self.args == "off"):
            alerts.notify(caller,"Turning off cloak...")
            setter.do_set_cloak(obj,0,obj)

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
        obj_x = search_object(caller.location)[0]
        obj = search_object(obj_x.db.ship)[0]
            
        if not self.args:
            alerts.notify(alerts.ansi_red("You did not enter any commands."))
        elif(errors.error_on_console(caller,obj)):
                return 0
        elif(not obj.db.sensor["ew_exist"]):
            alerts.notify(caller,alerts.ansi_red("{:s} has no Electronic Warfare systems.".format(obj.name)))
            return 0
        elif(obj.db.sensor["ew_damage"] <= 0.0):
            alerts.notify(caller,alerts.ansi_red("Electronic Warfare systems are inoperative."))
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
            alerts.notify(caller,buffer)
        elif(self.args == "on"):
            alerts.notify(caller,"Turning on Electronic Warfare systems...")
            setter.do_set_ew(obj,1,obj)
        elif(self.args == "off"):
            alerts.notify(caller,"Turning off Electronic Warfare systems...")
            setter.do_set_ew(obj,0,obj)

class CmdFreq(default_cmds.MuxCommand):
    """
    Commands related to the setting of frequencies.

    Usage: freq <device> <freq>

    Command list:
    device - Type of device (beam or missile)
    first - Frequency in Ghz (1.000 to 999.999)
    """

    key="freq"
    help_category = "Tactical"

    def func(self):
        self.args = self.args.split(" ")
        caller = self.caller
        obj_x = search_object(self.caller.location)[0]
        obj = search_object(obj_x.db.ship)[0]

        if(errors.error_on_console(self.caller,obj)):
            return 0
    
        if(len(self.args) == 2):
            if self.args[0][0] == "b":
                setter.do_set_beam_freq(caller,obj,float(self.args[1]))
            elif self.args[0][0] == "m":
                setter.do_set_missile_freq(caller,obj,float(self.args[1]))
            else:
                alerts.notify(caller,alerts.ansi_red("Wrong device: {.s}".format(self.args[0])))    
        else:
            alerts.notify(caller,alerts.ansi_red("Wrong command entered."))


class CmdEnable(default_cmds.MuxCommand):
    """
    Commands related to the enabling of the weapons.

    Usage: enable <weapon> <first> <last>

    Command list:
    weapon - Type of weapon (all,beam,missile)
    first - First bank/tube
    last - Last bank/tube
    """

    key="enable"
    help_category = "Tactical"
    aliases=["select"]

    def func(self):
        self.args = self.args.split(" ")
        caller = self.caller
        obj_x = search_object(self.caller.location)[0]
        obj = search_object(obj_x.db.ship)[0]

        if(errors.error_on_console(self.caller,obj)):
            return 0
    
        if(len(self.args) == 3):
            weapon = 0
            if self.args[0][0] == "b":
                weapon = 1
            if self.args[0][0] == "m":
                weapon = 2
            setter.do_set_weapon(caller,obj,weapon,int(self.args[1]) - 1,int(self.args[2]) - 1,1)
        else:
            alerts.notify(caller,alerts.ansi_red("Wrong command entered."))

class CmdDisable(default_cmds.MuxCommand):
    """
    Commands related to the disabling of the weapons.

    Usage: disable <weapon> <first> <last>

    Command list:
    weapon - Type of weapon (all,beam,missile)
    first - First bank/tube
    last - Last bank/tube
    """

    key="disable"
    help_category = "Tactical"
    aliases=["unselect"]

    def func(self):
        self.args = self.args.split(" ")
        caller = self.caller
        obj_x = search_object(self.caller.location)[0]
        obj = search_object(obj_x.db.ship)[0]

        if(errors.error_on_console(caller,obj)):
            return 0
    
        if(len(self.args) == 3):
            weapon = 0
            if self.args[0][0] == "b":
                weapon = 1
            if self.args[0][0] == "m":
                weapon = 2
            setter.do_set_weapon(caller,obj,weapon,int(self.args[1]) - 1,int(self.args[2]) - 1,0)
        else:
            alerts.notify(caller,alerts.ansi_red("Wrong command entered."))

class CmdTarget(default_cmds.MuxCommand):
    """
    Commands related to the targeting system.

    Usage: target <target> <weapon> <first> <last>

    Command list:
    target - ID of the target
    weapon - Type of weapon (all,beam,missiles)
    first - First bank/tube
    last - Last bank/tube
    """

    key="target"
    help_category = "Tactical"
    aliases = ["lock","lock on"]

    def func(self):
        self.args = self.args.split(" ")
        caller = self.caller
        obj_x = search_object(self.caller.location)[0]
        obj = search_object(obj_x.db.ship)[0]

        if(errors.error_on_console(caller,obj)):
            return 0
    
        if(len(self.args) == 4):
            weapon = 0
            if self.args[1][0] == "b":
                weapon = 1
            if self.args[1][0] == "m":
                weapon = 2
            setter.do_lock_weapon(caller,obj,int(self.args[0]),weapon,int(self.args[2])-1,int(self.args[3])-1)
        else:
            alerts.notify(caller,alerts.ansi_red("Wrong command entered."))

class CmdUnlock(default_cmds.MuxCommand):
    """
    Commands related to the targeting system.

    Usage: unlock <weapon> <first> <last>

    Command list:
    weapon - Type of weapon (all,beam,missiles)
    first - First bank/tube
    last - Last bank/tube
    """

    key="unlock"
    help_category = "Tactical"
    aliases = []

    def func(self):
        self.args = self.args.split(" ")
        caller = self.caller
        obj_x = search_object(self.caller.location)[0]
        obj = search_object(obj_x.db.ship)[0]

        if(errors.error_on_console(caller,obj)):
            return 0
    
        if(len(self.args) == 3):
            weapon = 0
            if self.args[0][0] == "b":
                weapon = 1
            if self.args[0][0] == "m":
                weapon = 2
            setter.do_unlock_weapon(caller,obj,weapon,int(self.args[1]) -1 ,int(self.args[2])- 1)
        else:
            alerts.notify(caller,alerts.ansi_red("Wrong command entered."))


class CmdFire(default_cmds.MuxCommand):
    """
    Commands related to the Firing of the weapons.

    Usage: fire <weapon> <location> <first> <last>
    
    Command list:
    weapon - Type of weapon (all,beam,missiles)
    first - First bank/tube
    last - Last bank/tube
    location - Target location (all,hull,engine,weapons,sensors,power)
    """

    key="fire"
    help_category = "Tactical"
    aliases=["shoot"]

    def func(self):
        self.args = self.args.split(" ")
        caller = self.caller
        obj_x = search_object(self.caller.location)[0]
        obj = search_object(obj_x.db.ship)[0]

        if(errors.error_on_console(self.caller,obj)):
            return 0
        
        if(self.args[0] == ""):
            setter.do_set_fire(caller,obj,-1,-1,0,0)
        elif(len(self.args) == 4):
            weapon = 0
            if self.args[0][0] == "b":
                weapon = 1
            elif self.args[0][0] == "m":
                weapon = 2
            mode = 0
            if self.args[1][0] == "h":
                weapon = 1
            elif self.args[1][0] == "e":
                weapon = 2
            elif self.args[1][0] == "w":
                weapon = 3
            elif self.args[1][0] == "s":
                weapon = 4
            elif self.args[1][0] == "p":
                weapon = 5
            setter.do_set_fire(caller,obj,int(self.args[2])-1,int(self.args[3])-1,weapon,mode)
        else:
            alerts.notify(caller,alerts.ansi_red("Wrong command entered."))

