"""
All the alerts go here!
"""
from evennia.utils.search import search_object,search_tag
from world import constants,utils,unparse
from evennia.utils import evtable
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
    if (freq < constants.MIN_COMMS_FREQUENCY or freq > MAX_COMMS_FREQUENCY):
        console_message(self,["communication"],ansi_red("#-1 BAD FREQUENCY VALUE"))
    if (range <= 0):
        console_message(self,["communication"],ansi_red("#-1 BAD RANGE VALUE"))
    #sending the message here...
    space_obj = search_tag(category="space_object",tag=constants.SHIP_ATTR_NAME)
    for obj in space_obj:
        if(obj.db.status["active"]):
            if(obj.db.structure["type"] is not None):
                if(obj.db.location == self.db.location):
                    if(self.name != obj.name):
                        if(utils.sdb2range(self,obj) < range):
                            if(obj.db.language != language):
                                message = rplanguage.obfuscate_language(message,language=language,level=1.0)
                            if(code):
                                message = encrypt_message(code,message)
                            do_console_notify(obj,["communication"],"[|b"+self.name+"|n]: " + message)

def console_message(self,console,text):
    for console_name in console:
        console_obj = search_object(self.name + "-" + console_name)
        if (console_obj.count() > 0):
            console_obj[0].msg_contents(text)
        else:
           self.msg(text)
           return

def do_console_notify(self,console,text):
    console_message(self,console,text)

def do_all_console_notify(self,text):
    for console_name in constants.CONSOLE_LIST:
        console_obj = search_object(self.name + "-" + console_name)
        if (console_obj.count() > 0):
            console_obj[0].msg_contents(text)
        else:
           self.msg(text)
    
def do_ship_notify(self,text):
    do_all_console_notify(self,text)
    
def do_space_notify_one(self,console,text):
    space_obj = search_tag(category="space_object",tag=constants.SHIP_ATTR_NAME)
    for obj in space_obj:
        if(obj.db.status["active"]):
            if(obj.db.structure["type"] is not None):
                if(obj.db.location == self.db.location):
                    if(self.name != obj.name):
                        contact = utils.sdb2contact(obj,self)
                        if (contact != constants.SENSOR_FAIL):
                            console.message(obj,console,"|b[|c"+self.name + " " + text + "|b]|n")

def do_space_notify_two(self,obj2,console,text):
    space_obj = search_tag(category="space_object",tag=constants.SHIP_ATTR_NAME)
    for obj in space_obj:
        if(obj.db.status["active"]):
            if(obj.db.structure["type"] is not None):
                if(obj.db.location == self.db.location):
                    if(self.name != obj.name and obj2.name != obj.name):
                        contact1 = utils.sdb2contact(obj,self)
                        contact2 = utils.sdb2contact(obj,obj2)
                        if (contact1 != constants.SENSOR_FAIL or contact2 != constants.SENSOR_FAIL):
                            console.message(obj,console,"|b[|c"+self.name + " " + text + "|b]|n")

def ship_cloak_online(self):
    do_ship_notify(self, ansi_notify(self.name + " engages its cloaking device."));
    do_space_notify_one(self, ["helm","tactical","science"], "engages its cloaking device")

def ship_cloak_offline(self):
    do_ship_notify(self, ansi_notify(self.name + " disengages its cloaking device."));
    do_space_notify_one(self, ["helm","tactical","science"], "disengages its cloaking device")

def exit_empire(self):
    console_message(self,["helm"],ansi_alert("Exiting " + self.db.move["empire"] + " space"))

def enter_empire(self):
    console_message(self,["helm"],ansi_warn("Entering " + self.db.move["empire"] + " space"))
    
def border_cross(self, type):
    #Check if we are actually moving, and not creating ships
    if (utils.sdb2true_speed(self) == 0.0):
        return
    if (self.move["out"] != 0.0):
        space_obj = search_tag(category="space_object",tag=constants.SHIP_ATTR_NAME)
        for obj in space_obj:
            if(obj.db.status["active"]):
                if(obj.db.structure["type"] is not None):
                    if(obj.db.space == self.db.space):
                        if(obj.db.empire == self.db.empire):
                            if (obj.name != self.name):
                                if (utils.sdb2range(self,obj) < constants.MAX_NOTIFICATION_DISTANCE):
                                    if (type):
                                        do_console_notify(self, ansi_notify(self.name + " disengages its cloaking device."))

