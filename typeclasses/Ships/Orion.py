from evennia.utils.create import create_object
from typeclasses.airlock import Airlock
from typeclasses.exits import Exit
from typeclasses.rooms import Room, Console
from typeclasses.spaceship import Maquis_Ship, Orion_Ship

class Medium_Cruiser_IIIa(Orion_Ship):
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
        arc_list = [41,35,31,47]
        for i in range(0,2):
            self.db.blist[i] = {"active":0,"name":3,"damage":1.0,"bonus":20,"cost":30,"range":260,"arcs":arc_list[i],"lock":0,"load":0,"recycle":6}
        for i in range(2,4):
            self.db.blist[i] = {"active":0,"name":4,"damage":1.0,"bonus":18,"cost":60,"range":480,"arcs":arc_list[i],"lock":0,"load":0,"recycle":6}
        arc_list = [27,27,27,27,30,30]
        for i in range(0,6):
            self.db.mlist[i] = {"active":0,"name":9,"damage":1.0,"warhead":25,"cost":2,"range":320,"arcs":arc_list[i],"lock":0,"load":0,"recycle":15}
        self.db.cost = 1022109
        create_ship_layout(self)

class Heavy_Cruiser_IIIa(Orion_Ship):
    def at_object_creation(self):
        super().at_object_creation()
        self.db.move["ratio"] = 4.0
        self.db.main["gw"] = 80.0 
        self.db.aux["gw"] = 48.0
        self.db.batt["gw"]= 8.0
        self.db.beam["banks"] = 6
        self.db.beam["exist"] = 1
        self.db.missile["tubes"] = 6
        self.db.missile["exist"] = 1
        self.db.cloak = {"version":0,"cost":80,"freq":0.0,"exist":1,"active":0,"damage":1.0}
        self.db.structure = {"type":1,"displacement":199160,"cargo_hold":19916,"cargo_mass":0.0,"superstructure":198.0,"max_structure":198,"has_landing_pad":1,"has_docking_bay":0,"can_land":1,"can_dock":1,"repair":198.0,"max_repair":198}
        arc_list = [41,41,35,35,31,47]
        for i in range(0,4):
            self.db.blist[i] = {"active":0,"name":3,"damage":1.0,"bonus":20,"cost":30,"range":260,"arcs":arc_list[i],"lock":0,"load":0,"recycle":6}
        for i in range(4,6):
            self.db.blist[i] = {"active":0,"name":4,"damage":1.0,"bonus":24,"cost":80,"range":480,"arcs":arc_list[i],"lock":0,"load":0,"recycle":6}
        arc_list = [27,27,27,27,30,30]
        for i in range(0,6):
            self.db.mlist[i] = {"active":0,"name":9,"damage":1.0,"warhead":25,"cost":2,"range":320,"arcs":arc_list[i],"lock":0,"load":0,"recycle":15}
        self.db.cost = 2056526
        create_ship_layout(self)

class Super_Cruiser_IIIa(Orion_Ship):
    def at_object_creation(self):
        super().at_object_creation()
        self.db.move["ratio"] = 6.0
        self.db.main["gw"] = 120.0 
        self.db.aux["gw"] = 72.0
        self.db.batt["gw"]= 12.0
        self.db.beam["banks"] = 6
        self.db.beam["exist"] = 1
        self.db.missile["tubes"] = 10
        self.db.missile["exist"] = 1
        self.db.cloak = {"version":0,"cost":120,"freq":0.0,"exist":1,"active":0,"damage":1.0}
        self.db.structure = {"type":1,"displacement":2399360,"cargo_hold":239936,"cargo_mass":0.0,"superstructure":335.0,"max_structure":335,"has_landing_pad":1,"has_docking_bay":0,"can_land":1,"can_dock":1,"repair":335.0,"max_repair":335}
        arc_list = [41,41,35,35,31,47]
        for i in range(0,4):
            self.db.blist[i] = {"active":0,"name":3,"damage":1.0,"bonus":20,"cost":30,"range":260,"arcs":arc_list[i],"lock":0,"load":0,"recycle":6}
        for i in range(4,6):
            self.db.blist[i] = {"active":0,"name":4,"damage":1.0,"bonus":30,"cost":100,"range":480,"arcs":arc_list[i],"lock":0,"load":0,"recycle":6}
        arc_list = [27,27,27,27,27,27,27,27,30,30]
        for i in range(0,10):
            self.db.mlist[i] = {"active":0,"name":9,"damage":1.0,"warhead":25,"cost":2,"range":320,"arcs":arc_list[i],"lock":0,"load":0,"recycle":15}
        self.db.cost = 3656143
        create_ship_layout(self)

