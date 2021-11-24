from unicodedata import category
from evennia.utils.create import create_object
from typeclasses.airlock import Airlock
from typeclasses.exits import Exit
from typeclasses.rooms import Room
from typeclasses.spaceship import Console, Generic_Ship

class Shuttle(Generic_Ship):
    def at_object_creation(self):
        super().at_object_creation()
        self.db.move["ratio"] = 1.0
        self.db.main["gw"] = 4.0 
        self.db.aux["gw"] = 1.0
        self.db.batt["gw"]= 0.4
        self.db.beam["banks"] = 1
        self.db.beam["exist"] = 1
        self.db.structure = {"type":1,"displacement":785,"cargo_hold":0,"cargo_mass":0.0,"superstructure":1.0,"max_structure":1,"has_landing_pad":0,"has_docking_bay":0,"can_land":1,"can_dock":0,"repair":1,"max_repair":1}
        self.db.blist[0] = {"active":0,"name":1,"damage":1.0,"bonus":0,"cost":3,"range":160,"arcs":33,"lock":0,"load":0,"recycle":6}
        self.db.cost = 0
        create_fighter_layout(self)

class Courier_II(Generic_Ship):
    def at_object_creation(self):
        super().at_object_creation()
        self.db.move["ratio"] = 1.0
        self.db.main["gw"] = 24.0 
        self.db.aux["gw"] = 16.0
        self.db.batt["gw"]= 2.4
        self.db.beam["banks"] = 2
        self.db.beam["exist"] = 1
        self.db.missile["tubes"] = 2
        self.db.missile["exist"] = 1
        self.db.structure = {"type":1,"displacement":24210,"cargo_hold":13200,"cargo_mass":0.0,"superstructure":20.0,"max_structure":20,"has_landing_pad":1,"has_docking_bay":0,"can_land":1,"can_dock":1,"repair":20.0,"max_repair":20}
        self.db.blist[0] = {"active":0,"name":4,"damage":1.0,"bonus":3,"cost":10,"range":480,"arcs":61,"lock":0,"load":0,"recycle":6}
        self.db.blist[1] = {"active":0,"name":4,"damage":1.0,"bonus":3,"cost":10,"range":480,"arcs":55,"lock":0,"load":0,"recycle":6}
        self.db.mlist[0] = {"active":0,"name":9,"damage":1.0,"warhead":25,"cost":2,"range":320,"arcs":57,"lock":0,"load":0,"recycle":15}
        self.db.mlist[1] = {"active":0,"name":9,"damage":1.0,"warhead":25,"cost":2,"range":320,"arcs":51,"lock":0,"load":0,"recycle":15}
        self.db.cost = 81709
        create_fighter_layout(self)

class Scout_Cruiser_III(Generic_Ship):
    def at_object_creation(self):
        super().at_object_creation()
        self.db.move["ratio"] = 2.0
        self.db.main["gw"] = 40.0 
        self.db.aux["gw"] = 24.0
        self.db.batt["gw"]= 4.0
        self.db.beam["banks"] = 4
        self.db.beam["exist"] = 1
        self.db.tech = {"firing":1.0,"fuel":1.0,"stealth":2.0,"cloak":1.0,"sensors":2.0,"aux_max":2.0,"main_max":2.0,"armor":1.0,"ly_range":1.0}
        self.db.structure = {"type":1,"displacement":49360,"cargo_hold":4936,"cargo_mass":0.0,"superstructure":59.0,"max_structure":59,"has_landing_pad":1,"has_docking_bay":0,"can_land":1,"can_dock":1,"repair":59.0,"max_repair":59}
        self.db.blist[0] = {"active":0,"name":3,"damage":1.0,"bonus":20,"cost":30,"range":260,"arcs":41,"lock":0,"load":0,"recycle":6}
        self.db.blist[1] = {"active":0,"name":3,"damage":1.0,"bonus":20,"cost":30,"range":260,"arcs":35,"lock":0,"load":0,"recycle":6}
        self.db.blist[2] = {"active":0,"name":4,"damage":1.0,"bonus":12,"cost":40,"range":480,"arcs":31,"lock":0,"load":0,"recycle":6}
        self.db.blist[3] = {"active":0,"name":4,"damage":1.0,"bonus":12,"cost":40,"range":480,"arcs":47,"lock":0,"load":0,"recycle":6}
        self.db.cost = 325240
        create_ship_layout(self)

