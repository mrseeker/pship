"""
Creates a spaceship with all it's functionalities.

"""

from typeclasses.airlock import Airlock
from typeclasses.rooms import Room,space_room,Console
from typeclasses.exits import Exit
from evennia import create_object
from world import constants

class Ship(space_room):
    """
    This creates a default spaceship without any consoles
    """

    def at_object_creation(self):
        super().at_object_creation()
        self.db.desc = "This is the bridge of " + self.key
        self.db.type = constants.SHIP_ATTR_NAME
        self.tags.add(constants.SHIP_ATTR_NAME,category="space_object")
        self.tags.remove(constants.type_name[0],category="space_object")
        self.db.sdesc = "Bridge"
        self.db.structure["type"] = 1
        self.db.engineering = {"start_sequence":0,"override":self.key}
        self.db.ship = self.key

class Generic_Ship(Ship):
    def at_object_creation(self):
        super().at_object_creation()
        self.db.engine = {"version":0,"warp_damage":1.0,"warp_max":0,"warp_exist":1,"impulse_damage":1.0,"impulse_max":0,"impulse_exist":1,"warp_cruise":0.0,"impulse_cruise":0.0}
        self.db.tech = {"firing":1.0,"fuel":1.0,"stealth":1.0,"cloak":1.0,"sensors":1.0,"aux_max":1.05,"main_max":1.05,"armor":1.0,"ly_range":1.0}
        self.db.sensor = {"version":0,"lrs_damage":1.0,"lrs_active":1,"lrs_exist":1,"lrs_resolution":1.0,"lrs_signature":1.0,"srs_damage":1.0,"srs_active":1,"srs_exist":1,"srs_resolution":1.0,"srs_signature":1.0,"ew_damage":1.0,"ew_active":1,"ew_exist":1,"visibility":1.0,"contacts":1,"counter":1}
        self.db.tract = {"cost":1,"freq":1.0,"exist":1,"active":0,"damage":1.0,"lock":0}
        self.db.trans = {"cost":1,"freq":1.0,"exist":1,"active":0,"damage":1.0,"d_lock":0,"s_lock":0}
        self.db.shield = {"ratio":3.0,"maximum":18,"freq":1.0,"exist":1,0:{"active":0,"damage":1.0},1:{"active":0,"damage":1.0},2:{"active":0,"damage":1.0},3:{"active":0,"damage":1.0},4:{"active":0,"damage":1.0},5:{"active":0,"damage":1.0}}
        self.db.main["exist"] = 1
        self.db.aux["exist"] = 1
        self.db.batt["exist"] = 1

class Maquis_Ship(Ship):
    def at_object_creation(self):
        super().at_object_creation()
        self.db.engine = {"version":0,"warp_damage":1.0,"warp_max":0,"warp_exist":1,"impulse_damage":1.0,"impulse_max":0,"impulse_exist":1,"warp_cruise":0.0,"impulse_cruise":0.0}
        self.db.tech = {"firing":1.0,"fuel":1.0,"stealth":1.0,"cloak":1.0,"sensors":1.25,"aux_max":1.05,"main_max":1.05,"armor":1.0,"ly_range":2.0}
        self.db.sensor = {"version":0,"lrs_damage":1.0,"lrs_active":1,"lrs_exist":1,"lrs_resolution":1.0,"lrs_signature":1.0,"srs_damage":1.0,"srs_active":1,"srs_exist":1,"srs_resolution":1.0,"srs_signature":1.0,"ew_damage":1.0,"ew_active":1,"ew_exist":1,"visibility":1.0,"contacts":1,"counter":1}
        self.db.tract = {"cost":1,"freq":1.0,"exist":1,"active":0,"damage":1.0,"lock":0}
        self.db.trans = {"cost":1,"freq":1.0,"exist":1,"active":0,"damage":1.0,"d_lock":0,"s_lock":0}
        self.db.shield = {"ratio":3.0,"maximum":18,"freq":1.0,"exist":1,0:{"active":0,"damage":1.0},1:{"active":0,"damage":1.0},2:{"active":0,"damage":1.0},3:{"active":0,"damage":1.0},4:{"active":0,"damage":1.0},5:{"active":0,"damage":1.0}}
        self.db.main["exist"] = 1
        self.db.aux["exist"] = 1
        self.db.batt["exist"] = 1