def report_eng_power(self,obj):
    table = evtable.EvTable("|cAllocation|n", "|cEPS Power|n", "|cPercentage|n")
    buffer = "|y|[bEngineering Allocation Report|n\n"
    table.add_row("|cTotal EPS",unparse.unparse_power(obj.db.power["total"]),"100%")
    table.add_row("|cTotal Helm",unparse.unparse_power(obj.db.alloc["helm"] * obj.db.power["total"]),unparse.unparse_percent(obj.db.alloc["helm"]),ansi_rainbow_scale(obj.db.alloc["helm"],35))
    table.add_row("|cTotal Tactical",unparse.unparse_power(obj.db.alloc["tactical"] * obj.db.power["total"]),unparse.unparse_percent(obj.db.alloc["tactical"]),ansi_rainbow_scale(obj.db.alloc["tactical"],35))
    table.add_row("|cTotal Operations",unparse.unparse_power(obj.db.alloc["operations"] * obj.db.power["total"]),unparse.unparse_percent(obj.db.alloc["operations"]),ansi_rainbow_scale(obj.db.alloc["operations"],35))
    console_message(self,["engineering"], buffer + str(table) + "|n")
    return 1

def report_helm_power(self,obj):
    table = evtable.EvTable("|cAllocation|n", "|cEPS Power|n", "|cPercentage|n")
    buffer = "|y|[bHelm/Navigation Allocation Report|n\n"
    table.add_row("|cTotal Helm",unparse.unparse_power(obj.db.alloc["helm"] * obj.db.power["total"]),unparse.unparse_percent(obj.db.alloc["helm"]))
    table.add_row("|cMovement",unparse.unparse_power(obj.db.alloc["movement"] * obj.db.power["total"]),unparse.unparse_percent(obj.db.alloc["movement"]),ansi_rainbow_scale(obj.db.alloc["movement"],35))
    table.add_row("|cShields",unparse.unparse_power(obj.db.alloc["shields"] * obj.db.power["total"]),unparse.unparse_percent(obj.db.alloc["shields"]),ansi_rainbow_scale(obj.db.alloc["shields"],35))
    for i in range(constants.MAX_SHIELD_NAME):
        table.add_row("|c"+ unparse.unparse_shield(i),unparse.unparse_power(obj.db.alloc["shield"][i] * obj.db.power["total"]),unparse.unparse_percent(obj.db.alloc["shield"][i]),ansi_rainbow_scale(obj.db.alloc["shield"][i],35))
    table.add_row("|c"+ constants.cloak_name[obj.db.cloak["exist"]] + "|n",unparse.unparse_power(obj.db.alloc["cloak"] * obj.db.power["total"]),unparse.unparse_percent(obj.db.alloc["cloak"]),ansi_rainbow_scale(obj.db.alloc["cloak"],35))
    console_message(self,["helm","engineering"], buffer + str(table) + "|n")
    return 1

def report_tact_power(self,obj):
    table = evtable.EvTable("|cAllocation|n","|cEPS Power|n", "|cPercentage|n")
    buffer = "|y|[bTactical/Weapon Allocation Report|n\n"
    table.add_row("|cTotal Tactical",unparse.unparse_power(obj.db.alloc["tactical"] * obj.db.power["total"]),unparse.unparse_percent(obj.db.alloc["tactical"]))
    table.add_row("|cBeam Weapons",unparse.unparse_power(obj.db.alloc["beams"] * obj.db.power["total"]),unparse.unparse_percent(obj.db.alloc["beams"]),ansi_rainbow_scale(obj.db.alloc["beams"],35))
    table.add_row("|cMissile Weapons ",unparse.unparse_power(obj.db.alloc["missiles"] * obj.db.power["total"]),unparse.unparse_percent(obj.db.alloc["missiles"]),ansi_rainbow_scale(obj.db.alloc["missiles"],35))
    table.add_row("|cEW Systems",unparse.unparse_power(obj.db.alloc["sensors"] * obj.db.power["total"]),unparse.unparse_percent(obj.db.alloc["sensors"]),ansi_rainbow_scale(obj.db.alloc["sensors"],35))
    table.add_row("|cECM",unparse.unparse_power(obj.db.alloc["ecm"] * obj.db.power["total"]),unparse.unparse_percent(obj.db.alloc["ecm"]),ansi_rainbow_scale(obj.db.alloc["ecm"],35))
    table.add_row("|cECCM",unparse.unparse_power(obj.db.alloc["eccm"] * obj.db.power["total"]),unparse.unparse_percent(obj.db.alloc["eccm"]),ansi_rainbow_scale(obj.db.alloc["ecm"],35))
    console_message(self,["engineering","science","tactical"], buffer + str(table) + "|n")
    return 1

