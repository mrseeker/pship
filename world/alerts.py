"""
All the alerts go here!
"""
import random
from evennia.utils.logger import log_msg
from evennia.utils.search import search_object,search_tag
from world import constants,utils,unparse
from evennia.utils import evtable
from evennia.contrib import rplanguage
import base64

def ansi_warn(text):
    return "|y|[rWARNING: " + text + "|n"

def ansi_alert(text):
    return "|r|[yALERT: " + text + "|n"

def ansi_notify(text):
    return "|w|[GMESSAGE: " + text + "|n"

def ansi_cmd(name,text):
    return "|w|[G"+ name + ": "+ text + "|n"

def ansi_blink(text):
    return "\033[5m" + text

def ansi_red(text):
    return "|r" + text + "|n"

def ansi_green(text):
    return "|g" + text + "|n"

def ansi_yellow(text):
    return "|y" + text + "|n"

def ansi_rainbow_scale(a,max):
    color1 = 0
    color2 = 0
    b = int(a * max + 0.5)

    if (max < 5):
        max = 5
    if (max > 75):
        max = 75
    if (b < 0):
        b = 0
    if (b > max):
        b = max

    buffer = "|b["

    for i in range(1,max):
        if (i <= b):
            color1 = (int((((i * 5) / (max + 1)) + 1)))
        else:
            color1 = 0
        if (color1 != color2):
            colors = {1:"|r",2:"|y",3:"|g",4:"|b",5:"|m"}
            buffer += colors.get(color1,"|b")
            color2 = color1;
        if (i <= b):
            buffer += "="
        else:
            buffer += "-"
    buffer += "|b]|n"
    return (buffer)

def ansi_stoplight_scale(a, max):
    color1 = 0
    color2 = 0
    b = int(a * max + 0.5)

    if (max < 5):
        max = 5
    if (max > 75):
        max = 75
    if (b < 0):
        b = 0
    if (b > max):
        b = max

    buffer = "|b["

    for i in range(1,max):
        if (i <= b):
            color1 = (int((((i * 5) / (max + 1)) + 1)))
        else:
            color1 = 0
        if (color1 != color2):
            colors = {1:"|r",2:"|y",3:"|y",4:"|g",5:"|g",6:"|g",7:"|g",8:"|g",9:"|g",10:"|g"}
            buffer += colors.get(color1,"|b")
            color2 = color1;
        if (i <= b):
            buffer += "="
        else:
            buffer += "-"
    buffer += "|b]|n"
    return (buffer)

def ansi_red_scale(a, max):
    color1 = 0
    color2 = 0
    b = int(a * max + 0.5)

    if (max < 5):
        max = 5
    if (max > 75):
        max = 75
    if (b < 0):
        b = 0
    if (b > max):
        b = max

    buffer = "|b["

    for i in range(1,max):
        if (i <= b):
            color1 = 1
        else:
            color1 = 0
        if (color1 != color2):
            colors = {1:"|r"}
            buffer += colors.get(color1,"|b")
            color2 = color1;
        if (i <= b):
            buffer += "="
        else:
            buffer += "-"
    buffer += "|b]|n"
    return (buffer)


def notify(self,text):
    self.msg(text)

def encrypt_message(key,message):
    k_len = len(key)
    k_ints = [ord(i) for i in key]
    txt_ints = [ord(i) for i in message]
    ret_txt = ''
    for i in range(len(txt_ints)):
        adder = k_ints[i % k_len]
        v = (txt_ints[i] - 32 + adder) % 95
        ret_txt += chr(v + 32)
    return base64.b64encode(ret_txt.encode('ascii')).decode('ascii')

def decrypt_message(key,message):
    message = base64.b64decode(message.encode('ascii')).decode('ascii')
    k_len = len(key)
    k_ints = [ord(i) for i in key]
    txt_ints = [ord(i) for i in message]
    ret_txt = ''
    for i in range(len(txt_ints)):
        adder = k_ints[i % k_len]
        adder *= -1
        v = (txt_ints[i] - 32 + adder) % 95
        ret_txt += chr(v + 32)
    return ret_txt