class Gorn_Ship(Ship):
    def at_object_creation(self):
        super().at_object_creation()
        self.db.engine = {"version":0,"warp_damage":1.0,"warp_max":0,"warp_exist":1,"impulse_damage":1.0,"impulse_max":0,"impulse_exist":1,"warp_cruise":0.0,"impulse_cruise":0.0}
        self.db.tech = {"firing":1.0,"fuel":1.0,"stealth":1.0,"cloak":1.0,"sensors":1.1,"aux_max":1.1,"main_max":1.1,"armor":1.5,"ly_range":1.1}
        self.db.sensor = {"version":0,"lrs_damage":1.0,"lrs_active":1,"lrs_exist":1,"lrs_resolution":1.0,"lrs_signature":1.0,"srs_damage":1.0,"srs_active":1,"srs_exist":1,"srs_resolution":1.0,"srs_signature":1.0,"ew_damage":1.0,"ew_active":1,"ew_exist":1,"visibility":1.0,"contacts":1,"counter":1}
        self.db.tract = {"cost":1,"freq":1.0,"exist":1,"active":0,"damage":1.0,"lock":0}
        self.db.trans = {"cost":1,"freq":1.0,"exist":1,"active":0,"damage":1.0,"d_lock":0,"s_lock":0}
        self.db.shield = {"ratio":3.0,"maximum":18,"freq":1.0,"exist":1,0:{"active":0,"damage":1.0},1:{"active":0,"damage":1.0},2:{"active":0,"damage":1.0},3:{"active":0,"damage":1.0},4:{"active":0,"damage":1.0},5:{"active":0,"damage":1.0}}
        self.db.main["exist"] = 1
        self.db.aux["exist"] = 1
        self.db.batt["exist"] = 1

class Orion_Ship(Ship):
    def at_object_creation(self):
        super().at_object_creation()
        self.db.engine = {"version":0,"warp_damage":1.0,"warp_max":0,"warp_exist":1,"impulse_damage":1.0,"impulse_max":0,"impulse_exist":1,"warp_cruise":0.0,"impulse_cruise":0.0}
        self.db.tech = {"firing":1.0,"fuel":1.0,"stealth":2.0,"cloak":1.0,"sensors":1.0,"aux_max":2.0,"main_max":2.0,"armor":1.0,"ly_range":1.0}
        self.db.sensor = {"version":0,"lrs_damage":1.0,"lrs_active":1,"lrs_exist":1,"lrs_resolution":1.0,"lrs_signature":1.0,"srs_damage":1.0,"srs_active":1,"srs_exist":1,"srs_resolution":1.0,"srs_signature":1.0,"ew_damage":1.0,"ew_active":1,"ew_exist":1,"visibility":1.0,"contacts":1,"counter":1}
        self.db.tract = {"cost":1,"freq":1.0,"exist":1,"active":0,"damage":1.0,"lock":0}
        self.db.trans = {"cost":1,"freq":1.0,"exist":1,"active":0,"damage":1.0,"d_lock":0,"s_lock":0}
        self.db.shield = {"ratio":3.0,"maximum":18,"freq":1.0,"exist":1,0:{"active":0,"damage":1.0},1:{"active":0,"damage":1.0},2:{"active":0,"damage":1.0},3:{"active":0,"damage":1.0},4:{"active":0,"damage":1.0},5:{"active":0,"damage":1.0}}
        self.db.main["exist"] = 1
        self.db.aux["exist"] = 1
        self.db.batt["exist"] = 1