class Cutlass_IV(Orion_Ship):
    def at_object_creation(self):
        super().at_object_creation()
        self.db.move["ratio"] = 2.0
        self.db.main["gw"] = 34.0 
        self.db.aux["gw"] = 12.0
        self.db.batt["gw"]= 3.4
        self.db.beam["banks"] = 4
        self.db.beam["exist"] = 1
        self.db.missile["tubes"] = 5
        self.db.missile["exist"] = 1
        self.db.cloak = {"version":0,"cost":10,"freq":0.0,"exist":1,"active":0,"damage":1.0}
        self.db.structure = {"type":1,"displacement":39695,"cargo_hold":3969,"cargo_mass":0.0,"superstructure":50.0,"max_structure":50,"has_landing_pad":1,"has_docking_bay":0,"can_land":1,"can_dock":1,"repair":50.0,"max_repair":50}
        arc_list = [59,59,61,55]
        for i in range(0,4):
            self.db.blist[i] = {"active":0,"name":4,"damage":1.0,"bonus":9,"cost":30,"range":480,"arcs":arc_list[i],"lock":0,"load":0,"recycle":6}
        arc_list = [43,43,43,29,23]
        for i in range(0,5):
            self.db.mlist[i] = {"active":0,"name":9,"damage":1.0,"warhead":25,"cost":1,"range":320,"arcs":arc_list[i],"lock":0,"load":0,"recycle":15}
        self.db.cost = 698811426
        create_ship_layout(self)

class Khopesh(Orion_Ship):
    def at_object_creation(self):
        super().at_object_creation()
        self.db.move["ratio"] = 1.0
        self.db.main["gw"] = 18.0 
        self.db.aux["gw"] = 12.0
        self.db.batt["gw"]= 1.8
        self.db.beam["banks"] = 4
        self.db.beam["exist"] = 1
        self.db.missile["tubes"] = 0
        self.db.missile["exist"] = 0
        self.db.cloak = {"version":0,"cost":8,"freq":0.0,"exist":1,"active":0,"damage":1.0}
        self.db.tech = {"firing":1.0,"fuel":1.0,"stealth":2.0,"cloak":1.0,"sensors":2.0,"aux_max":2.0,"main_max":2.0,"armor":1.0,"ly_range":1.0}
        self.db.structure = {"type":1,"displacement":13945,"cargo_hold":1394,"cargo_mass":0.0,"superstructure":23.0,"max_structure":23,"has_landing_pad":0,"has_docking_bay":0,"can_land":1,"can_dock":1,"repair":23.0,"max_repair":23}
        arc_list = [59,59,61,55]
        for i in range(0,4):
            self.db.blist[i] = {"active":0,"name":4,"damage":1.0,"bonus":6,"cost":20,"range":480,"arcs":arc_list[i],"lock":0,"load":0,"recycle":6}
        self.db.cost = 291651427
        create_fighter_layout(self)

class Excalibur_II(Orion_Ship):
    def at_object_creation(self):
        super().at_object_creation()
        self.db.move["ratio"] = 5.0
        self.db.main["gw"] = 102.0 
        self.db.aux["gw"] = 24.0
        self.db.batt["gw"]= 10.2
        self.db.beam["banks"] = 4
        self.db.beam["exist"] = 1
        self.db.missile["tubes"] = 10
        self.db.missile["exist"] = 1
        self.db.cloak = {"version":0,"cost":48,"freq":0.0,"exist":1,"active":0,"damage":1.0}
        self.db.tech = {"firing":1.0,"fuel":1.0,"stealth":2.0,"cloak":1.0,"sensors":2.0,"aux_max":2.0,"main_max":2.0,"armor":1.0,"ly_range":1.0}
        self.db.structure = {"type":1,"displacement":248795,"cargo_hold":24879,"cargo_mass":0.0,"superstructure":196.0,"max_structure":196,"has_landing_pad":1,"has_docking_bay":0,"can_land":1,"can_dock":1,"repair":196.0,"max_repair":196}
        arc_list = [59,59,61,55]
        for i in range(0,4):
            self.db.blist[i] = {"active":0,"name":4,"damage":1.0,"bonus":15,"cost":50,"range":480,"arcs":arc_list[i],"lock":0,"load":0,"recycle":6}
        arc_list = [43,43,43,43,29,29,23,23,30,30]
        for i in range(0,10):
            self.db.mlist[i] = {"active":0,"name":9,"damage":1.0,"warhead":25,"cost":1,"range":320,"arcs":arc_list[i],"lock":0,"load":0,"recycle":15}
        self.db.cost = 2480057144
        create_ship_layout(self)

