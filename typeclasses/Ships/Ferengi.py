from evennia.utils.create import create_object
from typeclasses.airlock import Airlock
from typeclasses.exits import Exit
from typeclasses.rooms import Room, Console
from typeclasses.spaceship import Ferengi_Ship

class MBlanca(Ferengi_Ship):
    def at_object_creation(self):
        super().at_object_creation()
        self.db.move["ratio"] = 0.333333
        self.db.main["gw"] = 6.0 
        self.db.aux["gw"] = 18.0
        self.db.batt["gw"]= 0.6
        self.db.beam["banks"] = 2
        self.db.beam["exist"] = 1
        self.db.missile["tubes"] = 2
        self.db.missile["exist"] = 1
        self.db.structure = {"type":1,"displacement":4970,"cargo_hold":0,"cargo_mass":0.0,"superstructure":9.0,"max_structure":9,"has_landing_pad":0,"has_docking_bay":0,"can_land":1,"can_dock":0,"repair":9,"max_repair":9}
        arc_list = [59,59]
        for i in range(0,2):
            self.db.blist[i] = {"active":0,"name":11,"damage":1.0,"bonus":3,"cost":9,"range":420,"arcs":arc_list[i],"lock":0,"load":0,"recycle":6}
        for i in range(0,2):
            self.db.mlist[i] = {"active":0,"name":3,"damage":1.0,"warhead":10,"cost":1,"range":240,"arcs":43,"lock":0,"load":0,"recycle":15}
        self.db.cost = 77486
        create_fighter_layout(self)

class MBlanca_III(Ferengi_Ship):
    def at_object_creation(self):
        super().at_object_creation()
        self.db.move["ratio"] = 0.333333
        self.db.main["gw"] = 8.0 
        self.db.aux["gw"] = 18.0
        self.db.batt["gw"]= 0.8
        self.db.beam["banks"] = 2
        self.db.beam["exist"] = 1
        self.db.missile["tubes"] = 1
        self.db.missile["exist"] = 1
        self.db.structure = {"type":1,"displacement":4920,"cargo_hold":0,"cargo_mass":0.0,"superstructure":10.0,"max_structure":10,"has_landing_pad":0,"has_docking_bay":0,"can_land":1,"can_dock":0,"repair":10,"max_repair":10}
        arc_list = [59,59]
        for i in range(0,2):
            self.db.blist[i] = {"active":0,"name":11,"damage":1.0,"bonus":3,"cost":9,"range":420,"arcs":arc_list[i],"lock":0,"load":0,"recycle":6}
        self.db.mlist[0] = {"active":0,"name":3,"damage":1.0,"warhead":28,"cost":8,"range":360,"arcs":43,"lock":0,"load":0,"recycle":15}
        self.db.cost = 110414
        create_fighter_layout(self)


class Vortac_IV(Ferengi_Ship):
    def at_object_creation(self):
        super().at_object_creation()
        self.db.move["ratio"] = 4
        self.db.main["gw"] = 60.0 
        self.db.aux["gw"] = 20.0
        self.db.batt["gw"]= 6.0
        self.db.beam["banks"] = 8
        self.db.beam["exist"] = 1
        self.db.missile["tubes"] = 4
        self.db.missile["exist"] = 1
        self.db.structure = {"type":1,"displacement":208578,"cargo_hold":20857,"cargo_mass":0.0,"superstructure":107.0,"max_structure":107,"has_landing_pad":1,"has_docking_bay":0,"can_land":1,"can_dock":1,"repair":107,"max_repair":107}
        arc_list = [17,33,24,40,18,34,20,36]
        for i in range(0,2):
            self.db.blist[i] = {"active":0,"name":11,"damage":1.0,"bonus":12,"cost":32,"range":420,"arcs":arc_list[i],"lock":0,"load":0,"recycle":6}
        for i in range(2,8):
            self.db.blist[i] = {"active":0,"name":11,"damage":1.0,"bonus":6,"cost":16,"range":420,"arcs":arc_list[i],"lock":0,"load":0,"recycle":6}
        arc_list = [59,57,51,62]
        for i in range(0,4):
            self.db.mlist[i] = {"active":0,"name":3,"damage":1.0,"warhead":28,"cost":8,"range":360,"arcs":arc_list[i],"lock":0,"load":0,"recycle":15}
        self.db.cost = 509542856
        create_ship_layout(self)

