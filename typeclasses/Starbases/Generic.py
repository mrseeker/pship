from evennia.utils.create import create_object
from typeclasses.airlock import Airlock
from typeclasses.exits import Exit
from typeclasses.rooms import Room,Console
from typeclasses.spacebase import Generic_SpaceBase

class Outpost_II(Generic_SpaceBase):
    def at_object_creation(self):
        super().at_object_creation()
        self.db.move["ratio"] = 800.0
        self.db.main["gw"] = 200.0 
        self.db.aux["gw"] = 100.0
        self.db.batt["gw"]= 20.0
        self.db.beam["banks"] = 8
        self.db.beam["exist"] = 1
        self.db.missile["tubes"] = 16
        self.db.missile["exist"] = 1
        self.db.structure = {"type":2,"displacement":4989900,"cargo_hold":3633000,"cargo_mass":0.0,"superstructure":318.0,"max_structure":318,"has_landing_pad":1,"has_docking_bay":1,"can_land":0,"can_dock":0,"repair":318.0,"max_repair":318}
        arc_list = [27,43,29,45,23,39,30,46]
        for i in range(0,8):
            self.db.blist[i] = {"active":0,"name":3,"damage":1.0,"bonus":6,"cost":20,"range":480,"arcs":arc_list[i],"lock":0,"load":0,"recycle":6}
        arc_list = [27,27,43,43,29,29,45,45,23,23,39,39,30,30,46,46]
        for i in range(0,16):
            self.db.mlist[i] = {"active":0,"name":9,"damage":1.0,"warhead":25,"cost":1,"range":320,"arcs":arc_list[i],"lock":0,"load":0,"recycle":15}
        self.db.cost = 1820868570
        create_base_layout(self)

class Outpost_IIb(Generic_SpaceBase):
    def at_object_creation(self):
        super().at_object_creation()
        self.db.move["ratio"] = 200.0
        self.db.main["gw"] = 200.0 
        self.db.aux["gw"] = 200.0
        self.db.batt["gw"]= 200.0
        self.db.beam["banks"] = 2
        self.db.beam["exist"] = 1
        self.db.missile["tubes"] = 10
        self.db.missile["exist"] = 1
        self.db.structure = {"type":2,"displacement":10000000,"cargo_hold":1000000,"cargo_mass":0.0,"superstructure":125.0,"max_structure":125,"has_landing_pad":1,"has_docking_bay":1,"can_land":0,"can_dock":0,"repair":125.0,"max_repair":125}
        arc_list = [31,47]
        for i in range(0,2):
            self.db.blist[i] = {"active":0,"name":4,"damage":1.0,"bonus":45,"cost":150,"range":1000,"arcs":arc_list[i],"lock":0,"load":0,"recycle":6}
        arc_list = [31,31,31,31,31,47,47,47,47,47]
        for i in range(0,10):
            self.db.mlist[i] = {"active":0,"name":9,"damage":1.0,"warhead":25,"cost":1,"range":320,"arcs":arc_list[i],"lock":0,"load":0,"recycle":15}
        self.db.cost = 994886
        create_base_layout(self)

class Station_II(Generic_SpaceBase):
    def at_object_creation(self):
        super().at_object_creation()
        self.db.move["ratio"] = 1000.0
        self.db.main["gw"] = 200.0 
        self.db.aux["gw"] = 200.0
        self.db.batt["gw"]= 20.0
        self.db.beam["banks"] = 8
        self.db.beam["exist"] = 1
        self.db.missile["tubes"] = 16
        self.db.missile["exist"] = 1
        self.db.structure = {"type":2,"displacement":9997900,"cargo_hold":8343000,"cargo_mass":0.0,"superstructure":709.0,"max_structure":709,"has_landing_pad":1,"has_docking_bay":1,"can_land":0,"can_dock":0,"repair":709.0,"max_repair":709}
        arc_list = [27,43,29,45,23,39,30,46]
        for i in range(0,8):
            self.db.blist[i] = {"active":0,"name":3,"damage":1.0,"bonus":6,"cost":80,"range":480,"arcs":arc_list[i],"lock":0,"load":0,"recycle":6}
        arc_list = [27,27,43,43,29,29,45,45,23,23,39,39,30,30,46,46]
        for i in range(0,16):
            self.db.mlist[i] = {"active":0,"name":9,"damage":1.0,"warhead":25,"cost":1,"range":320,"arcs":arc_list[i],"lock":0,"load":0,"recycle":15}
        self.db.cost = 9282816000
        create_base_layout(self)

