"""
Handles all operations-related commands
"""

from evennia import default_cmds, CmdSet
from evennia.utils.search import search_object
from world import errors, set as setter

class OperationCmdSet(CmdSet):
        
        key = "OperationCmdSet"
    
        def at_cmdset_creation(self):
            self.add(CmdReFuel())
            self.add(CmdDeFuel())

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
        if receiver is not None:
            receiver = receiver[0]
        if(errors.error_on_console(self.caller,obj)):
                return 0
        if(len(self.args) == 3):
            setter.do_set_refuel(self,obj,receiver,self.args[1],int(self.args[2]))
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
        if receiver is not None:
            receiver = receiver[0]
        elif (obj == receiver):
            #transferring it to itself...
            receiver = None
        if(errors.error_on_console(self.caller,obj)):
                return 0
        if(len(self.args) == 2):
            setter.do_set_refuel(self,obj,None,self.args[0],int(self.args[1]))
        if(len(self.args) == 3):
            setter.do_set_refuel(self,obj,receiver,self.args[1],int(self.args[2]))
        else:
            self.caller.msg("Command not found: " + str(self.args))