class Vortac_V(Ferengi_Ship):
    def at_object_creation(self):
        super().at_object_creation()
        self.db.move["ratio"] = 4
        self.db.main["gw"] = 80.0 
        self.db.aux["gw"] = 20.0
        self.db.batt["gw"]= 8.0
        self.db.beam["banks"] = 8
        self.db.beam["exist"] = 1
        self.db.missile["tubes"] = 4
        self.db.missile["exist"] = 1
        self.db.structure = {"type":1,"displacement":208578,"cargo_hold":20857,"cargo_mass":0.0,"superstructure":107.0,"max_structure":107,"has_landing_pad":1,"has_docking_bay":0,"can_land":1,"can_dock":1,"repair":107,"max_repair":107}
        arc_list = [27,43,29,45,23,39,30,46]
        for i in range(0,2):
            self.db.blist[i] = {"active":0,"name":11,"damage":1.0,"bonus":12,"cost":32,"range":420,"arcs":arc_list[i],"lock":0,"load":0,"recycle":6}
        for i in range(2,8):
            self.db.blist[i] = {"active":0,"name":11,"damage":1.0,"bonus":6,"cost":16,"range":420,"arcs":arc_list[i],"lock":0,"load":0,"recycle":6}
        arc_list = [59,57,51,62]
        for i in range(0,4):
            self.db.mlist[i] = {"active":0,"name":3,"damage":1.0,"warhead":28,"cost":8,"range":360,"arcs":arc_list[i],"lock":0,"load":0,"recycle":15}
        self.db.cost = 550857
        create_ship_layout(self)

class Nagus(Ferengi_Ship):
    def at_object_creation(self):
        super().at_object_creation()
        self.db.move["ratio"] = 8
        self.db.main["gw"] = 160.0 
        self.db.aux["gw"] = 56.0
        self.db.batt["gw"]= 16.0
        self.db.beam["banks"] = 12
        self.db.beam["exist"] = 1
        self.db.missile["tubes"] = 12
        self.db.missile["exist"] = 1
        self.db.structure = {"type":1,"displacement":2698640,"cargo_hold":269864,"cargo_mass":0.0,"superstructure":417.0,"max_structure":417,"has_landing_pad":1,"has_docking_bay":0,"can_land":1,"can_dock":1,"repair":417,"max_repair":417}
        arc_list = [57,51,27,27,43,43,29,23,45,39,30,46]
        for i in range(0,2):
            self.db.blist[i] = {"active":0,"name":11,"damage":1.0,"bonus":30,"cost":100,"range":480,"arcs":arc_list[i],"lock":0,"load":0,"recycle":6}
        for i in range(2,12):
            self.db.blist[i] = {"active":0,"name":11,"damage":1.0,"bonus":9,"cost":24,"range":420,"arcs":arc_list[i],"lock":0,"load":0,"recycle":6}
        arc_list = [59,59,59,57,57,57,51,51,51,62,62,62]
        for i in range(0,12):
            self.db.mlist[i] = {"active":0,"name":3,"damage":1.0,"warhead":28,"cost":8,"range":360,"arcs":arc_list[i],"lock":0,"load":0,"recycle":15}
        self.db.cost = 4315234
        create_ship_layout(self)

