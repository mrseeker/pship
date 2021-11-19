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
            self.add(CmdSrs())
            self.add(CmdLrs())
            self.add(CmdEmpire())
            self.add(CmdSensorReport())

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
            alerts.notify(caller,"You did not enter any commands.")
        elif(errors.error_on_console(self.caller,obj)):
            return 0
        elif(not obj.db.sensor["srs_exist"]):
            alerts.notify(caller,alerts.ansi_red("{:s} has no Short-range sensors.".format(obj.name)))
            return 0
        elif(obj.db.sensor["srs_damage"] <= 0.0):
            alerts.notify(caller,alerts.ansi_red("Short-range sensors are inoperative."))
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
            alerts.notify(caller,buffer)
        elif(self.args == "on"):
            alerts.notify(caller,"Turning on Short-range sensors...")
            setter.do_set_srs(obj,1,obj)
        elif(self.args == "off"):
            if (obj.db.structure["type"] == 0):
                alerts.notify(caller, alerts.ansi_red("Space object not loaded."))
            elif (obj.db.status["crippled"] == 2):
                alerts.notify(caller, alerts.ansi_red("Space object destroyed."))
            else:
                alerts.notify(caller,"Turning off Short-range sensors...")
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
        elif(errors.error_on_console(caller,obj)):
            return 0  
        elif(not obj.db.sensor["lrs_exist"]):
            alerts.notify(caller,alerts.ansi_red("{:s} has no Long-range sensors.".format(obj.name)))
            return 0
        elif(obj.db.sensor["lrs_damage"] <= 0.0):
            alerts.notify(caller,alerts.ansi_red("Long-range sensors are inoperative."))
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
            alerts.notify(caller,buffer)
        elif(self.args == "on"):
            alerts.notify(caller,"Turning on Long-range sensors...")
            setter.do_set_lrs(obj,1,obj)
        elif(self.args == "off"):
            alerts.notify(caller,"Turning off Long-range sensors...")
            setter.do_set_lrs(obj,0,obj)

class CmdIdent(default_cmds.MuxCommand):
    """
    Identifies and classifies a sensor contact

    Usage: ident(ify) <contact ID>
    
    Command list:
    None
    """

    key = "identify"
    aliases = ["ident"]
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

class CmdSensorReport(default_cmds.MuxCommand):
    """
    Gives a full report of all sensor contacts

    Usage: report <Command>
    
    Command list:
    <Contact ID>: Gives the full report of a contact ID
    <Type>: Gives back the status of a particular type(eg: ship, base, planet...)
    """

    key = "report"
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
