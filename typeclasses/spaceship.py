"""
Creates a spaceship with all it's functionalities.

"""

from typeclasses.rooms import Room
from typeclasses.exits import Exit
from evennia import create_object
from world import constants

class Ship(Room):
    """
    This creates a simple spaceship
    """

    def at_object_creation(self):
        super().at_object_creation()
        self.db.desc = "This is the bridge"
        self.db.type = constants.SHIP_ATTR_NAME
        self.db.sdesc = "Bridge"
        self.db.location = 0
        self.db.space = 0
        self.tags.add("space_object")
        self.db.coords = {"x":0.0,"y":0.0,"z":0.0, "speed":0.0}
        self.db.move = {"in":0.0,"out":0.0,"v":0.0,"ratio":1.0,"time":0,"quadrant":0,"dt":0,"cochranes":0}
        self.db.course = {"version":0,"d":[[0,0,0],[0,0,0],[0,0,0]],"yaw_in":0.0,"yaw_out":0.0,"roll_in":0.0,"roll_out":0.0,"pitch_in":0.0,"pitch_out":0.0}
        self.db.iff = {"frequency":0}
        self.db.shield = {0:{"active":0,"damage":100.0},1:{"active":0,"damage":100.0},2:{"active":0,"damage":100.0},3:{"active":0,"damage":100.0},4:{"active":0,"damage":100.0},5:{"active":0,"damage":100.0},"ratio":0,"visibility":0,"maximum":0}
        self.db.alloc = {"version":0,"shield":[0.0],"shields":0.0,"beams":0.0,"missiles":0.0,"sensors":0.0,"transporters":0.0,"tractors":0.0,"miscellaneous":0.0,"ecm":0.0,"eccm":0.0,"movement":0.0,"cloak":0.0}
        self.db.power = {"version":1,"total":0.0,"main":0.0,"aux":0.0,"batt":0.0}
        self.db.sensor = {"version":1,"ew_damage":0,"ew_active":0,"lrs_active":0,"srs_active":0,"counter":0}
        self.db.tech = {"stealth":1,"main_max":1,"aux_max":1,"fuel":1,"sensors":1,"ly_range":1}
        self.db.engine = {"version":1,"impulse_damage":0.0,"warp_damage":0.0,"warp_max":0.0,"impulse_max":0.0,"warp_exist":1,"impulse_exist":1,"warp_cruise":0.0}
        self.db.cloak = {"version":1,"active":0,"cost":0}
        self.db.trans = {"active":0,"d_lock":0,"s_lock":0}
        self.db.tract = {"active":0,"lock":0}
        self.db.main = {"exist":1,"in":0,"out":0,"gw":0,"damage":0}
        self.db.aux = {"exist":1,"gw":0,"in":0,"out":0,"damage":0}
        self.db.batt = {"in":0,"out":0,"gw":0}
        self.db.structure = {"superstructure":0.0,"type":constants.SHIP_ATTR_NAME,"displacement":0, "repair":0.0,"max_repair":0.0}
        self.db.status = {"active":0,"tractored":0,"tractoring":0,"crippled":0,"docked":0,"landed":0,"time":0,"autopilot":0}
        self.db.fuel = {"antimatter":0,"deuterium":0,"reserves":0}
        self.db.beam = {"in":0.0,"out":0.0,"banks":0}
        self.db.missile = {"tubes":0,"in":0.0,"out":0.0}
        self.db.slist = []
        self.db.blist = []
        self.db.engineering = {"start_sequence":0,"override":ship.key}
        for console in ["helm","engineering","science"]:
            ship_console = create_object(Console,key=self.key + "-"+ console)
            ship_console.db.sdesc = console
            ship_console.db.ship = self.key
            #specific commands for the consoles
            if(console == "engineering"):
                ship_console.cmdset.add("commands.engineering.EngineeringCmdSet", persistent=True)
            ship_console.tags.add(category=self.key,tag=console)
            exit_console_bridge = create_object(Exit, key=console, location=self, destination=ship_console)
            exit_console = create_object(Exit, key="Bridge",aliases=["bridge"], location=ship_console, destination=self)
        
    def get_display_name(self,looker, **kwargs):
       idstr = "(#%s)" % self.id if self.access(looker, access_type="control") else ""
       return "%s%s" % (self.db.sdesc, idstr)
       
class Console(Room):
    def at_object_creation(self):
        super().at_object_creation()
        self.tags.add(category="console",tag="general")
        self.db.type=constants.CONSOLE_ATTR_NAME
        self.db.sdesc = "Console"
        self.db.ship=""

    def get_display_name(self,looker, **kwargs):
       idstr = "(#%s)" % self.id if self.access(looker, access_type="control") else ""
       return "%s%s" % (self.db.sdesc, idstr)