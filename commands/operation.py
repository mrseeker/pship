"""
Handles all operations-related commands
"""

from evennia import default_cmds, CmdSet
from evennia.utils.search import search_object
from world import alerts, errors, set as setter

class OperationCmdSet(CmdSet):
        
        key = "OperationCmdSet"
    
        def at_cmdset_creation(self):
            self.add(CmdReFuel())
            self.add(CmdDeFuel())
            self.add(CmdFreq())

class CmdReFuel(default_cmds.MuxCommand):
    """
    Commands related to the fueling of a spaceship.

    Usage: refuel <shipname> <type> <value>
    
    Command list:
    None
    """

    key = "refuel"
    aliases = ["fuel"]
    help_category = "Operation"
    
    def func(self):
        self.args = self.args.split(" ")
        caller = self.caller
        obj_x = search_object(self.caller.location)[0]
        obj = search_object(obj_x.db.ship)[0]
        receiver = search_object(self.args[0])
        if len(receiver) > 0:
            receiver = receiver[0]
        else:
            receiver = None
        if(errors.error_on_console(caller,obj)):
                return 0
        if(len(self.args) == 3):
            setter.do_set_refuel(caller,obj,receiver,self.args[1],int(self.args[2]))
        else:
            self.caller.msg("Command not found: " + str(self.args))

class CmdDeFuel(default_cmds.MuxCommand):
    """
    Commands related to the dumping of fuel from a spaceship.

    Usage: defuel [shipname] <type> <value>
    
    Command list:
    None
    """

    key = "defuel"
    aliases = ["dump"]
    help_category = "Operation"
    
    def func(self):
        self.args = self.args.split(" ")
        caller = self.caller
        obj_x = search_object(self.caller.location)[0]
        obj = search_object(obj_x.db.ship)[0]
        receiver = search_object(self.args[0])
        if len(receiver) > 0:
            receiver = receiver[0]
        elif (obj == receiver):
            #transferring it to itself...
            receiver = None
        else:
            receiver = None
        if(errors.error_on_console(caller,obj)):
                return 0
        if(len(self.args) == 2):
            setter.do_set_defuel(caller,obj,None,self.args[0],int(self.args[1]))
        elif(len(self.args) == 3):
            setter.do_set_defuel(caller,obj,receiver,self.args[1],int(self.args[2]))
        else:
            self.caller.msg("Command not found: " + str(self.args))

class CmdFreq(default_cmds.MuxCommand):
    """
    Commands related to the setting of frequencies.

    Usage: freq <device> <freq>

    Command list:
    device - Type of device (tract or trans)
    first - Frequency in Ghz (1.000 to 999.999)
    """

    key="freq"
    help_category = "Operation"

    def func(self):
        self.args = self.args.split(" ")
        caller = self.caller
        obj_x = search_object(self.caller.location)[0]
        obj = search_object(obj_x.db.ship)[0]

        if(errors.error_on_console(self.caller,obj)):
            return 0
    
        if(len(self.args) == 2):
            if self.args[0][0] == "tract":
                setter.do_set_tract_freq(self,obj,float(self.args[1]))
            elif self.args[0][0] == "trans":
                setter.do_set_trans_freq(self,obj,float(self.args[1]))
            else:
                alerts.notify(self,alerts.ansi_red("Wrong device: {.s}".format(self.args[0])))    
        else:
            alerts.notify(self,alerts.ansi_red("Wrong command entered."))
