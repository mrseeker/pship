from world import alerts, errors, unparse, constants, format, utils
from evennia.utils.search import search_object, search_tag
from evennia.utils import evtable
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
        buffer = "|b--[|yDetailed Sensor Report|b]-----------------------------------------------------|w|n\n"
        buffer += format.type(obj_contact)
        buffer += format.resolution(obj.db.slist[i]["lev"])
        buffer += "\n"
        if (obj.db.slist[i]["lev"] > 0.5 and not obj_contact.db.cloak["active"]):
            buffer += format.name(obj_contact)
            buffer += format.cargo_cap(obj_contact)
            buffer += "\n"
            if (obj_contact.db.structure["type"] < 3 and (obj_contact.db.structure["has_docking_bay"] == 1 or obj_contact.db.structure["has_landing_pad"] == 1)):
                if (obj_contact.db.structure["has_docking_bay"] == 1):
                    buffer += format.docking_doors(obj_contact)
                if (obj_contact.db.structure["has_landing_pad"] == 1):
                    buffer += format.landing_doors(obj_contact)
                buffer += "\n"
        if (obj.db.slist[i]["lev"] > 0.25 and not obj_contact.db.cloak["active"]):
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
        buffer = "|b--[|yBorder Report|b]--------------------------------------------------------------|n\n|cEmpire               Bearing  Range   Status   Center Coordinates|w\n|b-------------------- ------- ------- -------- ---------------------------------|w\n"
        for empire in search_tag(constants.EMPIRE_ATTR_NAME,category="space_object"):
            if (empire is not None):
                range = utils.xyz2range(obj.db.coords["x"],obj.db.coords["y"],obj.db.coords["z"],empire.db.coords["x"],empire.db.coords["y"],empire.db.coords["z"]) / constants.PARSEC
                if (math.fabs(range - empire.db.radius) >= 100.0):
                    continue
                buffer += f'{empire.db.sdesc:>20}'
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
        
def contact_flags(self,obj):
    fp = ""
    if(obj.db.status["active"]):
        fp += 'A'
    if(obj.db.move["in"] != obj.db.move["out"]):
        fp += 'a'
    if(obj.db.beam["banks"] > 0):
        for i in range(obj.db.beam["banks"]):
            if(obj.db.blist[i]["lock"] == self.name):
                fp += 'B'
            elif(obj.db.blist[i]["active"] > 0):
                fp += 'b'
    if(obj.db.cloak["active"]):
        fp += 'C'
    if(obj.db.status["connected"]):
        fp += 'c'
    if(obj.db.status["docked"]):
        fp += 'd'
    if((obj.db.power["total"] * obj.db.alloc["sensors"] > 0.0) and obj.db.sensor["ew_active"] > 0):
        fp += 'E'
    if(obj.db.power["total"] != 0.0):
        fp += 'e'
    if(obj.db.status["landed"] == 1):
        fp += 'l'
    if(obj.db.missile["tubes"] > 0):
        for i in range(obj.db.missile["tubes"]):
            if(obj.db.mlist[i]["lock"] == self.name):
                fp += 'M'
            elif(obj.db.mlist[i]["active"] > 0):
                fp += 'm'
    if(self.db.shield["exist"]):
        for i in range(constants.MAX_SHIELD_NAME):
            if(obj.db.shield[i]["active"] * obj.db.alloc["shield"][i] * obj.db.power["total"] * obj.db.shield[i]["damage"] > 0.0):
                fp += 'S'
                break
    if(obj.db.status["tractoring"] == 1):
        fp += 'T'
    if(obj.db.status["tractored"] == 1):
        fp += 't'
    if(obj.db.status["crippled"] == 1):
        fp += 'X'
    return fp
    
