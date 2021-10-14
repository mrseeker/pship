"""
Handles all bridge-related commands
"""

from evennia import default_cmds
from world import set as setter
from world import alerts, errors,unparse, utils,constants
from evennia import CmdSet
from evennia.utils.search import search_object
from evennia.utils import evtable

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
        if (self.args[0] == "green"):
            alerts.do_ship_notify(obj,"\033[5m|X|[gALERT: Green alert|n")
        elif (self.args[0] == "yellow"):
            alerts.do_ship_notify(obj,"\033[5m|X|[yALERT: Yellow alert|n")
        elif (self.args[0] == "red"):
            alerts.do_ship_notify(obj,"\033[5m|X|[rALERT: Red alert|n")
        elif (self.args[0] == "blue"):
            alerts.do_ship_notify(obj,"\033[5m|c|[bALERT: Blue alert|n")
        elif (self.args[0] == "black"):
            alerts.do_ship_notify(obj,"\033[5m|w|[XALERT: Black alert|n")
        else:    
            self.caller.msg("Alert not found: " + str(self.args))

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
        self.args = self.args.split(" ")
        caller = self.caller
        obj_x = search_object(self.caller.location)[0]
        obj = search_object(obj_x.db.ship)[0]
        if(errors.error_on_console(self.caller,obj)):
            return 0
        alerts.do_ship_notify(obj,alerts.ansi_cmd_ext(caller.name,caller.location,' '.join(self.args)))