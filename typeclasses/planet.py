"""
Creates a planet with all it's functionalities.

"""

from typeclasses.airlock import Airlock
from typeclasses.rooms import Room,space_room
from typeclasses.exits import Exit
from evennia import create_object
from world import constants

class Planet(space_room):
    """
    This creates a default planet without any consoles
    """

    def at_object_creation(self):
        super().at_object_creation()
        self.db.desc = "This is the surface of the planet called " + self.key
        self.db.type = constants.LOCATION_ATTR_NAME
        self.tags.add(constants.LOCATION_ATTR_NAME,category="space_object")
        self.tags.remove(constants.type_name[0],category="space_object")
        self.db.sdesc = "Planet Surface"
        self.db.structure["type"] = 3
        self.db.ship = self.key

class Generic_Planet(Planet):
    def at_object_creation(self):
        super().at_object_creation()
        self.db.engine = {"version":0,"warp_damage":0.0,"warp_max":0,"warp_exist":0,"impulse_damage":0.0,"impulse_max":0,"impulse_exist":0,"warp_cruise":0.0,"impulse_cruise":0.0}
        self.db.sensor = {"version":0,"lrs_damage":0.0,"lrs_active":0,"lrs_exist":0,"lrs_resolution":0.0,"lrs_signature":0.0,"srs_damage":0.0,"srs_active":0,"srs_exist":0,"srs_resolution":0.0,"srs_signature":0.0,"ew_damage":0.0,"ew_active":0,"ew_exist":0,"visibility":0.0,"contacts":0,"counter":0}
        self.db.movement = {"time":1,"dt":1,"in":0.0,"out":0.0,"ratio":10000000.0,"cochranes":1278.0,"v":0.0,"empire":0,"quadrant":0}
        self.db.structure = {"type":3,"displacement":10000000000000.0,"cargo_hold":10000000000000.0,"cargo_mass":0.0,"superstructure":1000000000.0,"max_structure":1000000000,"has_landing_pad":1,"has_docking_bay":0,"can_land":0,"can_dock":0,"repair":1000.0,"max_repair":1000}
        self.db.technology = {"firing":1.0,"fuel":1.0,"stealth":1.0,"cloak":1.0,"sensors":1.0,"aux_max":1.05,"main_max":1.05,"armor":1.0,"ly_range":1.0}
        self.db.tract = {"cost":1,"freq":1.0,"exist":0,"active":0,"damage":0.0,"lock":0}
        self.db.trans = {"cost":1,"freq":1.0,"exist":0,"active":0,"damage":0.0,"d_lock":0,"s_lock":0}
        

class Console(Room):
    def at_object_creation(self):
        super().at_object_creation()
        self.tags.add("general",category="console")
        self.db.type=constants.CONSOLE_ATTR_NAME
        self.db.sdesc = "Console"
        self.db.ship=""
    