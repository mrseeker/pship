"""
Creates a wormhole with all it's functionalities.
"""

from typeclasses.rooms import space_room
from world import constants

class Wormhole(space_room):
    """
    This creates a default wormhole without any consoles
    """

    def at_object_creation(self):
        super().at_object_creation()
        self.db.desc = "This is the wormhole center of " + self.key
        self.db.type = constants.type_name[4]
        self.tags.add(constants.type_name[4],category="space_object")
        self.tags.remove(constants.type_name[0],category="space_object")
        self.db.sdesc = "Wormhole"
        self.db.structure["type"] = 4
        self.db.ship = self.key

class Generic_Wormhole(Wormhole):
    def at_object_creation(self):
        super().at_object_creation()
        self.db.engine = {"version":0,"warp_damage":0.0,"warp_max":0,"warp_exist":0,"impulse_damage":0.0,"impulse_max":0,"impulse_exist":0,"warp_cruise":0.0,"impulse_cruise":0.0}
        self.db.movement = {"time":1,"dt":1,"in":0.0,"out":0.0,"ratio":10000000.0,"cochranes":1000.0,"v":0.0,"empire":0,"quadrant":0}
        self.db.tech = {"firing":1.0,"fuel":1.0,"stealth":1.0,"cloak":1.0,"sensors":1.0,"aux_max":1.0,"main_max":1.0,"armor":1.0,"ly_range":1.0}
        self.db.sensor = {"version":0,"lrs_damage":0.0,"lrs_active":0,"lrs_exist":0,"lrs_resolution":0.0,"lrs_signature":0.0,"srs_damage":0.0,"srs_active":0,"srs_exist":0,"srs_resolution":0.0,"srs_signature":0.0,"ew_damage":0.0,"ew_active":0,"ew_exist":0,"visibility":0.0,"contacts":0,"counter":0}
        self.db.tract = {"cost":0,"freq":0.0,"exist":0,"active":0,"damage":0.0,"lock":0}
        self.db.trans = {"cost":0,"freq":0.0,"exist":0,"active":0,"damage":0.0,"d_lock":0,"s_lock":0}
        self.db.shield = {"ratio":3.0,"maximum":18,"freq":1.0,"exist":0,0:{"active":0,"damage":1.0},1:{"active":0,"damage":1.0},2:{"active":0,"damage":1.0},3:{"active":0,"damage":1.0},4:{"active":0,"damage":1.0},5:{"active":0,"damage":1.0}}
        self.db.main["exist"] = 0
        self.db.aux["exist"] = 0
        self.db.batt["exist"] = 0
