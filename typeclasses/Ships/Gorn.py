from evennia.utils.create import create_object
from typeclasses.airlock import Airlock
from typeclasses.exits import Exit
from typeclasses.rooms import Room, Console
from typeclasses.spaceship import Gorn_Ship

class Allosaurus(Gorn_Ship):
    def at_object_creation(self):
        super().at_object_creation()


class Stegosaurus(Gorn_Ship):
    def at_object_creation(self):
        super().at_object_creation()
        self.db.move["ratio"] = 2
        self.db.main["gw"] = 40.0 
        self.db.aux["gw"] = 12.0
        self.db.batt["gw"]= 4.0
        self.db.beam["banks"] = 4
        self.db.beam["exist"] = 1
        self.db.missile["exist"] = 0
        self.db.tech["sensors"] = 2.2
        self.db.structure = {"type":1,"displacement":48718,"cargo_hold":4871,"cargo_mass":0.0,"superstructure":33.0,"max_structure":33,"has_landing_pad":1,"has_docking_bay":0,"can_land":0,"can_dock":1,"repair":33.0,"max_repair":33}
        arc_list = [31,47,61,55]
        for i in range(0,4):
            self.db.blist[i] = {"active":0,"name":9,"damage":1.0,"bonus":6,"cost":20,"range":480,"arcs":arc_list[i],"lock":0,"load":0,"recycle":6}
        arc_list = [57,51]
        for i in range(0,2):
            self.db.mlist[i] = {"active":0,"name":9,"damage":1.0,"warhead":25,"cost":2,"range":320,"arcs":43,"lock":0,"load":0,"recycle":15}
        self.db.cost = 224285
        create_fighter_layout(self)

class Carnosaurus(Gorn_Ship):
    def at_object_creation(self):
        super().at_object_creation()
        self.db.move["ratio"] = 2
        self.db.main["gw"] = 40.0 
        self.db.aux["gw"] = 12.0
        self.db.batt["gw"]= 4.0
        self.db.beam["banks"] = 4
        self.db.beam["exist"] = 1
        self.db.missile["exist"] = 1
        self.db.missile["banks"] = 1
        self.db.structure = {"type":1,"displacement":48958,"cargo_hold":4895,"cargo_mass":0.0,"superstructure":43.0,"max_structure":43,"has_landing_pad":1,"has_docking_bay":0,"can_land":0,"can_dock":1,"repair":43.0,"max_repair":43}
        arc_list = [31,47,61,55]
        for i in range(0,4):
            self.db.blist[i] = {"active":0,"name":9,"damage":1.0,"bonus":6,"cost":20,"range":480,"arcs":arc_list[i],"lock":0,"load":0,"recycle":6}
        self.db.mlist[0] = {"active":0,"name":3,"damage":1.0,"warhead":96,"cost":45,"range":280,"arcs":43,"lock":0,"load":0,"recycle":15}
        self.db.cost = 283661
        create_fighter_layout(self)

class Velociraptor(Gorn_Ship):
    def at_object_creation(self):
        super().at_object_creation()
        self.db.move["ratio"] = 1
        self.db.main["gw"] = 24.0 
        self.db.aux["gw"] = 6.0
        self.db.batt["gw"]= 2.4
        self.db.beam["banks"] = 4
        self.db.beam["exist"] = 1
        self.db.missile["exist"] = 1
        self.db.missile["tubes"] = 1
        self.db.structure = {"type":1,"displacement":23844,"cargo_hold":2384,"cargo_mass":0.0,"superstructure":39.0,"max_structure":39,"has_landing_pad":1,"has_docking_bay":0,"can_land":1,"can_dock":1,"repair":39.0,"max_repair":39}
        arc_list = [31,47,61,55]
        for i in range(0,4):
            self.db.blist[i] = {"active":0,"name":4,"damage":1.0,"bonus":6,"cost":20,"range":480,"arcs":arc_list[i],"lock":0,"load":0,"recycle":6}
        self.db.mlist[0] = {"active":0,"name":3,"damage":1.0,"warhead":96,"cost":45,"range":280,"arcs":59,"lock":0,"load":0,"recycle":15}
        self.db.cost = 304044
        create_ship_layout(self)