class Bajoran_Ship(Ship):
    def at_object_creation(self):
        super().at_object_creation()
        self.db.engine = {"version":0,"warp_damage":1.0,"warp_max":0,"warp_exist":1,"impulse_damage":1.0,"impulse_max":0,"impulse_exist":1,"warp_cruise":0.0,"impulse_cruise":0.0}
        self.db.tech = {"firing":1.0,"fuel":1.0,"stealth":1.0,"cloak":1.0,"sensors":1.25,"aux_max":1.05,"main_max":1.05,"armor":1.0,"ly_range":2.0}
        self.db.sensor = {"version":0,"lrs_damage":1.0,"lrs_active":1,"lrs_exist":1,"lrs_resolution":1.0,"lrs_signature":1.0,"srs_damage":1.0,"srs_active":1,"srs_exist":1,"srs_resolution":1.0,"srs_signature":1.0,"ew_damage":1.0,"ew_active":1,"ew_exist":1,"visibility":1.0,"contacts":1,"counter":1}
        self.db.tract = {"cost":1,"freq":1.0,"exist":1,"active":0,"damage":1.0,"lock":0}
        self.db.trans = {"cost":1,"freq":1.0,"exist":1,"active":0,"damage":1.0,"d_lock":0,"s_lock":0}
        self.db.shield = {"ratio":3.0,"maximum":18,"freq":1.0,"exist":1,0:{"active":0,"damage":1.0},1:{"active":0,"damage":1.0},2:{"active":0,"damage":1.0},3:{"active":0,"damage":1.0},4:{"active":0,"damage":1.0},5:{"active":0,"damage":1.0}}
        self.db.main["exist"] = 1
        self.db.aux["exist"] = 1
        self.db.batt["exist"] = 1

class Ferengi_Ship(Ship):
    def at_object_creation(self):
        super().at_object_creation()
        self.db.engine = {"version":0,"warp_damage":1.0,"warp_max":0,"warp_exist":1,"impulse_damage":1.0,"impulse_max":0,"impulse_exist":1,"warp_cruise":0.0,"impulse_cruise":0.0}
        self.db.tech = {"firing":1.0,"fuel":1.5,"stealth":1.0,"cloak":1.0,"sensors":1.0,"aux_max":1.1,"main_max":1.1,"armor":1.0,"ly_range":1.5}
        self.db.sensor = {"version":0,"lrs_damage":1.0,"lrs_active":1,"lrs_exist":1,"lrs_resolution":1.0,"lrs_signature":1.0,"srs_damage":1.0,"srs_active":1,"srs_exist":1,"srs_resolution":1.0,"srs_signature":1.0,"ew_damage":1.0,"ew_active":1,"ew_exist":1,"visibility":1.0,"contacts":1,"counter":1}
        self.db.tract = {"cost":1,"freq":1.0,"exist":1,"active":0,"damage":1.0,"lock":0}
        self.db.trans = {"cost":1,"freq":1.0,"exist":1,"active":0,"damage":1.0,"d_lock":0,"s_lock":0}
        self.db.shield = {"ratio":3.0,"maximum":18,"freq":1.0,"exist":1,0:{"active":0,"damage":1.0},1:{"active":0,"damage":1.0},2:{"active":0,"damage":1.0},3:{"active":0,"damage":1.0},4:{"active":0,"damage":1.0},5:{"active":0,"damage":1.0}}
        self.db.main["exist"] = 1
        self.db.aux["exist"] = 1
        self.db.batt["exist"] = 1