class FrS(Generic_Ship):
    def at_object_creation(self):
        super().at_object_creation()
        self.db.move["ratio"] = 8.0
        self.db.main["gw"] = 64.0 
        self.db.aux["gw"] = 8.0
        self.db.batt["gw"]= 6.4
        self.db.beam["banks"] = 4
        self.db.beam["exist"] = 1
        self.db.tech["ly_range"] = 2.0
        self.db.structure = {"type":1,"displacement":399880,"cargo_hold":275400,"cargo_mass":0.0,"superstructure":234.0,"max_structure":234,"has_landing_pad":0,"has_docking_bay":0,"can_land":1,"can_dock":1,"repair":234.0,"max_repair":234.0}
        self.db.blist[0] = {"active":0,"name":8,"damage":1.0,"bonus":2,"cost":7,"range":400,"arcs":31,"lock":0,"load":0,"recycle":6}
        self.db.blist[1] = {"active":0,"name":8,"damage":1.0,"bonus":2,"cost":7,"range":400,"arcs":31,"lock":0,"load":0,"recycle":6}
        self.db.blist[2] = {"active":0,"name":8,"damage":1.0,"bonus":2,"cost":7,"range":400,"arcs":47,"lock":0,"load":0,"recycle":6}
        self.db.blist[3] = {"active":0,"name":8,"damage":1.0,"bonus":2,"cost":7,"range":400,"arcs":47,"lock":0,"load":0,"recycle":6}
        self.db.cost = 83851428
        create_ship_layout(self)

class Mega_Freight_IV(Generic_Ship):
    def at_object_creation(self):
        super().at_object_creation()
        self.db.move["ratio"] = 64.0
        self.db.main["gw"] = 960.0 
        self.db.aux["gw"] = 64.0
        self.db.batt["gw"]= 96.0
        self.db.beam["banks"] = 4
        self.db.beam["exist"] = 1
        self.db.tech["ly_range"] = 2.0
        self.db.structure = {"type":1,"displacement":3199400,"cargo_hold":2233200,"cargo_mass":0.0,"superstructure":1594.0,"max_structure":1594,"has_landing_pad":0,"has_docking_bay":0,"can_land":1,"can_dock":1,"repair":1594.0,"max_repair":1594.0}
        self.db.blist[0] = {"active":0,"name":8,"damage":1.0,"bonus":2,"cost":7,"range":400,"arcs":31,"lock":0,"load":0,"recycle":6}
        self.db.blist[1] = {"active":0,"name":8,"damage":1.0,"bonus":2,"cost":7,"range":400,"arcs":31,"lock":0,"load":0,"recycle":6}
        self.db.blist[2] = {"active":0,"name":8,"damage":1.0,"bonus":2,"cost":7,"range":400,"arcs":47,"lock":0,"load":0,"recycle":6}
        self.db.blist[3] = {"active":0,"name":8,"damage":1.0,"bonus":2,"cost":7,"range":400,"arcs":47,"lock":0,"load":0,"recycle":6}
        self.db.cost = 536914
        create_ship_layout(self)

