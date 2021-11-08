"""
Room

Rooms are simple containers that has no location of their own.

"""

from evennia.contrib.rpsystem import ContribRPRoom
from world import constants

class Room(ContribRPRoom):
    """
    Rooms are like any Object, except their location is None
    (which is default). They also use basetype_setup() to
    add locks so they cannot be puppeted or picked up.
    (to change that, use at_object_creation instead)

    See examples/object.py for a list of
    properties and methods available on all Objects.
    """

    def at_object_creation(self):
        super().at_object_creation()

class space_room(Room):
    """
    This creates a default space_room.
    """

    def at_object_creation(self):
        super().at_object_creation()
        self.db.desc = "This is a space room. You should not see this message."
        self.db.type = constants.type_name[0]
        self.db.sdesc = "Default Space Room"
        self.db.location = 0
        self.db.space = 0
        self.db.language = "default"
        self.tags.add(category="space_object",tag=constants.type_name[0])
        self.db.coords = {"x":0.0,"y":0.0,"z":0.0,"xo":0.0,"yo":0.0,"zo":0.0,"xd":0.0,"yd":0.0,"zd":0.0}
        self.db.move = {"time":0,"dt":0,"in":0.0,"out":0.0,"ratio":1.0,"cochranes":0.0,"v":0.0,"empire":"","quadrant":0}
        self.db.course = {"version":0,"yaw_in":0.0,"yaw_out":0.0,"pitch_in":0.0,"pitch_out":0.0,"roll_in":0.0,"roll_out":0.0,"d":[[0,0,0],[0,0,0],[0,0,0]],"rate":0.0}
        self.db.iff = {"frequency":0.0}
        shield_combo = {"ratio":0.0,"maximum":0,"freq":0.0,"exist":0}
        for i in range(constants.MAX_SHIELD_NAME):
            shield_combo[i] = {"active":0,"damage":0}
        self.db.shield = shield_combo
        self.db.alloc = {"version":1,"helm":0.0,"tactical":0.0,"operations":0.0,"movement":0.0,"shields":0.0,"shield":[0.0]*constants.MAX_SHIELD_NAME,"cloak":0.0,"beams":0.0,"missiles":0.0,"sensors":0.0,"ecm":0.0,"eccm":0.0,"transporters":0.0,"tractors":0.0,"miscellaneous":0.0}
        self.db.power = {"version":1,"main":0.0,"aux":0.0,"batt":0.0,"total":0.0}
        self.db.sensor = {"version":1,"lrs_damage":1.0,"lrs_active":0,"lrs_exist":0,"lrs_resolution":1.0,"srs_signature":1.0,"srs_damage":1.0,"srs_active":0,"srs_exist":0,"srs_resolution":1.0,"srs_signature":1.0,"ew_damage":1.0,"ew_exist":0,"visibility":1.0,"contacts":0,"counter":0}
        self.db.tech = {"firing":1.0,"fuel":1.0,"stealth":1.0,"cloak":1.0,"sensors":1.0,"aux_max":1.0,"main_max":1.0,"armor":1.0,"ly_range":1.0}
        self.db.engine = {"version":1,"warp_damage":1.0,"warp_max":1.0,"warp_exist":0,"impulse_damage":1.0,"impulse_max":1.0,"impulse_exist":1,"warp_cruise":0.0,"impulse_cruise":0.0}
        self.db.cloak = {"version":1,"cost":0,"freq":0.0,"exist":0,"active":0,"damage":0.0}
        self.db.trans = {"cost":0,"freq":0.0,"exist":0,"active":0,"damage":1.0,"d_lock":0,"s_lock":0}
        self.db.tract = {"cost":0,"freq":0.0,"exist":0,"active":0,"damage":1.0,"lock":0}
        self.db.main = {"in":0.0,"out":0.0,"damage":1.0,"gw":0.0,"exist":0}
        self.db.aux = {"in":0.0,"out":0.0,"damage":1.0,"gw":0.0,"exist":0}
        self.db.batt = {"in":0.0,"out":0.0,"damage":1.0,"gw":0.0,"exist":0}
        self.db.structure = {"type":0,"displacement":1.0,"cargo_hold":0.0, "cargo_mass":0.0, "superstructure":0.0,"has_landing_pad":0,"has_docking_bay":0,"can_land":0,"can_dock":0,"repair":0.0,"max_repair":0}
        self.db.status = {"active":0,"docked":0,"landed":0,"connected":0,"crippled":0,"tractoring":0,"tractored":0,"open_landing":0,"open_docking":0,"link":0,"autopilot":0}
        self.db.fuel = {"antimatter":0,"deuterium":0,"reserves":0}
        self.db.beam = {"in":0.0,"out":0.0,"freq":0.0,"exist":0,"banks":0}
        self.db.missile = {"in":0.0,"out":0.0,"freq":0.0,"exist":0,"tubes":0}
        beam_combo = {}
        for i in range(constants.MAX_BEAM_BANKS):
            beam_combo[i] = {"active":0,"name":0,"lock":"","damage":0.0,"bonus":0,"cost":0,"range":0,"arcs":0,"load":0,"recycle":0}
        self.db.blist = beam_combo
        missile_combo = {}
        for i in range(constants.MAX_MISSILE_TUBES):
            missile_combo[i] = {"active":0,"name":0,"lock":"","damage":0.0,"warhead":0,"cost":0,"range":0,"arcs":0,"load":0,"recycle":0}
        self.db.mlist = missile_combo
        sensor_combo = {}
        for i in range(constants.MAX_SENSOR_CONTACTS):
            sensor_combo[i] = {"key":"","num":0,"lev":0.0}
        self.db.slist = sensor_combo
        
    def get_display_name(self,looker, **kwargs):
       idstr = "(#%s)" % self.id if self.access(looker, access_type="control") else ""
       selfdesc = self.name if self.access(looker, access_type="control") else self.db.sdesc
       return "%s%s" % (selfdesc, idstr)
