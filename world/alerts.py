"""
All the alerts go here!
"""
from evennia.utils.search import search_object
from world import constants

def ansi_warn(text):
    return "|y|[rWARNING: " + text + "|H"

def ansi_alert(text):
    return "|r|[yALERT: " + text + "|H"

def ansi_notify(text):
    return "|w|[GMESSAGE: " + text + "|H"

def ansi_cmd(name,text):
    return "|w|[G"+ name + ": "+ text + "|H"

def ansi_blink(text):
    return "\033[5m" + text

def ansi_red(text):
    return "|r" + text + "|H"

def notify(self,text):
    self.msg(text)

def console_message(self,console,text):
    obj_x = search_object(self.location)[0]
    ship_obj = search_object(obj_x.db.ship)[0]
    for console_name in console:
        console_obj = search_object(ship_obj.name + "-" + console_name)
        if (console_obj.count() > 0):
            console_obj[0].msg_contents(text)
    
def do_all_console_notify(self,text):
    for console_name in constants.CONSOLE_LIST:
        console_obj = search_object(self.name + "-" + console_name)
        if (console_obj.count() > 0):
            console_obj[0].msg_contents(text)
    
def do_ship_notify(self,text):
    self.msg_contents(text)
    do_all_console_notify(self,text)
    
def do_space_notify_one(self,console,text):
    self.msg(text)