def transmit_message(self,freq,range,code,message,language="default"):
    if (freq < constants.MIN_COMMS_FREQUENCY or freq > constants.MAX_COMMS_FREQUENCY):
        console_message(self,["communication"],ansi_red("#-1 BAD FREQUENCY VALUE"))
    if (range <= 0):
        console_message(self,["communication"],ansi_red("#-1 BAD RANGE VALUE"))
    #sending the message here...
    space_obj = search_tag(constants.SHIP_ATTR_NAME,category="space_object")
    for obj in space_obj:
        if(obj.db.status["active"]):
            if(obj.db.structure["type"] != 0):
                if(obj.db.location == self.db.location):
                    if(self.name != obj.name):
                        if(utils.sdb2range(self,obj) < range):
                            if(obj.db.language != language):
                                message = rplanguage.obfuscate_language(message,language=language,level=1.0)
                            if(code):
                                message = encrypt_message(code,message)
                            do_console_notify(obj,["communication"],"[|b"+self.name+"|n]: " + message)

def console_message(obj,console,text):
    for console_name in console:
        console_obj = search_tag(console_name,category=obj.key.lower())
        if (console_obj.count() > 0):
            for obj in console_obj:
                obj.msg_contents(text)
        else:
            if (console != "bridge"):
                console_message(obj,"bridge",text)
            return

def do_console_notify(obj,console,text):
    console_message(obj,console,text)

def do_all_console_notify(obj,text):
    for console_name in constants.CONSOLE_LIST:
        console_obj = search_tag(console_name,category=obj.key.lower())
        if (console_obj.count() > 0):
            for obj in console_obj:
                if (obj.db.ship == obj.name):
                    obj.msg_contents(text)
    
def do_ship_notify(obj,text):
    do_all_console_notify(obj,text)
    
def do_space_notify_one(obj1,console,text):
    space_obj = search_tag(constants.SHIP_ATTR_NAME,category="space_object")
    for obj in space_obj:
        if(obj.db.status["active"]):
            if(obj.db.structure["type"] != 0):
                if(obj.db.location == obj1.db.location):
                    if(obj1.name != obj.name):
                        contact = utils.sdb2contact(obj,obj1)
                        if (contact != constants.SENSOR_FAIL):
                            console_message(obj,console,"|b[|c"+obj1.name + " " + text + "|b]|n")

def do_space_notify_two(obj1,obj2,console,text):
    space_obj = search_tag(constants.SHIP_ATTR_NAME,category="space_object")
    for obj in space_obj:
        if(obj.db.status["active"]):
            if(obj.db.structure["type"] != 0):
                if(obj.db.location == obj1.db.location):
                    if(obj1.name != obj.name and obj2.name != obj.name):
                        contact1 = utils.sdb2contact(obj,obj1)
                        contact2 = utils.sdb2contact(obj,obj2)
                        if (contact1 != constants.SENSOR_FAIL or contact2 != constants.SENSOR_FAIL):
                            console_message(obj,console,"|b[|c"+obj1.name + " " + text + "|b]|n")

def ship_cloak_online(obj):
    do_ship_notify(obj, ansi_notify(obj.name + " engages its cloaking device."))
    do_space_notify_one(obj, ["helm","tactical","science"], "engages its cloaking device")

def ship_cloak_offline(obj):
    do_ship_notify(obj, ansi_notify(obj.name + " disengages its cloaking device."))
    do_space_notify_one(obj, ["helm","tactical","science"], "disengages its cloaking device")

def exit_empire(obj):
    console_message(obj,["helm"],ansi_alert("Exiting " + unparse.unparse_empire(obj) + " space"))

def enter_empire(obj):
    console_message(obj,["helm"],ansi_warn("Entering " + unparse.unparse_empire(obj) + " space"))
    
