"""
Creates a spacebase with all it's functionalities.

"""

from typeclasses.airlock import Airlock
from typeclasses.rooms import Room,space_room
from typeclasses.exits import Exit
from evennia import create_object
from world import constants

class SpaceBase(space_room):
    """
    This creates a default spacebase without any consoles
    """

    def at_object_creation(self):
        super().at_object_creation()
        self.db.desc = "This is the bridge of " + self.key
        self.db.type = constants.SHIP_ATTR_NAME
        self.tags.add(constants.SHIP_ATTR_NAME,category="space_object")
        self.tags.remove(constants.type_name[0],category="space_object")
        self.db.sdesc = "Bridge"
        self.db.structure["type"] = 2
        self.db.engineering = {"start_sequence":0,"override":self.key}
        self.db.ship = self.key

class Generic_SpaceBase(SpaceBase):
    def at_object_creation(self):
        super().at_object_creation()
        self.db.engine = {"version":0,"warp_damage":0.0,"warp_max":0,"warp_exist":0,"impulse_damage":1.0,"impulse_max":0,"impulse_exist":1,"warp_cruise":0.0,"impulse_cruise":0.0}
        self.db.tech = {"firing":1.0,"fuel":1.0,"stealth":1.0,"cloak":1.0,"sensors":2.0,"aux_max":1.05,"main_max":1.05,"armor":1.0,"ly_range":1.0}
        self.db.sensor = {"version":0,"lrs_damage":1.0,"lrs_active":1,"lrs_exist":1,"lrs_resolution":1.0,"lrs_signature":1.0,"srs_damage":1.0,"srs_active":1,"srs_exist":1,"srs_resolution":1.0,"srs_signature":1.0,"ew_damage":1.0,"ew_active":1,"ew_exist":1,"visibility":1.0,"contacts":1,"counter":1}
        self.db.tract = {"cost":1,"freq":1.0,"exist":1,"active":0,"damage":1.0,"lock":0}
        self.db.trans = {"cost":1,"freq":1.0,"exist":1,"active":0,"damage":1.0,"d_lock":0,"s_lock":0}
        self.db.shield = {"ratio":3.0,"maximum":18,"freq":1.0,"exist":1,0:{"active":0,"damage":1.0},1:{"active":0,"damage":1.0},2:{"active":0,"damage":1.0},3:{"active":0,"damage":1.0},4:{"active":0,"damage":1.0},5:{"active":0,"damage":1.0}}
        self.db.main["exist"] = 1
        self.db.aux["exist"] = 1
        self.db.batt["exist"] = 1

class Console(Room):
    def at_object_creation(self):
        super().at_object_creation()
        self.tags.add("general",category="console")
        self.db.type=constants.CONSOLE_ATTR_NAME
        self.db.sdesc = "Console"
        self.db.ship=""