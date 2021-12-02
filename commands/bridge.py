"""
Handles all bridge-related commands
"""

from evennia import default_cmds
from world import alerts, errors
from evennia import CmdSet
from evennia.utils.search import search_object

class BridgeCmdSet(CmdSet):
        
        key = "BridgeCmdSet"
        def at_cmdset_creation(self):
            self.add(CmdAlerts())
            self.add(CmdBroadcast())

class BridgeFighterCmdSet(CmdSet):
        key = "BridgeFighterCmdSet"
        
        def at_cmdset_creation(self):
            self.add(CmdAlerts())
            self.add(CmdBroadcast())

class CmdAlerts(default_cmds.MuxCommand):
    """
    Sets the alert status

    Usage: alert <green/yellow/red/blue/black>
    
    Command list:
    Does not have any commands
    """

    key = "alert"
    help_category = "Bridge"

    def func(self):
        self.args = self.args.strip()
        self.args = self.args.split(" ")
        caller = self.caller
        obj_x = search_object(self.caller.location)[0]
        obj = search_object(obj_x.db.ship)[0]
        if(errors.error_on_console(self.caller,obj)):
            return 0
        if (self.args[0][0] == "g"):
            alerts.do_ship_notify(obj,"\033[5m|X|[gALERT: Green alert|n")
        elif (self.args[0][0] == "y"):
            alerts.do_ship_notify(obj,"\033[5m|X|[yALERT: Yellow alert|n")
        elif (self.args[0][0] == "r"):
            alerts.do_ship_notify(obj,"\033[5m|X|[rALERT: Red alert|n")
        elif (self.args[0][0] == "b" and self.args[0][2] == "u"):
            alerts.do_ship_notify(obj,"\033[5m|c|[bALERT: Blue alert|n")
        elif (self.args[0][0] == "b" and self.args[0][2] == "a"):
            alerts.do_ship_notify(obj,"\033[5m|w|[XALERT: Black alert|n")
        else:    
            alerts.notify(caller,alerts.ansi_red("Alert not found: {:s}".format(' '.join(self.args))))

class CmdBroadcast(default_cmds.MuxCommand):
    """
    Broadcasts to all stations

    Usage: broadcast <message>
    
    Command list:
    Does not have any commands
    """

    key = "broadcast"
    help_category = "Bridge"

    def func(self):
        self.args = self.args.strip()
        caller = self.caller
        obj_x = search_object(self.caller.location)[0]
        obj = search_object(obj_x.db.ship)[0]
        if(errors.error_on_console(caller,obj)):
            return 0
        alerts.do_ship_notify(obj,alerts.ansi_cmd(caller.name,self.args))