def border_cross(obj1, type):
    #Check if we are actually moving, and not creating ships
    if (utils.sdb2true_speed(obj1) == 0.0):
        return
    if (obj1.db.move["out"] != 0.0):
        space_obj = search_tag(constants.SHIP_ATTR_NAME,category="space_object")
        for obj in space_obj:
            if(obj.db.status["active"] == 1):
                if(obj.db.structure["type"] != 0):
                    if(obj.db.space == obj1.db.space):
                        if(obj.db.empire == obj1.db.empire):
                            if (obj.name != obj1.name):
                                if (utils.sdb2range(obj1,obj) < constants.MAX_NOTIFICATION_DISTANCE):
                                    if (type == 1):
                                        do_console_notify(obj, ["helm","science","security"], ansi_notify(f'Inbound border crossing reported at {utils.su2pc(obj1.db.coords["x"] - obj.db.coords["xo"]):.3f} {utils.su2pc(obj1.db.coords["y"] - obj.db.coords["yo"]):.3f} {utils.su2pc(obj1.db.coords["z"] - obj.db.coords["zo"]):.3f}'))
                                    else:
                                        do_console_notify(obj, ["helm","science","security"], ansi_notify(f'Outbound border crossing reported at {utils.su2pc(obj1.db.coords["x"] - obj.db.coords["xo"]):.3f} {utils.su2pc(obj1.db.coords["y"] - obj.db.coords["yo"]):.3f} {utils.su2pc(obj1.db.coords["z"] - obj.db.coords["zo"]):.3f}'))
def report_eng_power(obj):
    table = evtable.EvTable("|cAllocation|n", "|cEPS Power|n", "|cPercentage|n")
    buffer = "|y|[bEngineering Allocation Report|n\n"
    table.add_row("|cTotal EPS",unparse.unparse_power(obj.db.power["total"]),"100%")
    table.add_row("|cTotal Helm",unparse.unparse_power(obj.db.alloc["helm"] * obj.db.power["total"]),unparse.unparse_percent(obj.db.alloc["helm"]),ansi_rainbow_scale(obj.db.alloc["helm"],35))
    table.add_row("|cTotal Tactical",unparse.unparse_power(obj.db.alloc["tactical"] * obj.db.power["total"]),unparse.unparse_percent(obj.db.alloc["tactical"]),ansi_rainbow_scale(obj.db.alloc["tactical"],35))
    table.add_row("|cTotal Operations",unparse.unparse_power(obj.db.alloc["operations"] * obj.db.power["total"]),unparse.unparse_percent(obj.db.alloc["operations"]),ansi_rainbow_scale(obj.db.alloc["operations"],35))
    console_message(obj,["engineering"], buffer + str(table) + "|n")
    return 1

def report_helm_power(obj):
    table = evtable.EvTable("|cAllocation|n", "|cEPS Power|n", "|cPercentage|n")
    buffer = "|y|[bHelm/Navigation Allocation Report|n\n"
    table.add_row("|cTotal Helm",unparse.unparse_power(obj.db.alloc["helm"] * obj.db.power["total"]),unparse.unparse_percent(obj.db.alloc["helm"]))
    table.add_row("|cMovement",unparse.unparse_power(obj.db.alloc["movement"] * obj.db.power["total"]),unparse.unparse_percent(obj.db.alloc["movement"]),ansi_rainbow_scale(obj.db.alloc["movement"],35))
    table.add_row("|cShields",unparse.unparse_power(obj.db.alloc["shields"] * obj.db.power["total"]),unparse.unparse_percent(obj.db.alloc["shields"]),ansi_rainbow_scale(obj.db.alloc["shields"],35))
    for i in range(constants.MAX_SHIELD_NAME):
        table.add_row("|c"+ unparse.unparse_shield(i),unparse.unparse_power(obj.db.alloc["shield"][i] * obj.db.power["total"]),unparse.unparse_percent(obj.db.alloc["shield"][i]),ansi_rainbow_scale(obj.db.alloc["shield"][i],35))
    table.add_row("|c"+ constants.cloak_name[obj.db.cloak["exist"]] + "|n",unparse.unparse_power(obj.db.alloc["cloak"] * obj.db.power["total"]),unparse.unparse_percent(obj.db.alloc["cloak"]),ansi_rainbow_scale(obj.db.alloc["cloak"],35))
    console_message(obj,["helm","engineering"], buffer + str(table) + "|n")
    return 1

