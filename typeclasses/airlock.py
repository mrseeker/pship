from typeclasses.rooms import Room
from evennia import CmdSet
from evennia.utils.search import search_object,search_tag
from evennia import default_cmds

from world import alerts, constants,utils

class AirlockCmdSet(CmdSet):
        
        key = "AirlockCmdSet"
        def at_cmdset_creation(self):
            self.add(CmdExit())

class CmdExit(default_cmds.MuxCommand):
    """
    Exits the airlock

    Usage: exit
    
    Command list:
    None
    """

    key = "exit"
    help_category = "Airlock"

    def func(self):
        self.args = self.args.strip()
        self.args = self.args.split(" ")
        caller = self.caller
        obj_x = search_object(caller.location)[0]
        obj = search_object(obj_x.db.ship)[0]

        if (obj.db.location != 0):
            ship_airlock = utils.name2sdb(obj.db.location)
            airlock = search_tag("airlock",category=ship_airlock.name)
            if(len(airlock > 0)):
                airlock = airlock[0]
                if caller.move_to(airlock) and (obj.db.status["connected"] == 1):
                    alerts.do_console_notify(obj,["security"],"{:s} left the ship through the airlock.".format(caller.name))
                    alerts.do_console_notify(ship_airlock,["security"],"Someone entered the ship through the airlock.")
                else:
                    alerts.notify(caller,"The airlock opens, but you stare at a sealed door.")
            else:
                alerts.notify(caller,alerts.ansi_red("{:s} does not have an airlock.".format(ship_airlock.name)))
        else:
            alerts.notify(caller,alerts.ansi_red("The airlock refuses to open."))

class Airlock(Room):
    def at_object_creation(self):
        super().at_object_creation()
        self.tags.add("general",category="airlock")
        self.db.type=constants.CONSOLE_ATTR_NAME
        self.db.sdesc = "Airlock"
        self.db.ship=""
        self.cmdset.add("typeclasses.airlock.AirlockCmdSet", persistent=True)
    
    def get_display_name(self,looker, **kwargs):
       idstr = "(#%s)" % self.id if self.access(looker, access_type="control") else ""
       return "%s%s" % (self.db.sdesc, idstr)