class Romulan_Ship(Ship):
    def at_object_creation(self):
        super().at_object_creation()
        self.db.engine = {"version":0,"warp_damage":1.0,"warp_max":0,"warp_exist":1,"impulse_damage":1.0,"impulse_max":0,"impulse_exist":1,"warp_cruise":0.0,"impulse_cruise":0.0}
        self.db.tech = {"firing":1.0,"fuel":1.25,"stealth":1.25,"cloak":1.25,"sensors":1.25,"aux_max":1.05,"main_max":1.05,"armor":1.0,"ly_range":1.0}
        self.db.sensor = {"version":0,"lrs_damage":1.0,"lrs_active":1,"lrs_exist":1,"lrs_resolution":1.0,"lrs_signature":1.0,"srs_damage":1.0,"srs_active":1,"srs_exist":1,"srs_resolution":1.0,"srs_signature":1.0,"ew_damage":1.0,"ew_active":1,"ew_exist":1,"visibility":1.0,"contacts":1,"counter":1}
        self.db.tract = {"cost":1,"freq":1.0,"exist":1,"active":0,"damage":1.0,"lock":0}
        self.db.trans = {"cost":1,"freq":1.0,"exist":1,"active":0,"damage":1.0,"d_lock":0,"s_lock":0}
        self.db.shield = {"ratio":3.0,"maximum":18,"freq":1.0,"exist":1,0:{"active":0,"damage":1.0},1:{"active":0,"damage":1.0},2:{"active":0,"damage":1.0},3:{"active":0,"damage":1.0},4:{"active":0,"damage":1.0},5:{"active":0,"damage":1.0}}
        self.db.main["exist"] = 1
        self.db.aux["exist"] = 1
        self.db.batt["exist"] = 1

class Klingon_Ship(Ship):
    def at_object_creation(self):
        super().at_object_creation()
        self.db.engine = {"version":0,"warp_damage":1.0,"warp_max":0,"warp_exist":1,"impulse_damage":1.0,"impulse_max":0,"impulse_exist":1,"warp_cruise":0.0,"impulse_cruise":0.0}
        self.db.tech = {"firing":1.25,"fuel":1.0,"stealth":1.0,"cloak":1.0,"sensors":1.0,"aux_max":1.1,"main_max":1.1,"armor":2.0,"ly_range":1.0}
        self.db.sensor = {"version":0,"lrs_damage":1.0,"lrs_active":1,"lrs_exist":1,"lrs_resolution":1.0,"lrs_signature":1.0,"srs_damage":1.0,"srs_active":1,"srs_exist":1,"srs_resolution":1.0,"srs_signature":1.0,"ew_damage":1.0,"ew_active":1,"ew_exist":1,"visibility":1.0,"contacts":1,"counter":1}
        self.db.tract = {"cost":1,"freq":1.0,"exist":1,"active":0,"damage":1.0,"lock":0}
        self.db.trans = {"cost":1,"freq":1.0,"exist":1,"active":0,"damage":1.0,"d_lock":0,"s_lock":0}
        self.db.shield = {"ratio":3.0,"maximum":18,"freq":1.0,"exist":1,0:{"active":0,"damage":1.0},1:{"active":0,"damage":1.0},2:{"active":0,"damage":1.0},3:{"active":0,"damage":1.0},4:{"active":0,"damage":1.0},5:{"active":0,"damage":1.0}}
        self.db.main["exist"] = 1
        self.db.aux["exist"] = 1
        self.db.batt["exist"] = 1

class Dominion_Ship(Ship):
    def at_object_creation(self):
        super().at_object_creation()
        self.db.engine = {"version":0,"warp_damage":1.0,"warp_max":0,"warp_exist":1,"impulse_damage":1.0,"impulse_max":0,"impulse_exist":1,"warp_cruise":0.0,"impulse_cruise":0.0}
        self.db.tech = {"firing":1.25,"fuel":1.0,"stealth":1.0,"cloak":1.0,"sensors":1.25,"aux_max":1.1,"main_max":1.1,"armor":2.0,"ly_range":1.0}
        self.db.sensor = {"version":0,"lrs_damage":1.0,"lrs_active":1,"lrs_exist":1,"lrs_resolution":1.0,"lrs_signature":1.0,"srs_damage":1.0,"srs_active":1,"srs_exist":1,"srs_resolution":1.0,"srs_signature":1.0,"ew_damage":1.0,"ew_active":1,"ew_exist":1,"visibility":1.0,"contacts":1,"counter":1}
        self.db.tract = {"cost":1,"freq":1.0,"exist":1,"active":0,"damage":1.0,"lock":0}
        self.db.trans = {"cost":1,"freq":1.0,"exist":1,"active":0,"damage":1.0,"d_lock":0,"s_lock":0}
        self.db.shield = {"ratio":3.0,"maximum":18,"freq":1.0,"exist":1,0:{"active":0,"damage":1.0},1:{"active":0,"damage":1.0},2:{"active":0,"damage":1.0},3:{"active":0,"damage":1.0},4:{"active":0,"damage":1.0},5:{"active":0,"damage":1.0}}
        self.db.main["exist"] = 1
        self.db.aux["exist"] = 1
        self.db.batt["exist"] = 1