class BR_Cutlass(Orion_Ship):
    def at_object_creation(self):
        super().at_object_creation()
        self.db.move["ratio"] = 2.0
        self.db.main["gw"] = 30.0 
        self.db.aux["gw"] = 4.0
        self.db.batt["gw"]= 3.0
        self.db.beam["banks"] = 6
        self.db.beam["exist"] = 1
        self.db.missile["tubes"] = 5
        self.db.missile["exist"] = 1
        self.db.cloak = {"version":0,"cost":48,"freq":0.0,"exist":1,"active":0,"damage":1.0}
        self.db.tech = {"firing":1.0,"fuel":1.0,"stealth":1.0,"cloak":1.0,"sensors":1.0,"aux_max":2.0,"main_max":2.0,"armor":1.0,"ly_range":1.0}
        self.db.structure = {"type":1,"displacement":38725,"cargo_hold":3872,"cargo_mass":0.0,"superstructure":33.0,"max_structure":33,"has_landing_pad":1,"has_docking_bay":0,"can_land":1,"can_dock":1,"repair":33.0,"max_repair":33}
        arc_list = [25,41,19,35,20,20]
        for i in range(0,6):
            self.db.blist[i] = {"active":0,"name":1,"damage":1.0,"bonus":1,"cost":6,"range":360,"arcs":arc_list[i],"lock":0,"load":0,"recycle":6}
        arc_list = [27,27,27,45,39]
        for i in range(0,5):
            self.db.mlist[i] = {"active":0,"name":1,"damage":1.0,"warhead":10,"cost":1,"range":240,"arcs":arc_list[i],"lock":0,"load":0,"recycle":15}
        self.db.cost = 99034285
        create_ship_layout(self)

class Stiletto_IV(Orion_Ship):
    def at_object_creation(self):
        super().at_object_creation()
        self.db.move["ratio"] = 2.0
        self.db.main["gw"] = 34.0 
        self.db.aux["gw"] = 12.0
        self.db.batt["gw"]= 3.4
        self.db.beam["banks"] = 4
        self.db.beam["exist"] = 1
        self.db.missile["tubes"] = 4
        self.db.missile["exist"] = 1
        self.db.structure = {"type":1,"displacement":24595,"cargo_hold":24595,"cargo_mass":0.0,"superstructure":39.0,"max_structure":39,"has_landing_pad":1,"has_docking_bay":0,"can_land":1,"can_dock":1,"repair":39.0,"max_repair":39}
        arc_list = [59,59,61,55]
        for i in range(0,4):
            self.db.blist[i] = {"active":0,"name":4,"damage":1.0,"bonus":9,"cost":30,"range":480,"arcs":arc_list[i],"lock":0,"load":0,"recycle":6}
        arc_list = [43,43,29,23]
        for i in range(0,4):
            self.db.mlist[i] = {"active":0,"name":9,"damage":1.0,"warhead":25,"cost":1,"range":320,"arcs":arc_list[i],"lock":0,"load":0,"recycle":15}
        self.db.cost = 601020
        create_ship_layout(self)

class Longsword_IV(Orion_Ship):
    def at_object_creation(self):
        super().at_object_creation()
        self.db.move["ratio"] = 3.0
        self.db.main["gw"] = 51.0 
        self.db.aux["gw"] = 12.0
        self.db.batt["gw"]= 5.1
        self.db.beam["banks"] = 4
        self.db.beam["exist"] = 1
        self.db.missile["tubes"] = 4
        self.db.missile["exist"] = 1
        self.db.cloak = {"version":0,"cost":20,"freq":0.0,"exist":1,"active":0,"damage":1.0}
        self.db.structure = {"type":1,"displacement":59555,"cargo_hold":5955,"cargo_mass":0.0,"superstructure":66.0,"max_structure":66,"has_landing_pad":1,"has_docking_bay":0,"can_land":1,"can_dock":1,"repair":66.0,"max_repair":66}
        arc_list = [59,59,61,55]
        for i in range(0,4):
            self.db.blist[i] = {"active":0,"name":4,"damage":1.0,"bonus":12,"cost":40,"range":480,"arcs":arc_list[i],"lock":0,"load":0,"recycle":6}
        arc_list = [43,43,29,23]
        for i in range(0,4):
            self.db.mlist[i] = {"active":0,"name":1,"damage":1.0,"warhead":20,"cost":1,"range":320,"arcs":arc_list[i],"lock":0,"load":0,"recycle":15}
        self.db.cost = 786840000
        create_ship_layout(self)