def report_tact_power(obj):
    table = evtable.EvTable("|cAllocation|n","|cEPS Power|n", "|cPercentage|n")
    buffer = "|y|[bTactical/Weapon Allocation Report|n\n"
    table.add_row("|cTotal Tactical",unparse.unparse_power(obj.db.alloc["tactical"] * obj.db.power["total"]),unparse.unparse_percent(obj.db.alloc["tactical"]))
    table.add_row("|cBeam Weapons",unparse.unparse_power(obj.db.alloc["beams"] * obj.db.power["total"]),unparse.unparse_percent(obj.db.alloc["beams"]),ansi_rainbow_scale(obj.db.alloc["beams"],35))
    table.add_row("|cMissile Weapons ",unparse.unparse_power(obj.db.alloc["missiles"] * obj.db.power["total"]),unparse.unparse_percent(obj.db.alloc["missiles"]),ansi_rainbow_scale(obj.db.alloc["missiles"],35))
    table.add_row("|cEW Systems",unparse.unparse_power(obj.db.alloc["sensors"] * obj.db.power["total"]),unparse.unparse_percent(obj.db.alloc["sensors"]),ansi_rainbow_scale(obj.db.alloc["sensors"],35))
    table.add_row("|cECM",unparse.unparse_power(obj.db.alloc["ecm"] * obj.db.power["total"]),unparse.unparse_percent(obj.db.alloc["ecm"]),ansi_rainbow_scale(obj.db.alloc["ecm"],35))
    table.add_row("|cECCM",unparse.unparse_power(obj.db.alloc["eccm"] * obj.db.power["total"]),unparse.unparse_percent(obj.db.alloc["eccm"]),ansi_rainbow_scale(obj.db.alloc["ecm"],35))
    console_message(obj,["engineering","science","tactical"], buffer + str(table) + "|n")
    return 1

def report_ops_power(obj):
    table = evtable.EvTable("|cAllocation|n", "|cEPS Power|n", "|cPercentage|n")
    buffer = "|y|[bOperations Allocation Report|n\n"
    table.add_row("|cTotal Operations",unparse.unparse_power(obj.db.alloc["operations"] * obj.db.power["total"]),unparse.unparse_percent(obj.db.alloc["operations"]))
    table.add_row("|cTransporters",unparse.unparse_power(obj.db.alloc["transporters"] * obj.db.power["total"]),unparse.unparse_percent(obj.db.alloc["transporters"]),ansi_rainbow_scale(obj.db.alloc["transporters"],35))
    table.add_row("|cTractors",unparse.unparse_power(obj.db.alloc["tractors"] * obj.db.power["total"]),unparse.unparse_percent(obj.db.alloc["tractors"]),ansi_rainbow_scale(obj.db.alloc["tractors"],35))
    table.add_row("|cMiscellaneous",unparse.unparse_power(obj.db.alloc["miscellaneous"] * obj.db.power["total"]),unparse.unparse_percent(obj.db.alloc["miscellaneous"]),ansi_rainbow_scale(obj.db.alloc["miscellaneous"],35))
    console_message(obj,["engineering","damage","operation"], buffer + str(table) + "|n")
    return 1
    
def report_shield_power(obj):
    table = evtable.EvTable("|cAllocation|n", "|cEPS Power|n", "|cPercentage|n")
    buffer = "|y|[bShield Allocation Report|n\n"
    table.add_row("|cShields|n",unparse.unparse_power(obj.db.alloc["shields"] * obj.db.power["total"]),unparse.unparse_percent(obj.db.alloc["shields"]))
    for i in range(constants.MAX_SHIELD_NAME):
        table.add_row("|c"+ unparse.unparse_shield(i)+"|n",unparse.unparse_power(obj.db.alloc["shield"][i] * obj.db.power["total"]),unparse.unparse_percent(obj.db.alloc["shield"][i]),ansi_rainbow_scale(obj.db.alloc["shield"][i],35))
    table.add_row("|c" + constants.cloak_name[obj.db.cloak["exist"]] + "|n",unparse.unparse_power(obj.db.alloc["cloak"] * obj.db.power["total"]),unparse.unparse_percent(obj.db.alloc["cloak"]),ansi_rainbow_scale(obj.db.alloc["cloak"],35))
    console_message(obj,["helm","engineering"], buffer + str(table)+"|n")
    return 1