class Miramar_IV(Ferengi_Ship):
    def at_object_creation(self):
        super().at_object_creation()
        self.db.move["ratio"] = 2
        self.db.main["gw"] = 40.0 
        self.db.aux["gw"] = 28.0
        self.db.batt["gw"]= 4.0
        self.db.beam["banks"] = 4
        self.db.beam["exist"] = 1
        self.db.missile["tubes"] = 1
        self.db.missile["exist"] = 1
        self.db.structure = {"type":1,"displacement":58760,"cargo_hold":5876,"cargo_mass":0.0,"superstructure":21.0,"max_structure":21,"has_landing_pad":1,"has_docking_bay":0,"can_land":1,"can_dock":1,"repair":21,"max_repair":21}
        arc_list = [59,61,55,62]
        self.db.blist[0] = {"active":0,"name":11,"damage":1.0,"bonus":6,"cost":16,"range":480,"arcs":arc_list[0],"lock":0,"load":0,"recycle":6}
        for i in range(1,4):
            self.db.blist[i] = {"active":0,"name":11,"damage":1.0,"bonus":3,"cost":8,"range":420,"arcs":arc_list[i],"lock":0,"load":0,"recycle":6}
        self.db.mlist[0] = {"active":0,"name":3,"damage":1.0,"warhead":28,"cost":8,"range":360,"arcs":59,"lock":0,"load":0,"recycle":15}
        self.db.cost = 83190
        create_ship_layout(self)

class Lathander_IV(Ferengi_Ship):
    def at_object_creation(self):
        super().at_object_creation()
        self.db.move["ratio"] = 3
        self.db.main["gw"] = 48.0 
        self.db.aux["gw"] = 28.0
        self.db.batt["gw"]= 4.8
        self.db.beam["banks"] = 4
        self.db.beam["exist"] = 1
        self.db.missile["tubes"] = 4
        self.db.missile["exist"] = 1
        self.db.structure = {"type":1,"displacement":119060,"cargo_hold":11906,"cargo_mass":0.0,"superstructure":49.0,"max_structure":49,"has_landing_pad":1,"has_docking_bay":0,"can_land":0,"can_dock":1,"repair":49,"max_repair":49}
        arc_list = [59,61,55,62]
        self.db.blist[0] = {"active":0,"name":11,"damage":1.0,"bonus":18,"cost":48,"range":420,"arcs":arc_list[0],"lock":0,"load":0,"recycle":6}
        for i in range(1,4):
            self.db.blist[i] = {"active":0,"name":11,"damage":1.0,"bonus":9,"cost":24,"range":420,"arcs":arc_list[i],"lock":0,"load":0,"recycle":6}
        arc_list = [57,57,51,51]
        for i in range(0,4):
            self.db.mlist[i] = {"active":0,"name":3,"damage":1.0,"warhead":28,"cost":8,"range":360,"arcs":arc_list[i],"lock":0,"load":0,"recycle":15}
        self.db.cost = 323384285
        create_ship_layout(self)

class Lathander_V(Ferengi_Ship):
    def at_object_creation(self):
        super().at_object_creation()
        self.db.move["ratio"] = 3
        self.db.main["gw"] = 60.0 
        self.db.aux["gw"] = 28.0
        self.db.batt["gw"]= 6.0
        self.db.beam["banks"] = 4
        self.db.beam["exist"] = 1
        self.db.missile["tubes"] = 4
        self.db.missile["exist"] = 1
        self.db.structure = {"type":1,"displacement":119060,"cargo_hold":11906,"cargo_mass":0.0,"superstructure":49.0,"max_structure":49,"has_landing_pad":1,"has_docking_bay":0,"can_land":0,"can_dock":1,"repair":49,"max_repair":49}
        arc_list = [59,61,55,62]
        self.db.blist[0] = {"active":0,"name":11,"damage":1.0,"bonus":18,"cost":48,"range":420,"arcs":arc_list[0],"lock":0,"load":0,"recycle":6}
        for i in range(1,4):
            self.db.blist[i] = {"active":0,"name":11,"damage":1.0,"bonus":9,"cost":24,"range":420,"arcs":arc_list[i],"lock":0,"load":0,"recycle":6}
        arc_list = [57,57,51,51]
        for i in range(0,4):
            self.db.mlist[i] = {"active":0,"name":3,"damage":1.0,"warhead":28,"cost":8,"range":360,"arcs":arc_list[i],"lock":0,"load":0,"recycle":15}
        self.db.cost = 350521
        create_ship_layout(self)

