"""
This holds all the information for an empire. The physical representation of this empire is a beacon
"""
from typeclasses.spaceship import Ship
from world import constants

class Empire(Ship):
    def at_object_creation(self):
        super().at_object_creation()
        self.db.desc = "This is a beacon used to indicate empires"
        self.db.type = constants.EMPIRE_ATTR_NAME
        self.tags.add(tag=constants.EMPIRE_ATTR_NAME,category="space_object")
        self.tags.remove(category="space_object",tag=constants.SHIP_ATTR_NAME)
        self.db.sdesc = "Default Empire"
        self.db.location = 0
        self.db.space = 0
        self.db.radius = 1
        self.db.structure["type"] = 11

    def get_display_name(self,looker, **kwargs):
       idstr = "(#%s)" % self.id if self.access(looker, access_type="control") else ""
       selfdesc = self.name if self.access(looker, access_type="control") else self.db.sdesc
       return "%s%s" % (selfdesc, idstr)