def report_sensor_power(obj):
    table = evtable.EvTable("|cAllocation", "|cEPS Power|n", "|cPercentage|n")
    buffer = "|y|[bEW Systems Allocation Report\n"
    table.add_row("|cEW Systems",unparse.unparse_power(obj.db.alloc["sensors"] * obj.db.power["total"]),unparse.unparse_percent(obj.db.alloc["sensors"]))
    table.add_row("|cECM",unparse.unparse_power(obj.db.alloc["ecm"] * obj.db.power["total"]),unparse.unparse_percent(obj.db.alloc["ecm"]),ansi_rainbow_scale(obj.db.alloc["ecm"],35))
    table.add_row("|cECCM",unparse.unparse_power(obj.db.alloc["eccm"] * obj.db.power["total"]),unparse.unparse_percent(obj.db.alloc["eccm"]),ansi_rainbow_scale(obj.db.alloc["eccm"],35))
    console_message(obj,["engineering","science","tactical"], buffer + str(table)+"|n")
    return 1

def write_spacelog(self,obj,text):
    log_msg("SPACE {:s} - {:s} : {:s}".format(self.name,obj.name,text))
    return 1

def pitch(obj):
    console_message(obj,["helm"],"Pitch now {:.3f} degrees".format(obj.db.course["pitch_out"]))
    return 1

def roll(obj):
    console_message(obj,["helm"],"Roll now {:.3f} degrees".format(obj.db.course["roll_out"]))
    return 1

def speed_warp(obj):
    console_message(obj,["engineering","helm"],ansi_alert("Speed now warp {:.6f}".format(obj.db.move["out"])))
    return 1

def ship_enter_warp(obj):
    do_ship_notify(obj,"{:s} shifts into warp.".format(obj.name))
    return 1

def ship_exit_warp(obj):
    do_ship_notify(obj,"{:s} drops out of warp.".format(obj.name))
    return 1

def speed_stop(obj):
    console_message(obj,["engineering","helm"],ansi_alert("Speed now full stop"))
    return 1

def enter_quadrant(obj):
    console_message(obj,["helm"],ansi_alert("Entering {:s} quadrant".format(unparse.unparse_quadrant(obj))))
    return 1

def speed_impulse(obj):
    console_message(obj,["helm"],ansi_alert("Speed now {:.3f}% impulse".format(obj.db.move["out"] * 100.0)))
    return 1

def yaw(obj):
    console_message(obj,["helm"],"Yaw now {:.3f} degrees".format(obj.db.course["yaw_out"]))
    return 1

def main_balance(obj):
    console_message(obj,["engineering"],ansi_alert("M/A reactor balanced at {:.3f}%".format(obj.db.main["out"] * 100.0)))
    return 1

def aux_balance(obj):
    console_message(obj,["engineering"],ansi_alert("Fusion reactor balanced at {:.3f}%".format(obj.db.aux["out"] * 100.0)))
    return 1

def batt_balance(obj):
    console_message(obj,["engineering"],ansi_alert("Batteries set at {:.3f}%".format(obj.db.batt["out"] * 100.0)))
    return 1

def max_repair(obj):
    console_message(obj,["damage"],ansi_alert("Repair capacity maximized"))
    return 1

def anti_runout(obj):
    console_message(obj,["engineering"],ansi_warn("ANTIMATTER DEPLETION: M/A reactor now offline"))
    return 1

def deut_runout(obj):
    console_message(obj,["engineering"],ansi_warn("DEUTERIUM DEPLETION: All reactors now offline"))
    return 1

def batt_balance(obj):
    console_message(obj,["engineering"],ansi_alert("Batteries set at {:.3f}%".format(obj.db.batt["out"] * 100.0)))

def batt_runout(obj):
    console_message(obj,["engineering"],ansi_warn("BATTERY DEPLETION: Batteries now offline"))
    return 1

def main_overload(obj):
    do_all_console_notify(obj,ansi_warn("M/A REACTOR CORE BREACH IN PROGRESS"))
    return 1

def aux_overload(obj):
    do_all_console_notify(obj,ansi_warn("FUSION REACTOR CORE BREACH IN PROGRESS"))
    return 1

def ship_hurt(obj):
    if(obj.db.structure["type"] == 1 or obj.db.structure["type"] == 2):
        do_ship_notify(obj,"{:s} rocks violently from an impact.".format(obj.name))    
    elif (obj.db.structure["type"] == 3 and random.random(0,10) == 1):
        do_ship_notify(obj,"{:s} trembles from a surface impact.".format(obj.name))
	return 1

def ship_hit(obj):
    if(obj.db.structure["type"] == 1 or obj.db.structure["type"] == 2):
        do_ship_notify(obj,"{:s} shudders from an impact.".format(obj.name))    
    return 1
