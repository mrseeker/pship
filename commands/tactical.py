"""
Handles all engine-related commands
"""

from evennia import default_cmds
from world import set as setter
from world import alerts, errors
from evennia import CmdSet, utils
from evennia.utils.search import search_object
from evennia.utils import evtable

class TacticalCmdSet(CmdSet):
        
        key = "TacticalCmdSet"
    
        def at_cmdset_creation(self):
            self.add(CmdCloak())

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
            
        if not self.args:
            self.caller.msg("You did not enter any commands.")
        elif(self.args == "status"):
            if(errors.error_on_console(self.caller,obj)):
                return 0
            elif(not obj.db.cloak["exist"]):
                alerts.notify(self.caller,alerts.ansi_red(obj.name + " has no cloaking device."))
            elif(obj.db.cloak["damage"] <= 0.0):
                alerts.notify(self.caller,alerts.ansi_red("Cloaking device is inoperative."))
            else:
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
            if (obj.db.structure["type"] == 0):
                alerts.notify(self.caller, alerts.ansi_red("Space object not loaded."))
            elif (obj.db.status["crippled"] == 2):
                alerts.notify(self.caller, alerts.ansi_red("Space object destroyed."))
            else:
                self.caller.msg("Turning on cloak...")
                setter.do_set_cloak(obj,1,obj)
        elif(self.args == "off"):
            if (obj.db.structure["type"] == 0):
                alerts.notify(self.caller, alerts.ansi_red("Space object not loaded."))
            elif (obj.db.status["crippled"] == 2):
                alerts.notify(self.caller, alerts.ansi_red("Space object destroyed."))
            else:
                self.caller.msg("Turning off cloak...")
                setter.do_set_cloak(obj,0,obj)
        