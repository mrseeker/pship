from unicodedata import category
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

    Usage: exit/override [name]
    
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

        if (obj.location is not None or len(self.args) == 1):
            if (len(self.args[0]) != 0):
                ship_airlock = utils.name2sdb(self.args[0])
                if (ship_airlock == constants.SENSOR_FAIL):
                    alerts.notify(caller,alerts.ansi_red("That is not a valid contact"))
                    return 0
                elif(ship_airlock not in obj.contents):
                    alerts.notify(caller,alerts.ansi_red("That is not a valid contact"))
                    return 0
                elif(ship_airlock.tags.get(category="space_object") is None):
                    alerts.notify(caller,alerts.ansi_red("That is not a valid contact"))
            else:
                ship_airlock = obj.location
            airlock = search_tag("airlock",category=ship_airlock.name)
            if(len(airlock) > 0):
                airlock = airlock[0]
                if (ship_airlock.db.status["connected"] == 1 or ship_airlock.db.status["landed"] == 1 or ship_airlock.db.status["docked"] == 1):
                    if caller.move_to(airlock):
                        alerts.do_console_notify(obj,["security"],alerts.ansi_warn("{:s} left the ship through the airlock.".format(caller.db._sdesc)))
                        alerts.do_console_notify(ship_airlock,["security"],alerts.ansi_warn("{:s} entered the ship through the airlock.".format(caller.db._sdesc)))
                    else:
                        alerts.notify(caller,alerts.ansi_red("The airlock opens, but you stare at a sealed door."))
                elif(ship_airlock.db.status["connected"] == 0):
                    if("override" in self.switches):
                        alerts.notify(caller,alerts.ansi_red("The airlock opens, but you stare at a sealed door."))
                    else:
                        alerts.notify(caller,alerts.ansi_red("The airlock refuses to open."))
                else:
                    alerts.notify(caller,alerts.ansi_red("The airlock refuses to open."))
            else:
                alerts.notify(caller,alerts.ansi_red("{:s} does not have an airlock.".format(ship_airlock.name)))
        elif("override" in self.switches):
            space = create_object(Corpse,key=caller.name)
            space.db.coords["x"] = obj.db.coords["x"]
            space.db.coords["y"] = obj.db.coords["y"]
            space.db.coords["z"] = obj.db.coords["z"]
            space.db.move["v"] = obj.db.move["v"]
            space.db.course["d"][0][0] = obj.db.course["d"][0][0]
            space.db.course["d"][0][1] = obj.db.course["d"][0][1]
            space.db.course["d"][0][2] = obj.db.course["d"][0][2]
            space.db.ship = space.name
            space.tags.add("corpse",category=caller.name)
            space.cmdset.add("commands.science.ScienceCmdSet",persistent=True)
            caller.move_to(space)
            alerts.do_console_notify(obj,["security"],alerts.ansi_alert("{:s} left the ship through the airlock.".format(caller.sdesc)))
            alerts.write_spacelog(caller,obj,"LOG: exit through the airlock in space: {:s}".format(space.dbref))
        else:
            alerts.notify(caller,alerts.ansi_red("The airlock refuses to open."))

class Corpse(space_room):
    def at_object_creation(self):
        super().at_object_creation()
        self.tags.remove(constants.type_name[0],category="space_object")
#        self.tags.add(constants.type_name[9],category="airlock")
        self.db.sdesc = "Space"
        self.db.desc = "You are now a corpse happily floating in space"
        self.db.type = constants.type_name[9]
        self.db.status["active"] = 1
        self.db.structure["type"] = 9
        self.db.sensor["srs_exist"] = 1
        self.db.sensor["srs_active"] = 1
        self.db.sensor["srs_resolution"] = 0.01

class Airlock(Room):
    def at_object_creation(self):
        super().at_object_creation()
        self.tags.add("general",category="airlock")
        self.db.type=constants.CONSOLE_ATTR_NAME
        self.db.sdesc = "Airlock"
        self.db.ship=""
#        self.cmdset.add("typeclasses.airlock.AirlockCmdSet", persistent=True)