class Dkora_IV(Ferengi_Ship):
    def at_object_creation(self):
        super().at_object_creation()
        self.db.move["ratio"] = 6
        self.db.main["gw"] = 100.0 
        self.db.aux["gw"] = 28.0
        self.db.batt["gw"]= 10.0
        self.db.beam["banks"] = 8
        self.db.beam["exist"] = 1
        self.db.missile["tubes"] = 8
        self.db.missile["exist"] = 1
        self.db.structure = {"type":1,"displacement":499890,"cargo_hold":49989,"cargo_mass":0.0,"superstructure":310.0,"max_structure":310,"has_landing_pad":1,"has_docking_bay":0,"can_land":1,"can_dock":1,"repair":310,"max_repair":310}
        arc_list = [17,33,24,40,18,34,20,36]
        for i in range(0,2):
            self.db.blist[i] = {"active":0,"name":11,"damage":1.0,"bonus":18,"cost":48,"range":420,"arcs":arc_list[i],"lock":0,"load":0,"recycle":6}
        for i in range(2,8):
            self.db.blist[i] = {"active":0,"name":11,"damage":1.0,"bonus":9,"cost":24,"range":420,"arcs":arc_list[i],"lock":0,"load":0,"recycle":6}
        arc_list = [59,59,57,57,51,51,62,62]
        for i in range(0,8):
            self.db.mlist[i] = {"active":0,"name":3,"damage":1.0,"warhead":28,"cost":8,"range":360,"arcs":arc_list[i],"lock":0,"load":0,"recycle":15}
        self.db.cost = 1772960
        create_ship_layout(self)

class Dkora_V(Ferengi_Ship):
    def at_object_creation(self):
        super().at_object_creation()
        self.db.move["ratio"] = 6
        self.db.main["gw"] = 120.0 
        self.db.aux["gw"] = 28.0
        self.db.batt["gw"]= 12.0
        self.db.beam["banks"] = 8
        self.db.beam["exist"] = 1
        self.db.missile["tubes"] = 8
        self.db.missile["exist"] = 1
        self.db.structure = {"type":1,"displacement":499890,"cargo_hold":49989,"cargo_mass":0.0,"superstructure":310.0,"max_structure":310,"has_landing_pad":1,"has_docking_bay":0,"can_land":1,"can_dock":1,"repair":310,"max_repair":310}
        arc_list = [17,33,24,40,18,34,20,36]
        for i in range(0,2):
            self.db.blist[i] = {"active":0,"name":11,"damage":1.0,"bonus":18,"cost":48,"range":420,"arcs":arc_list[i],"lock":0,"load":0,"recycle":6}
        for i in range(2,8):
            self.db.blist[i] = {"active":0,"name":11,"damage":1.0,"bonus":9,"cost":24,"range":420,"arcs":arc_list[i],"lock":0,"load":0,"recycle":6}
        arc_list = [59,59,57,57,51,51,62,62]
        for i in range(0,8):
            self.db.mlist[i] = {"active":0,"name":3,"damage":1.0,"warhead":28,"cost":8,"range":360,"arcs":arc_list[i],"lock":0,"load":0,"recycle":15}
        self.db.cost = 1818189
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
            ship_console.tags.add("damage",category=self.key)
        if(console == "tactical"):
            ship_console.cmdset.add("commands.tactical.TacticalCmdSet", persistent=True)
        if(console == "helm"):
            ship_console.cmdset.add("commands.helm.HelmCmdSet", persistent=True)
            ship_console.tags.add("damage",category=self.key)
        if(console == "science"):
            ship_console.cmdset.add("commands.science.ScienceCmdSet", persistent=True)
        if(console == "operation"):
            ship_console.cmdset.add("commands.operation.OperationCmdSet", persistent=True)
            ship_console.tags.add("damage",category=self.key)
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
        self.tags.add("damage",category=self.key)

        ship_airlock = create_object(Airlock,key=self.key + "-airlock")
        ship_airlock.db.ship = self.key
        ship_airlock.tags.add("airlock",category=self.key)
        ship_airlock.tags.add("teleport",category=self.key)
        exit_airlock_bridge = create_object(Exit, key="Airlock",aliases=["airlock"], location=self, destination=ship_airlock)
        exit_airlock = create_object(Exit, key="Bridge",aliases=["bridge"], location=ship_airlock, destination=self)