class Super_Freight_IV(Generic_Ship):
    def at_object_creation(self):
        super().at_object_creation()
        self.db.move["ratio"] = 8.0
        self.db.main["gw"] = 120.0 
        self.db.aux["gw"] = 8.0
        self.db.batt["gw"]= 12.0
        self.db.beam["banks"] = 4
        self.db.beam["exist"] = 1
        self.db.missile["tubes"] = 1
        self.db.missile["exist"] = 1
        self.db.tech["ly_range"] = 2.0
        self.db.structure = {"type":1,"displacement":399880,"cargo_hold":275400,"cargo_mass":0.0,"superstructure":227.0,"max_structure":227,"has_landing_pad":0,"has_docking_bay":0,"can_land":1,"can_dock":1,"repair":227.0,"max_repair":227}
        self.db.blist[0] = {"active":0,"name":8,"damage":1.0,"bonus":2,"cost":7,"range":400,"arcs":31,"lock":0,"load":0,"recycle":6}
        self.db.blist[1] = {"active":0,"name":8,"damage":1.0,"bonus":2,"cost":7,"range":400,"arcs":31,"lock":0,"load":0,"recycle":6}
        self.db.blist[2] = {"active":0,"name":8,"damage":1.0,"bonus":2,"cost":7,"range":400,"arcs":47,"lock":0,"load":0,"recycle":6}
        self.db.blist[3] = {"active":0,"name":8,"damage":1.0,"bonus":2,"cost":7,"range":400,"arcs":47,"lock":0,"load":0,"recycle":6}
        self.db.mlist[1] = {"active":0,"name":9,"damage":1.0,"warhead":25,"cost":2,"range":320,"arcs":43,"lock":0,"load":0,"recycle":15}
        self.db.cost = 83851
        create_ship_layout(self)

class Medium_Cruiser_III(Generic_Ship):
    def at_object_creation(self):
        super().at_object_creation()
        self.db.move["ratio"] = 3.0
        self.db.main["gw"] = 60.0 
        self.db.aux["gw"] = 36.0
        self.db.batt["gw"]= 6.0
        self.db.beam["banks"] = 4
        self.db.beam["exist"] = 1
        self.db.missile["tubes"] = 6
        self.db.missile["exist"] = 1
        self.db.structure = {"type":1,"displacement":99360,"cargo_hold":9936,"cargo_mass":0.0,"superstructure":104.0,"max_structure":104,"has_landing_pad":1,"has_docking_bay":0,"can_land":1,"can_dock":1,"repair":104.0,"max_repair":104}
        self.db.blist[0] = {"active":0,"name":3,"damage":1.0,"bonus":20,"cost":30,"range":260,"arcs":41,"lock":0,"load":0,"recycle":6}
        self.db.blist[1] = {"active":0,"name":3,"damage":1.0,"bonus":20,"cost":30,"range":260,"arcs":35,"lock":0,"load":0,"recycle":6}
        self.db.blist[2] = {"active":0,"name":4,"damage":1.0,"bonus":18,"cost":60,"range":480,"arcs":31,"lock":0,"load":0,"recycle":6}
        self.db.blist[3] = {"active":0,"name":4,"damage":1.0,"bonus":18,"cost":60,"range":480,"arcs":47,"lock":0,"load":0,"recycle":6}
        self.db.mlist[0] = {"active":0,"name":9,"damage":1.0,"warhead":25,"cost":2,"range":320,"arcs":27,"lock":0,"load":0,"recycle":15}
        self.db.mlist[1] = {"active":0,"name":9,"damage":1.0,"warhead":25,"cost":2,"range":320,"arcs":27,"lock":0,"load":0,"recycle":15}
        self.db.mlist[2] = {"active":0,"name":9,"damage":1.0,"warhead":25,"cost":2,"range":320,"arcs":27,"lock":0,"load":0,"recycle":15}
        self.db.mlist[3] = {"active":0,"name":9,"damage":1.0,"warhead":25,"cost":2,"range":320,"arcs":27,"lock":0,"load":0,"recycle":15}
        self.db.mlist[4] = {"active":0,"name":9,"damage":1.0,"warhead":25,"cost":2,"range":320,"arcs":30,"lock":0,"load":0,"recycle":15}
        self.db.mlist[5] = {"active":0,"name":9,"damage":1.0,"warhead":25,"cost":2,"range":320,"arcs":30,"lock":0,"load":0,"recycle":15}        
        self.db.cost = 681406
        create_ship_layout(self)