class Apatosaurus(Gorn_Ship):
    def at_object_creation(self):
        super().at_object_creation()
        self.db.move["ratio"] = 8
        self.db.main["gw"] = 160.0 
        self.db.aux["gw"] = 48.0
        self.db.batt["gw"]= 16.0
        self.db.beam["banks"] = 8
        self.db.beam["exist"] = 1
        self.db.missile["exist"] = 1
        self.db.missile["tubes"] = 6
        self.db.structure = {"type":1,"displacement":4598514,"cargo_hold":459851,"cargo_mass":0.0,"superstructure":382.0,"max_structure":382,"has_landing_pad":1,"has_docking_bay":0,"can_land":0,"can_dock":1,"repair":382.0,"max_repair":382}
        arc_list = [57,51,29,45,23,39,60,54]
        for i in range(0,8):
            self.db.blist[i] = {"active":0,"name":9,"damage":1.0,"bonus":15,"cost":50,"range":480,"arcs":arc_list[i],"lock":0,"load":0,"recycle":6}
        arc_list = [43,57,51,60,54,46]
        self.db.mlist[0] = {"active":0,"name":3,"damage":1.0,"warhead":160,"cost":75,"range":280,"arcs":arc_list[0],"lock":0,"load":0,"recycle":15}
        for i in range(1,6):
            self.db.mlist[i] = {"active":0,"name":3,"damage":1.0,"warhead":64,"cost":30,"range":280,"arcs":arc_list[i],"lock":0,"load":0,"recycle":15}
        self.db.cost = 4297385
        create_ship_layout(self)

class Megalosaurus(Gorn_Ship):
    def at_object_creation(self):
        super().at_object_creation()
        self.db.move["ratio"] = 3
        self.db.main["gw"] = 60.0 
        self.db.aux["gw"] = 18.0
        self.db.batt["gw"]= 6.0
        self.db.beam["banks"] = 6
        self.db.beam["exist"] = 1
        self.db.missile["exist"] = 1
        self.db.missile["tubes"] = 3
        self.db.structure = {"type":1,"displacement":100154,"cargo_hold":10015,"cargo_mass":0.0,"superstructure":60.0,"max_structure":60,"has_landing_pad":1,"has_docking_bay":0,"can_land":0,"can_dock":1,"repair":60.0,"max_repair":60}
        arc_list = [57,51,29,45,23,39]
        for i in range(0,6):
            self.db.blist[i] = {"active":0,"name":9,"damage":1.0,"bonus":6,"cost":20,"range":480,"arcs":arc_list[i],"lock":0,"load":0,"recycle":6}
        arc_list = [43,57,51]
        self.db.mlist[0] = {"active":0,"name":3,"damage":1.0,"warhead":128,"cost":60,"range":280,"arcs":arc_list[0],"lock":0,"load":0,"recycle":15}
        for i in range(1,3):
            self.db.mlist[i] = {"active":0,"name":3,"damage":1.0,"warhead":32,"cost":15,"range":280,"arcs":arc_list[i],"lock":0,"load":0,"recycle":15}
        self.db.cost = 512571
        create_ship_layout(self)

class Allosaurus(Gorn_Ship):
    def at_object_creation(self):
        super().at_object_creation()
        self.db.move["ratio"] = 4
        self.db.main["gw"] = 80.0 
        self.db.aux["gw"] = 24.0
        self.db.batt["gw"]= 8.0
        self.db.beam["banks"] = 8
        self.db.beam["exist"] = 1
        self.db.missile["exist"] = 1
        self.db.missile["tubes"] = 3
        self.db.structure = {"type":1,"displacement":198582,"cargo_hold":19858,"cargo_mass":0.0,"superstructure":114.0,"max_structure":114,"has_landing_pad":1,"has_docking_bay":0,"can_land":0,"can_dock":1,"repair":114.0,"max_repair":114}
        arc_list = [57,51,29,45,23,39,60,54]
        for i in range(0,8):
            self.db.blist[i] = {"active":0,"name":9,"damage":1.0,"bonus":6,"cost":20,"range":480,"arcs":arc_list[i],"lock":0,"load":0,"recycle":6}
        arc_list = [43,57,51]
        self.db.mlist[0] = {"active":0,"name":3,"damage":1.0,"warhead":128,"cost":60,"range":280,"arcs":arc_list[0],"lock":0,"load":0,"recycle":15}
        for i in range(1,3):
            self.db.mlist[i] = {"active":0,"name":3,"damage":1.0,"warhead":32,"cost":15,"range":280,"arcs":arc_list[i],"lock":0,"load":0,"recycle":15}
        self.db.cost = 808520
        create_ship_layout(self)