class Dirk_IV(Orion_Ship):
    def at_object_creation(self):
        super().at_object_creation()
        self.db.move["ratio"] = 1.0
        self.db.main["gw"] = 18.0 
        self.db.aux["gw"] = 12.0
        self.db.batt["gw"]= 1.8
        self.db.beam["banks"] = 4
        self.db.beam["exist"] = 1
        self.db.missile["tubes"] = 3
        self.db.missile["exist"] = 1
        self.db.cloak = {"version":0,"cost":8,"freq":0.0,"exist":1,"active":0,"damage":1.0}
        self.db.structure = {"type":1,"displacement":15015,"cargo_hold":1501,"cargo_mass":0.0,"superstructure":29.0,"max_structure":29,"has_landing_pad":0,"has_docking_bay":0,"can_land":1,"can_dock":1,"repair":29.0,"max_repair":29}
        arc_list = [59,59,61,55]
        for i in range(0,4):
            self.db.blist[i] = {"active":0,"name":4,"damage":1.0,"bonus":6,"cost":20,"range":480,"arcs":arc_list[i],"lock":0,"load":0,"recycle":6}
        arc_list = [43,29,23]
        for i in range(0,3):
            self.db.mlist[i] = {"active":0,"name":9,"damage":1.0,"warhead":25,"cost":1,"range":320,"arcs":arc_list[i],"lock":0,"load":0,"recycle":15}
        self.db.cost = 468128422
        create_ship_layout(self)

class Claymore_IV(Orion_Ship):
    def at_object_creation(self):
        super().at_object_creation()
        self.db.move["ratio"] = 4.0
        self.db.main["gw"] = 68.0 
        self.db.aux["gw"] = 12.0
        self.db.batt["gw"]= 6.8
        self.db.beam["banks"] = 4
        self.db.beam["exist"] = 1
        self.db.missile["tubes"] = 6
        self.db.missile["exist"] = 1
        self.db.cloak = {"version":0,"cost":32,"freq":0.0,"exist":1,"active":0,"damage":1.0}
        self.db.structure = {"type":1,"displacement":99485,"cargo_hold":9948,"cargo_mass":0.0,"superstructure":100.0,"max_structure":100,"has_landing_pad":1,"has_docking_bay":0,"can_land":1,"can_dock":1,"repair":100.0,"max_repair":100}
        arc_list = [59,59,61,55]
        for i in range(0,4):
            self.db.blist[i] = {"active":0,"name":4,"damage":1.0,"bonus":15,"cost":50,"range":480,"arcs":arc_list[i],"lock":0,"load":0,"recycle":6}
        arc_list = [43,43,43,43,29,23]
        for i in range(0,6):
            self.db.mlist[i] = {"active":0,"name":9,"damage":1.0,"warhead":25,"cost":1,"range":320,"arcs":arc_list[i],"lock":0,"load":0,"recycle":15}
        self.db.cost = 1291920168
        create_ship_layout(self)

class Excalibur(Orion_Ship):
    def at_object_creation(self):
        super().at_object_creation()
        self.db.move["ratio"] = 5.0
        self.db.main["gw"] = 85.0 
        self.db.aux["gw"] = 18.0
        self.db.batt["gw"]= 8.5
        self.db.beam["banks"] = 4
        self.db.beam["exist"] = 1
        self.db.missile["tubes"] = 10
        self.db.missile["exist"] = 1
        self.db.cloak = {"version":0,"cost":48,"freq":0.0,"exist":1,"active":0,"damage":1.0}
        self.db.structure = {"type":1,"displacement":249495,"cargo_hold":24949,"cargo_mass":0.0,"superstructure":200.0,"max_structure":200,"has_landing_pad":1,"has_docking_bay":0,"can_land":1,"can_dock":1,"repair":200.0,"max_repair":200}
        arc_list = [59,59,61,55]
        for i in range(0,4):
            self.db.blist[i] = {"active":0,"name":4,"damage":1.0,"bonus":15,"cost":50,"range":480,"arcs":arc_list[i],"lock":0,"load":0,"recycle":6}
        arc_list = [43,43,43,43,29,29,23,23,30,30]
        for i in range(0,10):
            self.db.mlist[i] = {"active":0,"name":9,"damage":1.0,"warhead":25,"cost":1,"range":320,"arcs":arc_list[i],"lock":0,"load":0,"recycle":15}
        self.db.cost = 2365884784
        create_ship_layout(self)

