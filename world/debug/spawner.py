from evennia.utils.create import create_object
from evennia.utils.search import search_object
from typeclasses.Ships import Generic
from world import utils,set,iterate

self = search_object("#1")[0]
for i in range(0,10):
    ship = create_object(Generic.FrS,key="TEST-" + str(i))

    ship.db.fuel["antimatter"] = utils.sdb2max_antimatter(ship)
    ship.db.fuel["deuterium"] = utils.sdb2max_deuterium(ship)
    ship.db.fuel["reserves"] = utils.sdb2max_reserves(ship)

    set.do_set_active(self,ship)
    ship.db.status["autopilot"] = 1

    ship.db.alloc["helm"] = 0.90
    ship.db.alloc["operations"] = 0.10
    ship.db.alloc["movement"] = 1.00
    ship.db.alloc["version"] = 1
    ship.db.main["in"] = 1.00
    ship.db.aux["in"] = 1.00
    iterate.do_space_db_iterate([ship])
    iterate.up_main_io(ship)
    iterate.up_aux_io(ship)
    iterate.up_total_power(ship)
    set.do_set_coords_layin(self,ship,i,i,0)
    set.do_set_speed(self,ship,ship.db.engine["warp_cruise"])
    set.do_set_coords_engage(self,ship)