class Borg_Ship(Ship):
    def at_object_creation(self):
        super().at_object_creation()
        self.db.engine = {"version":0,"warp_damage":1.0,"warp_max":0,"warp_exist":1,"impulse_damage":1.0,"impulse_max":0,"impulse_exist":1,"warp_cruise":0.0,"impulse_cruise":0.0}
        self.db.tech = {"firing":1.25,"fuel":1.25,"stealth":1.25,"cloak":1.25,"sensors":1.25,"aux_max":2.0,"main_max":2.0,"armor":1.25,"ly_range":2.0}
        self.db.sensor = {"version":0,"lrs_damage":1.0,"lrs_active":1,"lrs_exist":1,"lrs_resolution":1.0,"lrs_signature":1.0,"srs_damage":1.0,"srs_active":1,"srs_exist":1,"srs_resolution":1.0,"srs_signature":1.0,"ew_damage":1.0,"ew_active":1,"ew_exist":1,"visibility":1.0,"contacts":1,"counter":1}
        self.db.tract = {"cost":1,"freq":1.0,"exist":1,"active":0,"damage":1.0,"lock":0}
        self.db.trans = {"cost":1,"freq":1.0,"exist":1,"active":0,"damage":1.0,"d_lock":0,"s_lock":0}
        self.db.shield = {"ratio":3.0,"maximum":18,"freq":1.0,"exist":1,0:{"active":0,"damage":1.0},1:{"active":0,"damage":1.0},2:{"active":0,"damage":1.0},3:{"active":0,"damage":1.0},4:{"active":0,"damage":1.0},5:{"active":0,"damage":1.0}}
        self.db.main["exist"] = 1
        self.db.aux["exist"] = 1
        self.db.batt["exist"] = 1

class Cardassian_Ship(Ship):
    def at_object_creation(self):
        super().at_object_creation()
        self.db.engine = {"version":0,"warp_damage":1.0,"warp_max":0,"warp_exist":1,"impulse_damage":1.0,"impulse_max":0,"impulse_exist":1,"warp_cruise":0.0,"impulse_cruise":0.0}
        self.db.tech = {"firing":1.0,"fuel":1.0,"stealth":1.25,"cloak":1.25,"sensors":1.1,"aux_max":1.1,"main_max":1.1,"armor":1.1,"ly_range":1.0}
        self.db.sensor = {"version":0,"lrs_damage":1.0,"lrs_active":1,"lrs_exist":1,"lrs_resolution":1.0,"lrs_signature":1.0,"srs_damage":1.0,"srs_active":1,"srs_exist":1,"srs_resolution":1.0,"srs_signature":1.0,"ew_damage":1.0,"ew_active":1,"ew_exist":1,"visibility":1.0,"contacts":1,"counter":1}
        self.db.tract = {"cost":1,"freq":1.0,"exist":1,"active":0,"damage":1.0,"lock":0}
        self.db.trans = {"cost":1,"freq":1.0,"exist":1,"active":0,"damage":1.0,"d_lock":0,"s_lock":0}
        self.db.shield = {"ratio":3.0,"maximum":18,"freq":1.0,"exist":1,0:{"active":0,"damage":1.0},1:{"active":0,"damage":1.0},2:{"active":0,"damage":1.0},3:{"active":0,"damage":1.0},4:{"active":0,"damage":1.0},5:{"active":0,"damage":1.0}}
        self.db.main["exist"] = 1
        self.db.aux["exist"] = 1
        self.db.batt["exist"] = 1

