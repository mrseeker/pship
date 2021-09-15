"""
All the alerts go here!
"""
from evennia.utils.search import search_object,search_tag
from world import constants,utils

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


def notify(self,text):
    self.msg(text)

def console_message(self,console,text):
    for console_name in console:
        console_obj = search_object(self.name + "-" + console_name)
        if (console_obj.count() > 0):
            console_obj[0].msg_contents(text)
        else:
           self.msg(text)
    
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
