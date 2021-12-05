from evennia.utils.create import create_object
from typeclasses.airlock import Airlock
from typeclasses.exits import Exit
from typeclasses.rooms import Room, Console
from typeclasses.spaceship import Bajoran_Ship

class Prophesy_II(Bajoran_Ship):
    def at_object_creation(self):
        super().at_object_creation()
        self.db.move["ratio"] = 5.0
        self.db.main["gw"] = 96.0 
        self.db.aux["gw"] = 40.0
        self.db.batt["gw"]= 9.6
        self.db.beam["banks"] = 8
        self.db.beam["exist"] = 1
        self.db.missile["tubes"] = 10
        self.db.missile["exist"] = 1
        self.db.structure = {"type":1,"displacement":248710,"cargo_hold":24871,"cargo_mass":0.0,"superstructure":202.0,"max_structure":202,"has_landing_pad":1,"has_docking_bay":0,"can_land":1,"can_dock":1,"repair":202,"max_repair":202}
        arc_list = [27,43,57,51,30,46,60,54]
        for i in range(0,4):
            self.db.blist[i] = {"active":0,"name":4,"damage":1.0,"bonus":18,"cost":60,"range":480,"arcs":arc_list[i],"lock":0,"load":0,"recycle":6}
        for i in range(4,8):
            self.db.blist[i] = {"active":0,"name":4,"damage":1.0,"bonus":6,"cost":20,"range":480,"arcs":arc_list[i],"lock":0,"load":0,"recycle":6}
        arc_list = [57,57,57,57,51,51,51,51,60,54]
        for i in range(0,10):
            self.db.mlist[i] = {"active":0,"name":9,"damage":1.0,"warhead":25,"cost":1,"range":320,"arcs":arc_list[i],"lock":0,"load":0,"recycle":15}
        self.db.cost = 2355296000
        create_ship_layout(self)

class Akorem_II(Bajoran_Ship):
    def at_object_creation(self):
        super().at_object_creation()
        self.db.move["ratio"] = 2.0
        self.db.main["gw"] = 39.0 
        self.db.aux["gw"] = 20.0
        self.db.batt["gw"]= 3.9
        self.db.beam["banks"] = 4
        self.db.beam["exist"] = 1
        self.db.missile["tubes"] = 4
        self.db.missile["exist"] = 1
        self.db.structure = {"type":1,"displacement":59948,"cargo_hold":5994,"cargo_mass":0.0,"superstructure":53.0,"max_structure":53,"has_landing_pad":1,"has_docking_bay":0,"can_land":1,"can_dock":1,"repair":53,"max_repair":53}
        arc_list = [57,51,60,54]
        for i in range(0,2):
            self.db.blist[i] = {"active":0,"name":4,"damage":1.0,"bonus":12,"cost":40,"range":480,"arcs":arc_list[i],"lock":0,"load":0,"recycle":6}
        for i in range(2,4):
            self.db.blist[i] = {"active":0,"name":4,"damage":1.0,"bonus":6,"cost":20,"range":480,"arcs":arc_list[i],"lock":0,"load":0,"recycle":6}
        arc_list = [57,51,60,54]
        for i in range(0,10):
            self.db.mlist[i] = {"active":0,"name":9,"damage":1.0,"warhead":25,"cost":1,"range":320,"arcs":arc_list[i],"lock":0,"load":0,"recycle":15}
        self.db.cost = 520611428
        create_ship_layout(self)

class Krim_II(Bajoran_Ship):
    def at_object_creation(self):
        super().at_object_creation()
        self.db.move["ratio"] = 3.0
        self.db.main["gw"] = 60.0 
        self.db.aux["gw"] = 20.0
        self.db.batt["gw"]= 6.0
        self.db.beam["banks"] = 8
        self.db.beam["exist"] = 1
        self.db.missile["tubes"] = 6
        self.db.missile["exist"] = 1
        self.db.cloak = {"version":0,"cost":60,"freq":0.0,"exist":1,"active":0,"damage":1.0}
        self.db.structure = {"type":1,"displacement":59948,"cargo_hold":5994,"cargo_mass":0.0,"superstructure":53.0,"max_structure":53,"has_landing_pad":1,"has_docking_bay":0,"can_land":1,"can_dock":1,"repair":53,"max_repair":53}
        arc_list = [27,43,57,51,30,46,60,54]
        for i in range(0,4):
            self.db.blist[i] = {"active":0,"name":4,"damage":1.0,"bonus":12,"cost":40,"range":480,"arcs":arc_list[i],"lock":0,"load":0,"recycle":6}
        for i in range(4,8):
            self.db.blist[i] = {"active":0,"name":4,"damage":1.0,"bonus":6,"cost":20,"range":480,"arcs":arc_list[i],"lock":0,"load":0,"recycle":6}
        arc_list = [57,51,30,46,60,54]
        for i in range(0,10):
            self.db.mlist[i] = {"active":0,"name":9,"damage":1.0,"warhead":25,"cost":1,"range":320,"arcs":arc_list[i],"lock":0,"load":0,"recycle":15}
        self.db.cost = 1134628572
        create_ship_layout(self)

def create_ship_layout(self):
    #create the ship layout here
    self.cmdset.add("commands.bridge.BridgeCmdSet", persistent=True)
    self.tags.add("bridge",category=self.key)
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
        self.tags.add("bridge",category=self.key)

        ship_airlock = create_object(Airlock,key=self.key + "-airlock")
        ship_airlock.db.ship = self.key
        ship_airlock.tags.add("airlock",category=self.key)
        ship_airlock.tags.add("teleport",category=self.key)
        exit_airlock_bridge = create_object(Exit, key="Airlock",aliases=["airlock"], location=self, destination=ship_airlock)
        exit_airlock = create_object(Exit, key="Bridge",aliases=["bridge"], location=ship_airlock, destination=self)