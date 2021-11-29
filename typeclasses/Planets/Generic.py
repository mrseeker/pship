from evennia.utils.create import create_object
from typeclasses.airlock import Airlock
from typeclasses.exits import Exit
from typeclasses.planet import Generic_Planet


class D(Generic_Planet):
    """
    This is an D-class planet. (Moon)
    These planets had a barren and cratered surface, and had little to no atmosphere.
    """
    def at_object_creation(self):
        super().at_object_creation()
        ship_airlock = create_object(Airlock,key=self.key + "-airlock")
        ship_airlock.db.ship = self.key
        ship_airlock.tags.add("airlock",category=self.key)
        exit_airlock_bridge = create_object(Exit, key="Airlock",aliases=["airlock"], location=self, destination=ship_airlock)
        exit_airlock = create_object(Exit, key="Planet Surface",aliases=["planet"], location=ship_airlock, destination=self)

class H(Generic_Planet):
    """
    This is an H-class planet. (Sheliak)
    These desert planets were categorized by a hot and arid surface, with little or no surface water and an atmosphere that might contain heavy gasses and metal vapors. Lifeforms found on class H planets included drought- and radiation-resistant plant life and similar animal life.
    """
    def at_object_creation(self):
        super().at_object_creation()
        ship_airlock = create_object(Airlock,key=self.key + "-airlock")
        ship_airlock.db.ship = self.key
        ship_airlock.tags.add("airlock",category=self.key)
        exit_airlock_bridge = create_object(Exit, key="Airlock",aliases=["airlock"], location=self, destination=ship_airlock)
        exit_airlock = create_object(Exit, key="Planet Surface",aliases=["planet"], location=ship_airlock, destination=self)

class J(Generic_Planet):
    """
    This is an J-class planet.
    They are located within the "cold zone" of a star system. A Class J gas giant is characterized by a tenuous surface, consisting of gaseous hydrogen and some hydrogen compounds, and an atmosphere consisting of zones that vary in temperature and composition.
    """
    def at_object_creation(self):
        super().at_object_creation()
        self.db.structure["has_landing_pad"] = 0

class K(Generic_Planet):
    """
    This is an K-class planet.
    A class K planet is found within the ecosphere of a star system. They are categorized by a barren surface with little or no surface water and a thin atmosphere comprised mainly of carbon dioxide. Lifeforms found on class K planets are limited to single-celled organisms, although class K planets can be adapted for humanoid life through the use of pressure domes.
    """
    def at_object_creation(self):
        super().at_object_creation()
        ship_airlock = create_object(Airlock,key=self.key + "-airlock")
        ship_airlock.db.ship = self.key
        ship_airlock.tags.add("airlock",category=self.key)
        exit_airlock_bridge = create_object(Exit, key="Airlock",aliases=["airlock"], location=self, destination=ship_airlock)
        exit_airlock = create_object(Exit, key="Planet Surface",aliases=["planet"], location=ship_airlock, destination=self)

class L(Generic_Planet):
    """
    This is an L-class planet.
    Class L worlds could have different kinds of atmospheres ranging from suitable for humanoid life to unsuited without additional means, but typically they had higher concentrations of carbon dioxide than class M worlds. While vegetation was common on L-class worlds, they were usually, though not always, devoid of fauna. Class L planets were prime candidates for colonization and potential terraforming.
    """
    def at_object_creation(self):
        super().at_object_creation()
        ship_airlock = create_object(Airlock,key=self.key + "-airlock")
        ship_airlock.db.ship = self.key
        ship_airlock.tags.add("airlock",category=self.key)
        exit_airlock_bridge = create_object(Exit, key="Airlock",aliases=["airlock"], location=self, destination=ship_airlock)
        exit_airlock = create_object(Exit, key="Planet Surface",aliases=["planet"], location=ship_airlock, destination=self)