def contact_line(obj_x,contact):
    obj = search_object(obj_x.db.slist[contact]["key"])[0]
    level = obj.db.slist[contact]["lev"] * 100.0
    
    if (level < 0.0):
        level = 0.0
    elif(level > 100.0):
        level = 100.0
    
    arc1 = unparse.unparse_arc(utils.sdb2arc(obj_x,obj))
    arc2 = unparse.unparse_arc(utils.sdb2arc(obj,obj_x))
    
    buffer = ""
    
    if(obj_x.db.iff["frequency"] == obj.db.iff["frequency"]):
        friendly = "|g*"
    else:
        friendly = "|r*"
    if (obj.db.cloak["active"]):
        cloak = "(cloaked)"
        classname = "-"
        contact_flag = "-"
    else:
        if (level < 50.0):
            cloak = "-"
            classname = f'{unparse.unparse_class(obj):16}'
            contact_flag = f'{contact_flags(obj_x,obj):6}'
        else:
            cloak = f'{obj.name}'
            classname = f'{unparse.unparse_class(obj):16}'
            contact_flag = f'{contact_flags(obj_x,obj):6}'
    
    if (level < 25):
        buffer = [f'{obj_x.db.slist[contact]["num"]:3d}',f'{unparse.unparse_type(obj):4}',f'{level:3.0f}',f'{utils.sdb2bearing(obj_x,obj):3.0f}',f'{utils.sdb2elevation(obj_x, obj):3.0f}',f'{unparse.unparse_range(utils.sdb2range(obj_x,obj)):7}',f'{arc1:5}',f'{obj.db.course["yaw_out"]:3.0f}',f'{obj.db.course["pitch_out"]:3.0f}',f'{unparse.unparse_speed(obj.db.move["out"]):6s}',f'{arc2:5s}',"-","-",f'{friendly}|n']
    else:
        buffer = [f'{obj_x.db.slist[contact]["num"]:3d}',f'{unparse.unparse_type(obj):4}',f'{level:3.0f}',f'{utils.sdb2bearing(obj_x,obj):3.0f}',f'{utils.sdb2elevation(obj_x, obj):3.0f}',f'{unparse.unparse_range(utils.sdb2range(obj_x,obj)):7}',f'{arc1:5}',f'{obj.db.course["yaw_out"]:3.0f}',f'{obj.db.course["pitch_out"]:3.0f}',f'{unparse.unparse_speed(obj.db.move["out"]):6s}',f'{arc2:5s}',f'{cloak}',f'{classname}',f'{contact_flag}',f'{friendly}|n']
    return buffer
    