class Light_Cruiser_II(Generic_Ship):
    def at_object_creation(self):
        super().at_object_creation()
        self.db.move["ratio"] = 2.0
        self.db.main["gw"] = 36.0 
        self.db.aux["gw"] = 24.0
        self.db.batt["gw"]= 3.6
        self.db.beam["banks"] = 6
        self.db.beam["exist"] = 1
        self.db.missile["tubes"] = 2
        self.db.missile["exist"] = 1
        self.db.structure = {"type":1,"displacement":49960,"cargo_hold":4996,"cargo_mass":0.0,"superstructure":49.0,"max_structure":49,"has_landing_pad":1,"has_docking_bay":0,"can_land":1,"can_dock":1,"repair":49.0,"max_repair":49}
        self.db.blist[0] = {"active":0,"name":4,"damage":1.0,"bonus":6,"cost":20,"range":480,"arcs":27,"lock":0,"load":0,"recycle":6}
        self.db.blist[1] = {"active":0,"name":4,"damage":1.0,"bonus":6,"cost":20,"range":480,"arcs":43,"lock":0,"load":0,"recycle":6}
        self.db.blist[2] = {"active":0,"name":4,"damage":1.0,"bonus":6,"cost":20,"range":480,"arcs":29,"lock":0,"load":0,"recycle":6}
        self.db.blist[3] = {"active":0,"name":4,"damage":1.0,"bonus":6,"cost":20,"range":480,"arcs":45,"lock":0,"load":0,"recycle":6}
        self.db.blist[4] = {"active":0,"name":4,"damage":1.0,"bonus":6,"cost":20,"range":480,"arcs":23,"lock":0,"load":0,"recycle":6}
        self.db.blist[5] = {"active":0,"name":4,"damage":1.0,"bonus":6,"cost":20,"range":480,"arcs":39,"lock":0,"load":0,"recycle":6}
        self.db.mlist[0] = {"active":0,"name":9,"damage":1.0,"warhead":25,"cost":2,"range":320,"arcs":43,"lock":0,"load":0,"recycle":15}
        self.db.mlist[1] = {"active":0,"name":9,"damage":1.0,"warhead":25,"cost":2,"range":320,"arcs":43,"lock":0,"load":0,"recycle":15}
        self.db.cost = 321177
        create_ship_layout(self)

class Medium_Cruiser_II(Generic_Ship):
    def at_object_creation(self):
        super().at_object_creation()
        self.db.move["ratio"] = 3.0
        self.db.main["gw"] = 54.0 
        self.db.aux["gw"] = 36.0
        self.db.batt["gw"]= 5.4
        self.db.beam["banks"] = 6
        self.db.beam["exist"] = 1
        self.db.missile["tubes"] = 3
        self.db.missile["exist"] = 1
        self.db.structure = {"type":1,"displacement":99060,"cargo_hold":9906,"cargo_mass":0.0,"superstructure":91.0,"max_structure":91,"has_landing_pad":1,"has_docking_bay":0,"can_land":1,"can_dock":1,"repair":91.0,"max_repair":91}
        self.db.blist[0] = {"active":0,"name":4,"damage":1.0,"bonus":9,"cost":30,"range":480,"arcs":27,"lock":0,"load":0,"recycle":6}
        self.db.blist[1] = {"active":0,"name":4,"damage":1.0,"bonus":9,"cost":30,"range":480,"arcs":43,"lock":0,"load":0,"recycle":6}
        self.db.blist[2] = {"active":0,"name":4,"damage":1.0,"bonus":9,"cost":30,"range":480,"arcs":29,"lock":0,"load":0,"recycle":6}
        self.db.blist[3] = {"active":0,"name":4,"damage":1.0,"bonus":9,"cost":30,"range":480,"arcs":45,"lock":0,"load":0,"recycle":6}
        self.db.blist[4] = {"active":0,"name":4,"damage":1.0,"bonus":9,"cost":30,"range":480,"arcs":23,"lock":0,"load":0,"recycle":6}
        self.db.blist[5] = {"active":0,"name":4,"damage":1.0,"bonus":9,"cost":30,"range":480,"arcs":39,"lock":0,"load":0,"recycle":6}
        self.db.mlist[0] = {"active":0,"name":9,"damage":1.0,"warhead":25,"cost":2,"range":320,"arcs":43,"lock":0,"load":0,"recycle":15}
        self.db.mlist[1] = {"active":0,"name":9,"damage":1.0,"warhead":25,"cost":2,"range":320,"arcs":43,"lock":0,"load":0,"recycle":15}
        self.db.mlist[2] = {"active":0,"name":9,"damage":1.0,"warhead":25,"cost":2,"range":320,"arcs":43,"lock":0,"load":0,"recycle":15}
        self.db.cost = 610645714
        create_ship_layout(self)