class M(Generic_Planet):
    """
    This is an M-class planet.
    A class M or Minshara class planet, moon, or planetoid was considered to be suitable for humanoid life.
    """
    def at_object_creation(self):
        super().at_object_creation()
        ship_airlock = create_object(Airlock,key=self.key + "-airlock")
        ship_airlock.db.ship = self.key
        ship_airlock.tags.add("airlock",category=self.key)
        exit_airlock_bridge = create_object(Exit, key="Airlock",aliases=["airlock"], location=self, destination=ship_airlock)
        exit_airlock = create_object(Exit, key="Planet Surface",aliases=["planet"], location=ship_airlock, destination=self)

class N(Generic_Planet):
    """
    This is an N-class planet.
    Reducing planets are located within the "ecosphere" of a star system, with class N planets categorized by a high surface temperature due to greenhouse effect (which causes all water on the planet to exist only as vapor) and an extremely dense atmosphere, comprised of carbon dioxide and sulfides. A textbook example of a class N planet is Venus.
    """
    def at_object_creation(self):
        super().at_object_creation()
        ship_airlock = create_object(Airlock,key=self.key + "-airlock")
        ship_airlock.db.ship = self.key
        ship_airlock.tags.add("airlock",category=self.key)
        exit_airlock_bridge = create_object(Exit, key="Airlock",aliases=["airlock"], location=self, destination=ship_airlock)
        exit_airlock = create_object(Exit, key="Planet Surface",aliases=["planet"], location=ship_airlock, destination=self)

class N(Generic_Planet):
    """
    This is an N-class planet.
    Reducing planets are located within the "ecosphere" of a star system, with class N planets categorized by a high surface temperature due to greenhouse effect (which causes all water on the planet to exist only as vapor) and an extremely dense atmosphere, comprised of carbon dioxide and sulfides. A textbook example of a class N planet is Venus.
    """
    def at_object_creation(self):
        super().at_object_creation()
        ship_airlock = create_object(Airlock,key=self.key + "-airlock")
        ship_airlock.db.ship = self.key
        ship_airlock.tags.add("airlock",category=self.key)
        exit_airlock_bridge = create_object(Exit, key="Airlock",aliases=["airlock"], location=self, destination=ship_airlock)
        exit_airlock = create_object(Exit, key="Planet Surface",aliases=["planet"], location=ship_airlock, destination=self)

class R(Generic_Planet):
    """
    This is an R-class planet.
    A rogue planet is a planet that has broken out of its orbit around a star. However, such a planet may still be capable of supporting life due to geologic activities on it, such as hot gases venting from its interior, forming oases where lifeforms can thrive. The lack of a sun causes rogue planets to exist in a state of perpetual night.
    """
    def at_object_creation(self):
        super().at_object_creation()
        ship_airlock = create_object(Airlock,key=self.key + "-airlock")
        ship_airlock.db.ship = self.key
        ship_airlock.tags.add("airlock",category=self.key)
        exit_airlock_bridge = create_object(Exit, key="Airlock",aliases=["airlock"], location=self, destination=ship_airlock)
        exit_airlock = create_object(Exit, key="Planet Surface",aliases=["planet"], location=ship_airlock, destination=self)

class T(Generic_Planet):
    """
    This is an T-class planet.
    a class T planet is a gas giant classified as a "large ultragiant", 50,000,000 to 120,000,000 kilometers in diameter.
    """
    def at_object_creation(self):
        super().at_object_creation()
        self.db.structure["has_landing_pad"] = 0

class Y(Generic_Planet):
    """
    This is an Y-class planet.
     a class Y planet was characterized by a toxic atmosphere, sulfuric deserts, surface temperatures exceeding five hundred Kelvin, and thermionic radiation discharges. Due to the inhospitable and dangerous nature, and often hellish appearance, of such planets they were also nicknamed "Demon class" by Starfleet. Even entering a standard orbit of a class Y planet could be hazardous to starships.
     """
    def at_object_creation(self):
        super().at_object_creation()
        ship_airlock = create_object(Airlock,key=self.key + "-airlock")
        ship_airlock.db.ship = self.key
        ship_airlock.tags.add("airlock",category=self.key)
        exit_airlock_bridge = create_object(Exit, key="Airlock",aliases=["airlock"], location=self, destination=ship_airlock)
        exit_airlock = create_object(Exit, key="Planet Surface",aliases=["planet"], location=ship_airlock, destination=self)

