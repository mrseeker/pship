"""
This holds all the information for an empire. The physical representation of this empire is a beacon
"""
from typeclasses.objects import Object
from world import constants

class Empire(Object):
    def at_object_creation(self):
        super().at_object_creation()
        self.db.desc = "This is a beacon used to indicate empires"
        self.db.type = constants.EMPIRE_ATTR_NAME
        self.tags.add(constants.EMPIRE_ATTR_NAME,category="space_object")
        self.db.sdesc = "Default Empire"
        self.db.location = 0
        self.db.space = 0
        self.db.radius = 1
        self.db.active = 0
        self.db.coords = {"x":0.0,"y":0.0,"z":0.0}
        

    def get_display_name(self,looker, **kwargs):
       idstr = "(#%s)" % self.id if self.access(looker, access_type="control") else ""
       selfdesc = self.name if self.access(looker, access_type="control") else self.db.sdesc
       return "%s%s" % (selfdesc, idstr)