class UFP_Ship(Ship):
    def at_object_creation(self):
        super().at_object_creation()
        self.db.engine = {"version":0,"warp_damage":1.0,"warp_max":0,"warp_exist":1,"impulse_damage":1.0,"impulse_max":0,"impulse_exist":1,"warp_cruise":0.0,"impulse_cruise":0.0}
        self.db.tech = {"firing":1.0,"fuel":1.1,"stealth":1.0,"cloak":1.0,"sensors":1.25,"aux_max":1.1,"main_max":1.1,"armor":1.0,"ly_range":2.0}
        self.db.sensor = {"version":0,"lrs_damage":1.0,"lrs_active":1,"lrs_exist":1,"lrs_resolution":1.0,"lrs_signature":1.0,"srs_damage":1.0,"srs_active":1,"srs_exist":1,"srs_resolution":1.0,"srs_signature":1.0,"ew_damage":1.0,"ew_active":1,"ew_exist":1,"visibility":1.0,"contacts":1,"counter":1}
        self.db.tract = {"cost":1,"freq":1.0,"exist":1,"active":0,"damage":1.0,"lock":0}
        self.db.trans = {"cost":1,"freq":1.0,"exist":1,"active":0,"damage":1.0,"d_lock":0,"s_lock":0}
        self.db.shield = {"ratio":3.0,"maximum":18,"freq":1.0,"exist":1,0:{"active":0,"damage":1.0},1:{"active":0,"damage":1.0},2:{"active":0,"damage":1.0},3:{"active":0,"damage":1.0},4:{"active":0,"damage":1.0},5:{"active":0,"damage":1.0}}
        self.db.main["exist"] = 1
        self.db.aux["exist"] = 1
        self.db.batt["exist"] = 1

class Fighter(Ship):
    """
    This is a generic fighter class. It is a very limited spaceship
    """
    def at_object_creation(self):
        super().at_object_creation()
        self.cmdset.add("commands.bridge.FighterBridgeCmdSet", persistent=True)
        self.cmdset.add("commands.engineering.EngineeringFighterCmdSet", persistent=True)
        self.cmdset.add("commands.tactical.TacticalCmdSet", persistent=True)
        self.cmdset.add("commands.helm.FighterCmdSet", persistent=True)

class Test(Ship):
    """
    This is a generic testship that holds all consoles in one single area.
    """
    def at_object_creation(self):
        super().at_object_creation()
        self.cmdset.add("commands.bridge.BridgeCmdSet", persistent=True)
        for console in ["helm","engineering","tactical","science","security","operation"]:
            ship_console = create_object(Console,key=self.key + "-"+ console)
            ship_console.db.sdesc = console
            ship_console.db.ship = self.key
            #specific commands for the consoles
            if(console == "engineering"):
                ship_console.cmdset.add("commands.engineering.EngineeringCmdSet", persistent=True)
            if(console == "tactical"):
                ship_console.cmdset.add("commands.tactical.TacticalCmdSet", persistent=True)
            if(console == "helm"):
                ship_console.cmdset.add("commands.helm.HelmCmdSet", persistent=True)
            if(console == "operation"):
                ship_console.cmdset.add("commands.operation.OperationCmdSet", persistent=True)
            ship_console.tags.add(console,category=self.key)
            exit_console_bridge = create_object(Exit, key=console, location=self, destination=ship_console)
            exit_console = create_object(Exit, key="Bridge",aliases=["bridge"], location=ship_console, destination=self)
        
        ship_airlock = create_object(Airlock,key=self.key + "-airlock")
        ship_airlock.db.ship = self.key
        ship_airlock.tags.add("airlock",category=self.key)
        exit_airlock_bridge = create_object(Exit, key="Airlock",aliases=["airlock"], location=self, destination=ship_airlock)
        exit_airlock = create_object(Exit, key="Bridge",aliases=["bridge"], location=ship_airlock, destination=self)

        ship_teleport = create_object(Room,key=self.key + "-teleport")
        ship_teleport.db.ship = self.key
        ship_teleport.tags.add("teleport",category=self.key)
        exit_teleport_bridge = create_object(Exit, key="Teleporter room",aliases=["teleport"], location=self, destination=ship_teleport)
        exit_teleport = create_object(Exit, key="Bridge",aliases=["bridge"], location=ship_teleport, destination=self)