class Triceratops(Gorn_Ship):
    def at_object_creation(self):
        super().at_object_creation()
        self.db.move["ratio"] = 4
        self.db.main["gw"] = 80.0 
        self.db.aux["gw"] = 24.0
        self.db.batt["gw"]= 8.0
        self.db.beam["banks"] = 8
        self.db.beam["exist"] = 1
        self.db.missile["exist"] = 1
        self.db.missile["tubes"] = 3
        self.db.structure = {"type":1,"displacement":298722,"cargo_hold":29872,"cargo_mass":0.0,"superstructure":205.0,"max_structure":205,"has_landing_pad":1,"has_docking_bay":0,"can_land":0,"can_dock":1,"repair":205.0,"max_repair":205}
        arc_list = [57,51,29,45,23,39,60,54]
        for i in range(0,8):
            self.db.blist[i] = {"active":0,"name":4,"damage":1.0,"bonus":9,"cost":30,"range":480,"arcs":arc_list[i],"lock":0,"load":0,"recycle":6}
        arc_list = [43,57,51]
        self.db.mlist[0] = {"active":0,"name":3,"damage":1.0,"warhead":160,"cost":75,"range":280,"arcs":arc_list[0],"lock":0,"load":0,"recycle":15}
        for i in range(1,3):
            self.db.mlist[i] = {"active":0,"name":3,"damage":1.0,"warhead":64,"cost":30,"range":280,"arcs":arc_list[i],"lock":0,"load":0,"recycle":15}
        self.db.cost = 1676490
        create_ship_layout(self)


class Tyrannosaurus(Gorn_Ship):
    def at_object_creation(self):
        super().at_object_creation()
        self.db.move["ratio"] = 5
        self.db.main["gw"] = 100.0 
        self.db.aux["gw"] = 30.0
        self.db.batt["gw"]= 10.0
        self.db.beam["banks"] = 8
        self.db.beam["exist"] = 1
        self.db.missile["exist"] = 1
        self.db.missile["tubes"] = 5
        self.db.structure = {"type":1,"displacement":498830,"cargo_hold":498830,"cargo_mass":0.0,"superstructure":339.0,"max_structure":339,"has_landing_pad":1,"has_docking_bay":0,"can_land":0,"can_dock":1,"repair":339.0,"max_repair":339}
        arc_list = [57,51,29,45,23,39,60,54]
        for i in range(0,8):
            self.db.blist[i] = {"active":0,"name":4,"damage":1.0,"bonus":12,"cost":40,"range":480,"arcs":arc_list[i],"lock":0,"load":0,"recycle":6}
        arc_list = [43,57,51,60,54]
        self.db.mlist[0] = {"active":0,"name":3,"damage":1.0,"warhead":160,"cost":75,"range":280,"arcs":arc_list[0],"lock":0,"load":0,"recycle":15}
        for i in range(1,3):
            self.db.mlist[i] = {"active":0,"name":3,"damage":1.0,"warhead":64,"cost":30,"range":280,"arcs":arc_list[i],"lock":0,"load":0,"recycle":15}
        for i in range(3,5):
            self.db.mlist[i] = {"active":0,"name":3,"damage":1.0,"warhead":32,"cost":15,"range":280,"arcs":arc_list[i],"lock":0,"load":0,"recycle":15}
        
        self.db.cost = 2998917
        create_ship_layout(self)

class Godzilla(Gorn_Ship):
    def at_object_creation(self):
        super().at_object_creation()
        self.db.move["ratio"] = 10
        self.db.main["gw"] = 200.0 
        self.db.aux["gw"] = 60.0
        self.db.batt["gw"]= 20.0
        self.db.beam["banks"] = 8
        self.db.beam["exist"] = 1
        self.db.missile["exist"] = 1
        self.db.missile["tubes"] = 6
        self.db.structure = {"type":1,"displacement":8799110,"cargo_hold":879911,"cargo_mass":0.0,"superstructure":509.0,"max_structure":509,"has_landing_pad":1,"has_docking_bay":0,"can_land":0,"can_dock":1,"repair":509.0,"max_repair":509}
        arc_list = [57,51,29,45,23,39,60,54]
        for i in range(0,8):
            self.db.blist[i] = {"active":0,"name":9,"damage":1.0,"bonus":18,"cost":60,"range":480,"arcs":arc_list[i],"lock":0,"load":0,"recycle":6}
        arc_list = [43,57,51,60,54,46]
        self.db.mlist[0] = {"active":0,"name":3,"damage":1.0,"warhead":160,"cost":75,"range":280,"arcs":arc_list[0],"lock":0,"load":0,"recycle":15}
        for i in range(1,5):
            self.db.mlist[i] = {"active":0,"name":3,"damage":1.0,"warhead":64,"cost":30,"range":280,"arcs":arc_list[i],"lock":0,"load":0,"recycle":15}
        self.db.mlist[5] = {"active":0,"name":3,"damage":1.0,"warhead":160,"cost":75,"range":280,"arcs":arc_list[5],"lock":0,"load":0,"recycle":15}
        self.db.cost = 6451174
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