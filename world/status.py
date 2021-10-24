from world import alerts, errors, unparse, constants, format, utils
from evennia.utils.search import search_object

def sensor_report(self,contact):
    obj_x = search_object(self.caller.location)[0]
    obj = search_object(obj_x.db.ship)[0]
    obj_contact = utils.contact2sdb(obj,contact)
    if(errors.error_on_console(self.caller,obj)):
        return 0
    elif(obj.db.sensor["lrs_exist"]==0 and obj.db.sensor["srs_exist"]==0):
        self.caller.msg(alerts.ansi_red(obj.name + " has no sensors."))
    elif(obj.db.sensor["contacts"] == 0):
        self.caller.msg(alerts.ansi_red("There are no sensor contacts."))
    elif(errors.error_on_contact(self,obj,obj_contact)):
        return 0
    else:
        i = utils.contact2slist(obj,contact)
        buffer = "|b|h--[|yDetailed Sensor Report|b]-----------------------------------------------------|w|n\n"
        buffer += format.type(obj_contact)
        buffer += format.resolution(obj.db.slist["lev"][i])
        buffer += "\n"
        if (obj.db.slist["lev"][i] > 0.5 and not obj_contact.db.cloak["active"]):
            buffer += format.name(obj_contact)
            buffer += format.cargo_cap(obj_contact)
            buffer += "\n"
            if (obj_contact.db.structure["type"] < 3 and (obj_contact.db.structure["has_docking_bay"] == 1 or obj_contact.db.structure["has_landing_pad"] == 1)):
                if (obj_contact.db.structure["has_docking_bay"] == 1):
                    buffer += format.docking_doors(obj_contact)
                if (obj_contact.db.structure["has_landing_pad"] == 1):
                    buffer += format.landing_doors(obj_contact)
                buffer += "\n"
        if (obj.db.slist["lev"][i] > 0.25 and not obj_contact.db.cloak["active"]):
            buffer += format.ship_class(obj_contact)
            buffer += format.displacement(obj_contact)
            buffer += "\n"
        buffer += format.contact_arc(obj, obj_contact)
        buffer += format.contact_shield(obj, obj_contact)
        buffer += "\n"
        buffer += format.course(obj_contact)
        buffer += format.speed(obj_contact)
        buffer += "\n"
        buffer += format.l_line()
        buffer += format.bearing(obj,obj_contact)
        buffer += format.ship_range(obj,obj_contact)
        buffer += "\n"
        buffer += format.firing_arc(obj, obj_contact)
        buffer += format.facing_shield(obj, obj_contact)
        buffer += "\n"
        buffer += format.l_end()
        alerts.notify(self.caller,buffer)
    return 1