class Station_IIb(Generic_SpaceBase):
    def at_object_creation(self):
        super().at_object_creation()
        self.db.move["ratio"] = 500.0
        self.db.main["gw"] = 500.0 
        self.db.aux["gw"] = 500.0
        self.db.batt["gw"]= 500.0
        self.db.beam["banks"] = 4
        self.db.beam["exist"] = 1
        self.db.missile["tubes"] = 20
        self.db.missile["exist"] = 1
        self.db.structure = {"type":2,"displacement":100000000,"cargo_hold":10000000,"cargo_mass":0.0,"superstructure":500.0,"max_structure":500,"has_landing_pad":1,"has_docking_bay":1,"can_land":0,"can_dock":0,"repair":500.0,"max_repair":500}
        arc_list = [31,31,47,47]
        for i in range(0,4):
            self.db.blist[i] = {"active":0,"name":4,"damage":1.0,"bonus":45,"cost":150,"range":1000,"arcs":arc_list[i],"lock":0,"load":0,"recycle":6}
        arc_list = [31,31,31,31,31,31,31,31,31,31,47,47,47,47,47,47,47,47,47,47]
        for i in range(0,20):
            self.db.mlist[i] = {"active":0,"name":9,"damage":1.0,"warhead":25,"cost":1,"range":320,"arcs":arc_list[i],"lock":0,"load":0,"recycle":15}
        self.db.cost = 7100485
        create_base_layout(self)

class Starbase_II(Generic_SpaceBase):
    def at_object_creation(self):
        super().at_object_creation()
        self.db.move["ratio"] = 4000.0
        self.db.main["gw"] = 1200.0 
        self.db.aux["gw"] = 400.0
        self.db.batt["gw"]= 120.0
        self.db.beam["banks"] = 8
        self.db.beam["exist"] = 1
        self.db.missile["tubes"] = 16
        self.db.missile["exist"] = 1
        self.db.structure = {"type":2,"displacement":39986900,"cargo_hold":33312000,"cargo_mass":0.0,"superstructure":2414.0,"max_structure":2414,"has_landing_pad":1,"has_docking_bay":1,"can_land":0,"can_dock":0,"repair":2414.0,"max_repair":2414}
        arc_list = [27,43,29,45,23,39,30,46]
        for i in range(0,8):
            self.db.blist[i] = {"active":0,"name":3,"damage":1.0,"bonus":24,"cost":80,"range":480,"arcs":arc_list[i],"lock":0,"load":0,"recycle":6}
        arc_list = [27,27,43,43,29,29,45,45,23,23,39,39,30,30,46,46]
        for i in range(0,16):
            self.db.mlist[i] = {"active":0,"name":9,"damage":1.0,"warhead":25,"cost":1,"range":320,"arcs":arc_list[i],"lock":0,"load":0,"recycle":15}
        self.db.cost = 30834016000
        create_base_layout(self)

class Starbase_IIb(Generic_SpaceBase):
    def at_object_creation(self):
        super().at_object_creation()
        self.db.move["ratio"] = 1000.0
        self.db.main["gw"] = 1000.0 
        self.db.aux["gw"] = 1000.0
        self.db.batt["gw"]= 1000.0
        self.db.beam["banks"] = 4
        self.db.beam["exist"] = 1
        self.db.missile["tubes"] = 20
        self.db.missile["exist"] = 1
        self.db.structure = {"type":2,"displacement":1000000000 ,"cargo_hold":100000000 ,"cargo_mass":0.0,"superstructure":2000.0,"max_structure":2000,"has_landing_pad":1,"has_docking_bay":1,"can_land":0,"can_dock":0,"repair":2000.0,"max_repair":2000}
        arc_list = [31,31,47,47]
        for i in range(0,4):
            self.db.blist[i] = {"active":0,"name":4,"damage":1.0,"bonus":45,"cost":150,"range":1000,"arcs":arc_list[i],"lock":0,"load":0,"recycle":6}
        arc_list = [31,31,31,31,31,31,31,31,31,31,47,47,47,47,47,47,47,47,47,47]
        for i in range(0,20):
            self.db.mlist[i] = {"active":0,"name":9,"damage":1.0,"warhead":25,"cost":1,"range":320,"arcs":arc_list[i],"lock":0,"load":0,"recycle":15}
        self.db.cost = 27543343000
        create_base_layout(self)


def create_base_layout(self):
    #create the base layout here
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
