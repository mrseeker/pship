from evennia.utils.create import create_object
from typeclasses.rooms import Room, space_room
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

    Usage: exit/override
    
    Switches:
    Override - Exits the airlock, even if it means you end up in space.

    Command list:
    None
    """

    key = "exit"
    help_category = "Airlock"
    switch_options = ("override",)

    def func(self):
        self.args = self.args.strip()
        self.args = self.args.split(" ")
        caller = self.caller
        obj_x = search_object(caller.location)[0]
        obj = search_object(obj_x.db.ship)[0]

        if (obj.db.location != 0):
            ship_airlock = utils.name2sdb(obj.db.location)
            airlock = search_tag("airlock",category=ship_airlock.name)
            if(len(airlock) > 0):
                airlock = airlock[0]
                if (obj.db.status["connected"] == 1 or obj.db.status["landed"] == 1 or obj.db.status["docked"] == 1):
                    if caller.move_to(airlock):
                        alerts.do_console_notify(obj,["security"],"Someone left the ship through the airlock.")
                        alerts.do_console_notify(ship_airlock,["security"],"Someone entered the ship through the airlock.")
                    else:
                        alerts.notify(caller,"The airlock opens, but you stare at a sealed door.")
                else:
                    alerts.notify(caller,alerts.ansi_red("The airlock refuses to open."))
            else:
                alerts.notify(caller,alerts.ansi_red("{:s} does not have an airlock.".format(ship_airlock.name)))
        elif("override" in self.switches):
            space = create_object(space_room,key="space-" + caller.name)
            space.db.sdesc = "Space"
            space.db.desc = "You are a corpse happily floating in space"
            space.db.coords["x"] = obj.db.coords["x"]
            space.db.coords["y"] = obj.db.coords["y"]
            space.db.coords["z"] = obj.db.coords["z"]
            space.db.move["v"] = obj.db.move["v"]
            space.db.course["d"][0][0] = obj.db.course["d"][0][0]
            space.db.course["d"][0][1] = obj.db.course["d"][0][1]
            space.db.course["d"][0][2] = obj.db.course["d"][0][2]
            space.db.type = constants.type_name[9]
            space.db.status["active"] = 1
            space.db.structure["type"] = 9
            space.tags.add("corpse",category=caller.name)
            space.cmdset.add("commands.science.ScienceCmdSet",persistent=True)
            caller.move_to(space)
            alerts.do_console_notify(obj,["security"],alerts.ansi_alert("Someone left the ship through the airlock."))
            alerts.log_msg("{:s} exited through the airlock.".format(caller.name))
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

