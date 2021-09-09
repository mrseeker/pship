"""
Creates a spaceship with all it's functionalities.

"""

from typeclasses.rooms import Room
from evennia import create_object
from world import constants

class Ship(Room):
    """
    This creates a simple spaceship
    """

    def at_object_creation(self):
        self.db.desc = "This is the bridge"
        self.db.type = constants.SDB_ATTR_NAME
        self.db.coords = {"x":0,"y":0,"z":0, "speed":0}
        self.db.move = {"in":0.0,"out":0.0,"v":0.0,"ratio":0,"time":0}
        self.db.course = {"d":[[0,0,0],[0,0,0],[0,0,0]]}
        self.db.iff = {"frequency":0}
        self.db.shield = {0:[{"active":0,"damage":100.0}],"ratio":0,"visibility":0,"maximum":0}
        self.db.alloc = {"version":0,"shield":[0.0],"shields":0.0,"beams":0.0,"missiles":0.0,"sensors":0.0,"transporters":0.0,"tractors":0.0,"miscellaneous":0.0,"ecm":0.0,"eccm":0.0,"movement":0.0,"cloak":0.0}
        self.db.power = {"total":0.0,"aux":0.0,"batt":0.0}
        self.db.sensor = {"version":1,"ew_damage":0,"ew_active":0,"lrs_active":0,"srs_active":0}
        self.db.tech = {"sensors":0,"ly_range":0}
        self.db.engine = {"version":1,"impulse_damage":0.0,"warp_damage":0.0,"warp_max":0.0,"impulse_max":0.0}
        self.db.cloak = {"version":1,"active":0}
        self.db.trans = {"active":0,"d_lock":0,"s_lock":0}
        self.db.tract = {"active":0,"lock":0}
        self.db.main = {"gw":0}
        self.db.aux = {"gw":0}
        self.db.batt = {"in":0,"out":0,"gw":0}
        self.db.structure = {"superstructure":0.0,"type":constants.SHIP_ATTR_NAME,"displacement":0}
        self.db.status = {"tractored":None,"tractoring":None,"crippled":None,"time":0}