def report_ops_power(self,obj):
    table = evtable.EvTable("|cAllocation|n", "|cEPS Power|n", "|cPercentage|n")
    buffer = "|y|[bOperations Allocation Report|n\n"
    table.add_row("|cTotal Operations",unparse.unparse_power(obj.db.alloc["operations"] * obj.db.power["total"]),unparse.unparse_percent(obj.db.alloc["operations"]))
    table.add_row("|cTransporters",unparse.unparse_power(obj.db.alloc["transporters"] * obj.db.power["total"]),unparse.unparse_percent(obj.db.alloc["transporters"]),ansi_rainbow_scale(obj.db.alloc["transporters"],35))
    table.add_row("|cTractors",unparse.unparse_power(obj.db.alloc["tractors"] * obj.db.power["total"]),unparse.unparse_percent(obj.db.alloc["tractors"]),ansi_rainbow_scale(obj.db.alloc["tractors"],35))
    table.add_row("|cMiscellaneous",unparse.unparse_power(obj.db.alloc["miscellaneous"] * obj.db.power["total"]),unparse.unparse_percent(obj.db.alloc["miscellaneous"]),ansi_rainbow_scale(obj.db.alloc["miscellaneous"],35))
    console_message(self,["engineering","damage","operation"], buffer + str(table) + "|n")
    return 1
    
def report_shield_power(self,obj):
    table = evtable.EvTable("|cAllocation|n", "|cEPS Power|n", "|cPercentage|n")
    buffer = "|y|[bShield Allocation Report|n\n"
    table.add_row("|cShields|n",unparse.unparse_power(obj.db.alloc["shields"] * obj.db.power["total"]),unparse.unparse_percent(obj.db.alloc["shields"]))
    for i in range(constants.MAX_SHIELD_NAME):
        table.add_row("|c"+ unparse.unparse_shield(i)+"|n",unparse.unparse_power(obj.db.alloc["shield"][i] * obj.db.power["total"]),unparse.unparse_percent(obj.db.alloc["shield"][i]),ansi_rainbow_scale(obj.db.alloc["shield"][i],35))
    table.add_row("|c" + constants.cloak_name[obj.db.cloak["exist"]] + "|n",unparse.unparse_power(obj.db.alloc["cloak"] * obj.db.power["total"]),unparse.unparse_percent(obj.db.alloc["cloak"]),ansi_rainbow_scale(obj.db.alloc["cloak"],35))
    console_message(self,["helm","engineering"], buffer + str(table)+"|n")
    return 1

def report_sensor_power(self,obj):
    table = evtable.EvTable("|cAllocation", "|cEPS Power|n", "|cPercentage|n")
    buffer = "|y|[bEW Systems Allocation Report\n"
    table.add_row("|cEW Systems",unparse.unparse_power(obj.db.alloc["sensors"] * obj.db.power["total"]),unparse.unparse_percent(obj.db.alloc["sensors"]))
    table.add_row("|cECM",unparse.unparse_power(obj.db.alloc["ecm"] * obj.db.power["total"]),unparse.unparse_percent(obj.db.alloc["ecm"]),ansi_rainbow_scale(obj.db.alloc["ecm"],35))
    table.add_row("|cECCM",unparse.unparse_power(obj.db.alloc["eccm"] * obj.db.power["total"]),unparse.unparse_percent(obj.db.alloc["eccm"]),ansi_rainbow_scale(obj.db.alloc["eccm"],35))
    console_message(self,["engineering","science","tactical"], buffer + str(table)+"|n")
    return 1

def pitch(self):
    #TODO
    console_message(self,["helm"],"New pitch set")
    return 1

def roll(self):
    #TODO
    console_message(self,["helm"],"New roll set")
    return 1

def speed_warp(self):
    #TODO
    console_message(self,["helm"],"Speed enters warp")
    return 1

def ship_enter_warp(self):
    #TODO
    console_message(self,["helm"],"Ship enters warp")
    return 1

def ship_exit_warp(self):
    #TODO
    console_message(self,["helm"],"Ship exits warp")
    return 1


def speed_exit_warp(self):
    #TODO
    console_message(self,["helm"],"Speed exits warp")
    return 1

def speed_stop(self):
    #TODO
    console_message(self,["helm"],"Speed has stopped")
    return 1

def enter_quadrant(self):
    #TODO
    console_message(self,["helm"],"Entering quadrant")
    return 1


def speed_impulse(self):
    #TODO
    console_message(self,["helm"],"Speed enters impulse")
    return 1

def yaw(self):
    #TODO
    console_message(self,["helm"],"New yaw set")
    return 1

def main_balance(self):
    #TODO
    console_message(self,["engineering"],"New main_balance set")
    return 1

def max_repair(self):
    #TODO
    console_message(self,["engineering"],"Maximum repairs")
    return 1

def anti_runout(self):
    #TODO
    console_message(self,["engineering"],"Antimatter runout!")
    return 1

def deut_runout(self):
    #TODO
    console_message(self,["engineering"],"Deeuterium runout!")
    return 1


def batt_runout(self):
    #TODO
    console_message(self,["engineering"],"Battery runout!")
    return 1

def main_overload(self):
    #TODO
    console_message(self,["engineering"],"Main overload!")
    return 1

def aux_overload(self):
    #TODO
    console_message(self,["engineering"],"Aux overload!")
    return 1