def do_sensor_contacts(self, a):
    obj_x = search_object(self.caller.location)[0]
    obj = search_object(obj_x.db.ship)[0]
    if (isinstance(a,int)):
        contact = utils.contact2slist(obj,a)
        x = 0
    else:
        contact = constants.SENSOR_FAIL
        x = a[0].lower()
    ctype = 0
    if(x == 'a'):
        ctype = 4
    elif(x == 'b'):
        ctype = 2
    elif(x == 'p'):
        ctype = 3
    elif(x == 's'):
        x = a[1].lower()
        if(x == 'h'):
            ctype = 1
        elif(x == 't'):
            ctype = 5
        else:
            ctype = 0
    else:
        ctype = 0
    if(errors.error_on_console(self.caller,obj)):
        return 0
    elif(obj.db.sensor["contacts"] == 0):
        buffer = "|b--[|ySensor Report|b]--------------------------------------------------------------|n\n"
        buffer += format.course(obj)
        buffer += format.speed(obj)
        buffer += "\n"
        buffer += format.location(obj)
        buffer += format.velocity(obj)
        buffer += "\n"
        buffer += format.l_end()
        alerts.notify(self.caller, buffer)
        return 1
    elif(ctype > 0):
        buffer = "|b--[|ySensor Report|b]--------------------------------------------------------------|n\n"
        
        #buffer += "|c### Type Res Bearing Range   Arcs  Heading Speed  Arcs  Name       Class flags\n"
        #buffer += "|b--- ---- --- ------- ------- ----- ------- ------ ----- ---------------- ------|w\n"
        table = evtable.EvTable("###","Type","Res","Bearing","Elevation","Range","Arcs","Yaw","Pitch","Speed","Arcs","Name","Class","flags",border="header",header_line_char="-")
        for contact in range(obj.db.sensor["contacts"]):
            obj_contact = search_object(obj.db.slist[contact]["key"])[0]
            if(obj_contact.db.structure["type"] == ctype):
                #buffer += contact_line(obj,contact)
                table.add_row(*contact_line(obj,contact))
        buffer += str(table)
        buffer += "\n"
        buffer += format.l_line()
        buffer += format.course(obj)
        buffer += format.speed(obj)
        buffer += "\n"
        buffer += format.location(obj)
        buffer += format.velocity(obj)
        buffer += "\n"
        buffer += format.l_end()
        alerts.notify(self.caller, buffer)
        return 1
    elif(contact != constants.SENSOR_FAIL):
        buffer = ""
        #buffer = "|c### Type Res Bearing Range   Arcs  Heading Speed  Arcs  Name       Class flags\n"
        #buffer += "|b--- ---- --- ------- ------- ----- ------- ------ ----- ---------------- ------|w\n"
        table = evtable.EvTable("###","Type","Res","Bearing","Elevation","Range","Arcs","Yaw","Pitch","Speed","Arcs","Name","Class","flags",border="header",header_line_char="-")
        table.add_row(*contact_line(obj,contact))
        #buffer += contact_line(obj,contact)
        buffer += str(table)
        alerts.notify(self.caller, buffer)
        return 1
    else:
        buffer = "|b--[|ySensor Report|b]--------------------------------------------------------------|n\n"
        
        #buffer += "|c### Type Res Bearing Range   Arcs  Heading Speed  Arcs  Name       Class flags\n"
        table = evtable.EvTable("###","Type","Res","Bearing","Elevation","Range","Arcs","Yaw","Pitch","Speed","Arcs","Name","Class","flags",border="header",header_line_char="-")
        for ctype in range(1,len(constants.type_name)):
            first = 1
            for contact in range(obj.db.sensor["contacts"]):
                if(first):
                    #buffer += "|b--- ---- --- ------- ------- ----- ------- ------ ----- ---------------- ------|w\n"
                    first = 0
                #buffer += contact_line(obj,contact)
                obj = search_object(obj_x.db.slist[contact]["key"])[0]
                if obj.db.structure["type"] == ctype:
                    table.add_row(*contact_line(obj,contact))
        buffer += str(table)
        buffer += "\n"
        buffer += format.l_line()
        buffer += format.course(obj)
        buffer += format.speed(obj)
        buffer += "\n"
        buffer += format.location(obj)
        buffer += format.velocity(obj)
        buffer += "\n"
        buffer += format.l_end()
        alerts.notify(self.caller, buffer)
        return 1

