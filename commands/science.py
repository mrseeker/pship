"""
Handles all science-related commands
"""

from evennia import default_cmds
from world import set as setter
from world import alerts, errors, status
from evennia import CmdSet, utils
from evennia.utils.search import search_object
from evennia.utils import evtable

class ScienceCmdSet(CmdSet):
        
        key = "ScienceCmdSet"
    
        def at_cmdset_creation(self):
            self.add(CmdIdent())
            self.add(CmdEmpire())


class CmdIdent(default_cmds.MuxCommand):
    """
    Identifies and classifies a sensor contact

    Usage: ident(ify) <contact ID>
    
    Command list:
    None
    """

    key = "identify"
    alias = "ident"
    help_category = "Science"
    
    def func(self):
        self.args = self.args.strip()
        caller = self.caller
        obj_x = search_object(self.caller.location)[0]
        obj = search_object(obj_x.db.ship)[0]
            
        if not self.args:
            self.caller.msg("You did not enter any contacts")
        elif(len(self.args) == 1):
            status.sensor_report(self,int(self.args[0]))
        else:
            self.caller.msg("Wrong amount of arguments")

class CmdEmpire(default_cmds.MuxCommand):
    """
    Identifies and classifies all sensor contacts from beacons

    Usage: empire
    
    Command list:
    None
    """

    key = "empire"
    
    help_category = "Science"
    
    def func(self):
        self.args = self.args.strip()
        caller = self.caller
        obj_x = search_object(self.caller.location)[0]
        obj = search_object(obj_x.db.ship)[0]
            
        if not self.args:
            status.do_border_report(self)
        else:
            self.caller.msg("Wrong amount of arguments")
