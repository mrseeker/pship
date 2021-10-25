from world import alerts, errors, unparse, constants, format, utils
from evennia.utils.search import search_object, search_tag
import math

#Gives detailed sensor information
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

#Gives information about an empire
def do_border_report(self):
    obj_x = search_object(self.caller.location)[0]
    obj = search_object(obj_x.db.ship)[0]
    if(errors.error_on_console(self.caller,obj)):
        return 0
    elif(obj.db.sensor["lrs_exist"]==0):
        self.caller.msg(alerts.ansi_red(obj.name + " has no long-range sensors."))
    elif(obj.db.sensor["lrs_active"] == 0):
        self.caller.msg(alerts.ansi_red("Long-range sensors are inactive."))
    else:
        buffer = "|b|h--[|yBorder Report|b]--------------------------------------------------------------|n\n|cEmpire               Bearing  Range   Status   Center Coordinates|w\n|b-------------------- ------- ------- -------- ---------------------------------|w\n"
        for empire in search_tag(constants.EMPIRE_ATTR_NAME,category="space_object"):
            if (empire is not None):
                range = utils.xyz2range(obj.db.coords["x"],obj.db.coords["y"],obj.db.coords["z"],empire.db.coords["x"],empire.db.coords["y"],empire.db.coords["z"]) / constants.PARSEC
                if (math.fabs(range - empire.db.radius) >= 100.0):
                    continue
                buffer += f'{empire.name:>20}'
                if (range > empire.db.radius):
                    buffer += f'{int(utils.xy2bearing((empire.db.coords["x"] - obj.db.coords["x"]),(empire.db.coords["y"] - obj.db.coords["y"]))):3d} {int(utils.xyz2elevation((empire.db.coords["x"] - obj.db.coords["x"]),(empire.db.coords["y"] - obj.db.coords["y"]),(empire.db.coords["z"] - obj.db.coords["z"]))):>3d}  {unparse.unparse_range((range - empire.db.radius) * constants.PARSEC):>7s}  Outside  '
                else:
                    buffer += f'{int(utils.xy2bearing((obj.db.coords["x"] - empire.db.coords["x"]),(obj.db.coords["y"] - empire.db.coords["y"]))):3d} {int(utils.xyz2elevation((obj.db.coords["x"] - empire.db.coords["x"]),(obj.db.coords["y"] - empire.db.coords["y"]),(obj.db.coords["z"] - empire.db.coords["z"]))):>3d}  {unparse.unparse_range((empire.db.radius - range) * constants.PARSEC):>7s}  Inside   '
                buffer += f'{(empire.db.coords["x"] - obj.db.coords["xo"])/constants.PARSEC:10.3f} {(empire.db.coords["y"] - obj.db.coords["yo"])/constants.PARSEC:10.3f} {(empire.db.coords["z"] - obj.db.coords["zo"])/constants.PARSEC:10.3f}\n'
        buffer += format.l_line()
        buffer += format.course(obj)
        buffer += format.speed(obj)
        buffer += "\n"
        buffer += format.location(obj)
        buffer += format.velocity(obj)
        buffer += "\n"
        buffer += format.l_end()
        alerts.notify(self.caller,buffer)