def do_damage_status(self,obj,name=None):
    if(obj.db.structure["type"] == 0):
        alerts.notify(self,alerts.ansi_red("Space object not loaded."))
        return 0
    elif(obj.db.status["crippled"] == 2):
        alerts.notify(self,alerts.ansi_red("Space object destroyed."))
        return 0
    elif(obj.db.status["active"] != 1):
        alerts.notify(self,alerts.ansi_red("{:s} systems are inactive.".format(obj.name)))
        return 0
    
    if(name is not None):
        obj_x = utils.name2sdb(name)

        if (obj_x == constants.SENSOR_FAIL):
            alerts.notify(self,alerts.ansi_red("That is not a valid subject."))
            return 0
        elif(obj_x.db.location != obj.name):
            alerts.notify(self,alerts.ansi_red("That is not a valid subject."))
            return 0
        elif(obj_x.db.type == 0):
            alerts.notify(self,alerts.ansi_red("That is not a valid subject."))
            alerts.write_spacelog(self,obj_x,"BUG:Subject has bad TYPE")
            return 0
        elif(obj_x.db.status["connected"] != 1):
            alerts.notify(self,alerts.ansi_red("{:s} is not connected.".format(obj_x.name)))
    else:
        obj_x = obj
    
    buffer = "|b--[|yDamage Control Status Report|b]-----------------------------------------------|n\n"
    if(name is not None):
        buffer += format.name(obj_x)
        buffer += format.ship_class(obj_x)
        buffer += "\n"
        buffer += format.l_line()
    table = evtable.EvTable("System Name","Integ","Condition","Repair Cost",border="header",header_line_char="-")
    if(obj_x.db.structure["superstructure"] != obj_x.db.structure["max_structure"]):
        table.add_row(constants.system_name[0],unparse.unparse_percent(obj_x.db.structure["superstructure"]/obj_x.db.structure["max_structure"]),unparse.unparse_damage(obj_x.db.structure["superstructure"]/obj_x.db.structure["max_structure"]),(obj_x.db.structure["superstructure"] - obj_x.db.structure["max_structure"]) * constants.repair_mult[0])
    if(obj_x.db.aux["exist"] == 1 and obj_x.db.aux["damage"] < 1.0):
        table.add_row(constants.system_name[1],unparse.unparse_percent(obj_x.db.aux["damage"]),unparse.unparse_damage(obj_x.db.aux["damage"]),(1 - obj_x.db.aux["damage"]) * constants.repair_mult[1] * obj_x.db.aux["gw"] * 100.0)
    if(obj_x.db.batt["exist"] == 1 and obj_x.db.batt["damage"] < 1.0):
        table.add_row(constants.system_name[2],unparse.unparse_percent(obj_x.db.batt["damage"]),unparse.unparse_damage(obj_x.db.batt["damage"]),(1 - obj_x.db.batt["damage"]) * constants.repair_mult[2] * obj_x.db.batt["gw"] * 100.0)
    if(obj_x.db.beam["exist"] == 1):
        for i in range(obj_x.db.beam["banks"]):
            if(obj_x.db.blist[i]["damage"] < 1.0):
                table.add_row("{:s} {:d}".format(constants.system_name[3],i+1),unparse.unparse_percent(obj_x.db.blist[i]["damage"]),unparse.unparse_damage(obj_x.db.blist[i]["damage"]),(1.0 - obj_x.db.blist[i]["damage"])* constants.repair_mult[3] * obj_x.db.blist[i]["cost"] * 100.0)
    if(obj_x.db.cloak["exist"] == 1 and obj_x.db.cloak["damage"] < 1.0):
        table.add_row(constants.system_name[4],unparse.unparse_percent(obj_x.db.cloak["damage"]),unparse.unparse_damage(obj_x.db.cloak["damage"]),(1 - obj_x.db.cloak["damage"]) * constants.repair_mult[4] * (1.0 + (obj_x.db.structure["max_structure"]/10.0))*100.0)
    if(obj_x.db.sensor["ew_exist"] == 1 and obj_x.db.sensor["ew_damage"] < 1.0):
        table.add_row(constants.system_name[5],unparse.unparse_percent(obj_x.db.sensor["ew_damage"]),unparse.unparse_damage(obj_x.db.sensor["ew_damage"]),(1 - obj_x.db.sensor["ew_damage"]) * constants.repair_mult[5] * (1.0 + (obj_x.db.structure["max_structure"]/10.0))*100.0)
    if(obj_x.db.engine["impulse_exist"] == 1 and obj_x.db.engine["impulse_damage"] < 1.0):
        table.add_row(constants.system_name[6],unparse.unparse_percent(obj_x.db.engine["impulse_damage"]),unparse.unparse_damage(obj_x.db.engine["impulse_damage"]),(1 - obj_x.db.engine["impulse_damage"]) * constants.repair_mult[6] * (1.0 + (obj_x.db.structure["max_structure"]/10.0))*100.0)
    if(obj_x.db.sensor["lrs_exist"] == 1 and obj_x.db.sensor["lrs_damage"] < 1.0):
        table.add_row(constants.system_name[7],unparse.unparse_percent(obj_x.db.sensor["lrs_damage"]),unparse.unparse_damage(obj_x.db.sensor["lrs_damage"]),(1 - obj_x.db.sensor["lrs_damage"]) * constants.repair_mult[7] * (1.0 + (obj_x.db.structure["max_structure"]/10.0))*100.0)
    if(obj_x.db.main["exist"] == 1 and obj_x.db.main["damage"] < 1.0):
        table.add_row(constants.system_name[8],unparse.unparse_percent(obj_x.db.main["damage"]),unparse.unparse_damage(obj_x.db.main["damage"]),(1 - obj_x.db.main["damage"]) * constants.repair_mult[8] * obj_x.db.main["gw"] * 100.0)
    if(obj_x.db.missile["exist"] == 1):
        for i in range(obj_x.db.missile["tubes"]):
            if(obj_x.db.mlist[i]["damage"] < 1.0):
                table.add_row("{:s} {:d}".format(constants.system_name[9],i+1),unparse.unparse_percent(obj_x.db.mlist[i]["damage"]),unparse.unparse_damage(obj_x.db.mlist[i]["damage"]),(1.0 - obj_x.db.mlist[i]["damage"])* constants.repair_mult[9] * obj_x.db.blist[i]["warhead"] * 100.0)
    if(obj_x.db.shield["exist"] == 1):
        for i in range(constants.MAX_SHIELD_NAME):
            if(obj_x.db.shield[i]["damage"] < 1.0):
                table.add_row(unparse.unparse_shield(i),unparse.unparse_percent(obj_x.db.shield[i]["damage"]),unparse.unparse_damage(obj_x.db.shield[i]["damage"]),(1.0 - obj_x.db.shield[i]["damage"])* constants.repair_mult[10] * (1.0 + (obj_x.db.structure["max_structure"]/10.0)) * 100)
    if(obj_x.db.sensor["srs_exist"] == 1 and obj_x.db.sensor["ars_damage"] < 1.0):
        table.add_row(constants.system_name[11],unparse.unparse_percent(obj_x.db.sensor["srs_damage"]),unparse.unparse_damage(obj_x.db.sensor["srs_damage"]),(1 - obj_x.db.sensor["srs_damage"]) * constants.repair_mult[11] * (1.0 + (obj_x.db.structure["max_structure"]/10.0))*100.0)
    if(obj_x.db.tract["exist"] == 1 and obj_x.db.tract["damage"] < 1.0):
        table.add_row(constants.system_name[12],unparse.unparse_percent(obj_x.db.tract["damage"]),unparse.unparse_damage(obj_x.db.tract["damage"]),(1 - obj_x.db.tract["damage"]) * constants.repair_mult[12] * (1.0 + (obj_x.db.structure["max_structure"]/10.0))*100.0)
    if(obj_x.db.trans["exist"] == 1 and obj_x.db.trans["damage"] < 1.0):
        table.add_row(constants.system_name[13],unparse.unparse_percent(obj_x.db.trans["damage"]),unparse.unparse_damage(obj_x.db.trans["damage"]),(1 - obj_x.db.trans["damage"]) * constants.repair_mult[13] * (1.0 + (obj_x.db.structure["max_structure"]/10.0))*100.0)
    if(obj_x.db.engine["warp_exist"] == 1 and obj_x.db.engine["warp_damage"] < 1.0):
        table.add_row(constants.system_name[14],unparse.unparse_percent(obj_x.db.engine["warp_damage"]),unparse.unparse_damage(obj_x.db.engine["warp_damage"]),(1 - obj_x.db.engine["warp_damage"]) * constants.repair_mult[14] * (1.0 + (obj_x.db.structure["max_structure"]/10.0))*100.0)
    buffer += str(table) + "\n"
    buffer += format.l_line
    buffer += "|cRepair Capacity|w: {:.3f} ({:d}) units: {:s}\n".format(obj.db.structure["repair"],int(obj.db.structure["max_repair"]),unparse.unparse_percent_3(obj.db.structure["repair"] / obj.db.structure["max_repair"]))
    buffer += format.l_end

    alerts.notify(self,buffer)
    obj.db.status["time"] = obj.db.move["time"]
    return 1