class Heavy_Cruiser_II(Generic_Ship):
    def at_object_creation(self):
        super().at_object_creation()
        self.db.move["ratio"] = 4.0
        self.db.main["gw"] = 72.0 
        self.db.aux["gw"] = 24.0
        self.db.batt["gw"]= 7.2
        self.db.beam["banks"] = 6
        self.db.beam["exist"] = 1
        self.db.missile["tubes"] = 4
        self.db.missile["exist"] = 1
        self.db.structure = {"type":1,"displacement":199160,"cargo_hold":19916,"cargo_mass":0.0,"superstructure":167.0,"max_structure":167,"has_landing_pad":1,"has_docking_bay":0,"can_land":1,"can_dock":1,"repair":167.0,"max_repair":167}
        self.db.blist[0] = {"active":0,"name":4,"damage":1.0,"bonus":12,"cost":40,"range":480,"arcs":27,"lock":0,"load":0,"recycle":6}
        self.db.blist[1] = {"active":0,"name":4,"damage":1.0,"bonus":12,"cost":40,"range":480,"arcs":43,"lock":0,"load":0,"recycle":6}
        self.db.blist[2] = {"active":0,"name":4,"damage":1.0,"bonus":12,"cost":40,"range":480,"arcs":29,"lock":0,"load":0,"recycle":6}
        self.db.blist[3] = {"active":0,"name":4,"damage":1.0,"bonus":12,"cost":40,"range":480,"arcs":45,"lock":0,"load":0,"recycle":6}
        self.db.blist[4] = {"active":0,"name":4,"damage":1.0,"bonus":12,"cost":40,"range":480,"arcs":23,"lock":0,"load":0,"recycle":6}
        self.db.blist[5] = {"active":0,"name":4,"damage":1.0,"bonus":12,"cost":40,"range":480,"arcs":39,"lock":0,"load":0,"recycle":6}
        self.db.mlist[0] = {"active":0,"name":9,"damage":1.0,"warhead":25,"cost":2,"range":320,"arcs":43,"lock":0,"load":0,"recycle":15}
        self.db.mlist[1] = {"active":0,"name":9,"damage":1.0,"warhead":25,"cost":2,"range":320,"arcs":43,"lock":0,"load":0,"recycle":15}
        self.db.mlist[2] = {"active":0,"name":9,"damage":1.0,"warhead":25,"cost":2,"range":320,"arcs":43,"lock":0,"load":0,"recycle":15}
        self.db.mlist[3] = {"active":0,"name":9,"damage":1.0,"warhead":25,"cost":2,"range":320,"arcs":43,"lock":0,"load":0,"recycle":15}
        self.db.cost = 1125142857
        create_ship_layout(self)

