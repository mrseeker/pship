"""
Handles all science-related commands
"""

from evennia import default_cmds
from world import set as setter
from world import alerts, errors, status,constants
from evennia import CmdSet, utils
from evennia.utils.search import search_object
from evennia.utils import evtable

class ScienceCmdSet(CmdSet):
        
        key = "ScienceCmdSet"
    
        def at_cmdset_creation(self):
            self.add(CmdIdent())
            self.add(CmdEmpire())
            self.add(CmdSensorReport())


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
        else:
            status.sensor_report(self,self.args)

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

class CmdSensorReport(default_cmds.MuxCommand):
    """
    Gives a full report of all sensor contacts

    Usage: report <Command>
    
    Command list:
    <Contact ID>: Gives the full report of a contact ID
    <Type>: Gives back the status of a particular type(eg: ship, base, planet...)
    """

    key = "report"
    alias = "report"
    help_category = "Science"
    
    def func(self):
        self.args = self.args.strip()
        caller = self.caller
        obj_x = search_object(self.caller.location)[0]
        obj = search_object(obj_x.db.ship)[0]
            
        if not self.args:
            status.do_sensor_contacts(self,constants.SENSOR_FAIL)
        else:
            status.do_sensor_contacts(self,self.args)
