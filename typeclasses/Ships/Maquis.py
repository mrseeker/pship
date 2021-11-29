from evennia.utils.create import create_object
from typeclasses.airlock import Airlock
from typeclasses.exits import Exit
from typeclasses.rooms import Room
from typeclasses.spaceship import Console, Maquis_Ship

class Opus_Mach_II(Maquis_Ship):
    def at_object_creation(self):
        super().at_object_creation()
        self.db.move["ratio"] = 0.5
        self.db.main["gw"] = 12.0 
        self.db.aux["gw"] = 8.0
        self.db.batt["gw"]= 1.2
        self.db.beam["banks"] = 4
        self.db.beam["exist"] = 1
        self.db.missile["tubes"] = 2
        self.db.missile["exist"] = 1
        self.db.structure = {"type":1,"displacement":14165,"cargo_hold":0,"cargo_mass":0.0,"superstructure":21.0,"max_structure":21,"has_landing_pad":0,"has_docking_bay":0,"can_land":1,"can_dock":0,"repair":21,"max_repair":21}
        arc_list = [57,57,51,51]
        for i in range(0,4):
            self.db.blist[i] = {"active":0,"name":1,"damage":1.0,"bonus":3,"cost":10,"range":480,"arcs":arc_list[i],"lock":0,"load":0,"recycle":6}
        arc_list = [57,51]
        for i in range(0,2):
            self.db.mlist[i] = {"active":0,"name":9,"damage":1.0,"warhead":25,"cost":2,"range":320,"arcs":arc_list[i],"lock":0,"load":0,"recycle":15}
        self.db.cost = 208257
        create_fighter_layout(self)

class Opus_Mach_IIa(Maquis_Ship):
    def at_object_creation(self):
        super().at_object_creation()
        self.db.move["ratio"] = 0.5
        self.db.main["gw"] = 12.0 
        self.db.aux["gw"] = 8.0
        self.db.batt["gw"]= 1.2
        self.db.beam["banks"] = 4
        self.db.beam["exist"] = 1
        self.db.missile["tubes"] = 2
        self.db.missile["exist"] = 1
        self.db.structure = {"type":1,"displacement":14165,"cargo_hold":0,"cargo_mass":0.0,"superstructure":21.0,"max_structure":21,"has_landing_pad":0,"has_docking_bay":0,"can_land":1,"can_dock":0,"repair":21,"max_repair":21}
        arc_list = [57,57,51,51]
        for i in range(0,4):
            self.db.blist[i] = {"active":0,"name":1,"damage":1.0,"bonus":3,"cost":10,"range":480,"arcs":arc_list[i],"lock":0,"load":0,"recycle":6}
        arc_list = [57,51]
        for i in range(0,2):
            self.db.mlist[i] = {"active":0,"name":9,"damage":1.0,"warhead":25,"cost":2,"range":320,"arcs":arc_list[i],"lock":0,"load":0,"recycle":15}
        self.db.cost = 208257
        create_fighter_layout(self)

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