class Super_Cruiser_II(Generic_Ship):
    def at_object_creation(self):
        super().at_object_creation()
        self.db.move["ratio"] = 6.0
        self.db.main["gw"] = 108.0 
        self.db.aux["gw"] = 72.0
        self.db.batt["gw"]= 10.8
        self.db.beam["banks"] = 6
        self.db.beam["exist"] = 1
        self.db.missile["tubes"] = 6
        self.db.missile["exist"] = 1
        self.db.structure = {"type":1,"displacement":399060,"cargo_hold":39906,"cargo_mass":0.0,"superstructure":308.0,"max_structure":308,"has_landing_pad":1,"has_docking_bay":0,"can_land":1,"can_dock":1,"repair":308.0,"max_repair":308}
        self.db.blist[0] = {"active":0,"name":4,"damage":1.0,"bonus":15,"cost":50,"range":480,"arcs":27,"lock":0,"load":0,"recycle":6}
        self.db.blist[1] = {"active":0,"name":4,"damage":1.0,"bonus":15,"cost":50,"range":480,"arcs":43,"lock":0,"load":0,"recycle":6}
        self.db.blist[2] = {"active":0,"name":4,"damage":1.0,"bonus":15,"cost":50,"range":480,"arcs":29,"lock":0,"load":0,"recycle":6}
        self.db.blist[3] = {"active":0,"name":4,"damage":1.0,"bonus":15,"cost":50,"range":480,"arcs":45,"lock":0,"load":0,"recycle":6}
        self.db.blist[4] = {"active":0,"name":4,"damage":1.0,"bonus":15,"cost":50,"range":480,"arcs":23,"lock":0,"load":0,"recycle":6}
        self.db.blist[5] = {"active":0,"name":4,"damage":1.0,"bonus":15,"cost":50,"range":480,"arcs":39,"lock":0,"load":0,"recycle":6}
        self.db.mlist[0] = {"active":0,"name":9,"damage":1.0,"warhead":25,"cost":2,"range":320,"arcs":43,"lock":0,"load":0,"recycle":15}
        self.db.mlist[1] = {"active":0,"name":9,"damage":1.0,"warhead":25,"cost":2,"range":320,"arcs":43,"lock":0,"load":0,"recycle":15}
        self.db.mlist[2] = {"active":0,"name":9,"damage":1.0,"warhead":25,"cost":2,"range":320,"arcs":43,"lock":0,"load":0,"recycle":15}
        self.db.mlist[3] = {"active":0,"name":9,"damage":1.0,"warhead":25,"cost":2,"range":320,"arcs":43,"lock":0,"load":0,"recycle":15}
        self.db.mlist[4] = {"active":0,"name":9,"damage":1.0,"warhead":25,"cost":2,"range":320,"arcs":43,"lock":0,"load":0,"recycle":15}
        self.db.mlist[5] = {"active":0,"name":9,"damage":1.0,"warhead":25,"cost":2,"range":320,"arcs":43,"lock":0,"load":0,"recycle":15}
        self.db.cost = 2171520000
        create_ship_layout(self)


def create_ship_layout(self):
    #create the ship layout here
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
        if(console == "science"):
            ship_console.cmdset.add("commands.science.ScienceCmdSet", persistent=True)
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
    exit_teleport_bridge = create_object(Exit, key="Teleporter",aliases=["teleport"], location=self, destination=ship_teleport)
    exit_teleport = create_object(Exit, key="Bridge",aliases=["bridge"], location=ship_teleport, destination=self)

def create_fighter_layout(self):
        self.cmdset.add("commands.bridge.FighterBridgeCmdSet", persistent=True)
        self.cmdset.add("commands.engineering.EngineeringFighterCmdSet", persistent=True)
        self.cmdset.add("commands.tactical.TacticalCmdSet", persistent=True)
        self.cmdset.add("commands.helm.FighterCmdSet", persistent=True)

        ship_airlock = create_object(Airlock,key=self.key + "-airlock")
        ship_airlock.db.ship = self.key
        ship_airlock.tags.add("airlock",category=self.key)
        ship_airlock.tags.add("teleport",category=self.key)
        exit_airlock_bridge = create_object(Exit, key="Airlock",aliases=["airlock"], location=self, destination=ship_airlock)
        exit_airlock = create_object(Exit, key="Bridge",aliases=["bridge"], location=ship_airlock, destination=self)