class Aeon_Flux_III(Orion_Ship):
    def at_object_creation(self):
        super().at_object_creation()
        self.db.move["ratio"] = 1.0
        self.db.main["gw"] = 34.0 
        self.db.aux["gw"] = 3.0
        self.db.batt["gw"]= 3.4
        self.db.beam["banks"] = 3
        self.db.beam["exist"] = 1
        self.db.missile["tubes"] = 2
        self.db.missile["exist"] = 1
        self.db.cloak = {"version":0,"cost":8,"freq":0.0,"exist":1,"active":0,"damage":1.0}
        self.db.structure = {"type":1,"displacement":24760,"cargo_hold":8100,"cargo_mass":0.0,"superstructure":17.0,"max_structure":17,"has_landing_pad":0,"has_docking_bay":0,"can_land":1,"can_dock":1,"repair":17.0,"max_repair":17}
        arc_list = [43,31,47]
        self.db.blist[0] = {"active":0,"name":2,"damage":1.0,"bonus":6,"cost":9,"range":200,"arcs":arc_list[0],"lock":0,"load":0,"recycle":6}
        for i in range(1,3):
            self.db.blist[i] = {"active":0,"name":2,"damage":1.0,"bonus":8,"cost":12,"range":200,"arcs":arc_list[i],"lock":0,"load":0,"recycle":6}
        arc_list = [41,35]
        for i in range(0,2):
            self.db.mlist[i] = {"active":0,"name":1,"damage":1.0,"warhead":10,"cost":1,"range":240,"arcs":arc_list[i],"lock":0,"load":0,"recycle":15}
        self.db.cost = 111375
        create_ship_layout(self)

class Aeon_Flux_III(Orion_Ship):
    def at_object_creation(self):
        super().at_object_creation()
        self.db.move["ratio"] = 1.0
        self.db.main["gw"] = 34.0 
        self.db.aux["gw"] = 3.0
        self.db.batt["gw"]= 3.4
        self.db.beam["banks"] = 3
        self.db.beam["exist"] = 1
        self.db.missile["tubes"] = 2
        self.db.missile["exist"] = 1
        self.db.cloak = {"version":0,"cost":8,"freq":0.0,"exist":1,"active":0,"damage":1.0}
        self.db.structure = {"type":1,"displacement":24760,"cargo_hold":8100,"cargo_mass":0.0,"superstructure":17.0,"max_structure":17,"has_landing_pad":0,"has_docking_bay":0,"can_land":1,"can_dock":1,"repair":17.0,"max_repair":17}
        arc_list = [43,31,47]
        self.db.blist[0] = {"active":0,"name":2,"damage":1.0,"bonus":6,"cost":9,"range":200,"arcs":arc_list[0],"lock":0,"load":0,"recycle":6}
        for i in range(1,3):
            self.db.blist[i] = {"active":0,"name":2,"damage":1.0,"bonus":8,"cost":12,"range":200,"arcs":arc_list[i],"lock":0,"load":0,"recycle":6}
        arc_list = [41,35]
        for i in range(0,2):
            self.db.mlist[i] = {"active":0,"name":1,"damage":1.0,"warhead":10,"cost":1,"range":240,"arcs":arc_list[i],"lock":0,"load":0,"recycle":15}
        self.db.cost = 111375
        create_fighter_layout(self)

class Bladewing_IV(Orion_Ship):
    def at_object_creation(self):
        super().at_object_creation()
        self.db.move["ratio"] = 0.5
        self.db.main["gw"] = 12.0 
        self.db.aux["gw"] = 8.0
        self.db.batt["gw"]= 1.2
        self.db.beam["banks"] = 4
        self.db.beam["exist"] = 1
        self.db.missile["tubes"] = 1
        self.db.missile["exist"] = 1
        self.db.structure = {"type":1,"displacement":4917,"cargo_hold":0,"cargo_mass":0.0,"superstructure":13.0,"max_structure":13,"has_landing_pad":0,"has_docking_bay":0,"can_land":1,"can_dock":0,"repair":13.0,"max_repair":13}
        arc_list = [57,57,51,51]
        for i in range(0,4):
            self.db.blist[i] = {"active":0,"name":1,"damage":1.0,"bonus":3,"cost":7,"range":400,"arcs":arc_list[i],"lock":0,"load":0,"recycle":6}
        self.db.mlist[0] = {"active":0,"name":1,"damage":1.0,"warhead":20,"cost":1,"range":320,"arcs":43,"lock":0,"load":0,"recycle":15}
        self.db.cost = 146880000
        create_fighter_layout(self)



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