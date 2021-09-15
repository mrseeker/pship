"""
Handles all engine-related commands
"""

from evennia import default_cmds
from world import set as setter
from world import alerts, errors
from evennia import CmdSet, utils
from evennia.utils.search import search_object
from evennia.utils import evtable

class EngineeringCmdSet(CmdSet):
        
        key = "EngineeringCmdSet"
    
        def at_cmdset_creation(self):
            self.add(CmdEngine())

class CmdEngine(default_cmds.MuxCommand):
    """
    Commands related to the proper functioning of the engine.

    Usage: engine <command>
    
    Command list:
    status - Gives the current status of the engine
    start - Starts the M/A reactor
    shutdown - Stops the M/A reactor
    abort - Tries to shut down the current bootup sequence
    eject main/aux <key> - Ejects the main/aux core. Requires Chief Engineer privileges.

    """

    key = "engine"
    help_category = "Engineering"
    
    def func(self):
        self.args = self.args.strip()
        caller = self.caller
        obj_x = search_object(self.caller.location)[0]
        obj = search_object(obj_x.db.ship)[0]
        if not self.args:
            self.caller.msg("You did not enter any commands.")
        elif(self.args == "status"):
            if(errors.error_on_console(self.caller,obj)):
                return 0
            table = evtable.EvTable("Name","In","Out","Power","Condition")
            if (obj.db.main["exist"]):
                table.add_row("Main",obj.db.main["in"],obj.db.main["out"],str(obj.db.main["gw"]) + "GW",str(obj.db.main["damage"]) + "%")
            if (obj.db.aux["exist"]):
                table.add_row("Aux",obj.db.aux["in"],obj.db.aux["out"],str(obj.db.aux["gw"]) + "GW",str(obj.db.aux["damage"]) + "%")
            table.add_row("Battery",obj.db.batt["in"],str(obj.db.batt["out"]) + "GW",obj.db.batt["gw"])
            self.caller.msg("Engine status:")
            self.caller.msg(table)
        elif(self.args == "start"):
            if (self.args == "start" and obj.db.engineering["start_sequence"]==0):
                if (obj.db.structure["type"] == 0):
                    alerts.notify(self, alerts.ansi_red("Space object not loaded."))
                elif (obj.db.status["crippled"] == 2):
                    alerts.notify(self, alerts.ansi_red("Space object destroyed."))
                elif(obj.db.status["active"]):
                    alerts.notify(self, alerts.ansi_red(obj.name + " systems are already active."))
                elif(not obj.db.main["exist"]):
                    alerts.notify(self,alerts.ansi_red(obj.name + " has no M/A reactor."))
                elif(obj.db.main["damage"] <= -1.0):
                    alerts.notify(self,alerts.ansi_red("M/A reactor controls are inoperative."))
                elif(obj.db.fuel["antimatter"] <= 0.0):
                    alerts.notify(self,alerts.ansi_red("There is no antimattter fuel."))
                elif(obj.db.fuel["deuterium"] <= 0.0):
                    alerts.notify(self,alerts.ansi_red("There is no deuterium fuel."))
                else:
                    self.caller.msg("Starting up engines for " + obj.name)
                    alerts.console_message(self.caller,["engineering"],alerts.ansi_notify(self.caller.name + " is starting up the engines... type 'engine abort' to stop the process."))
                    obj.db.engineering["start_sequence"]=1
                    utils.delay(60,self.step1)
            else:
                self.caller.msg("Engines are already starting... type 'engine abort' to stop the process.")
        elif(self.args == "eject main " + obj.db.engineering["override"]):
            alerts.console_message(self.caller,["engineering"],alerts.ansi_alert("Dumping M/A reactor!"))
            alerts.do_all_console_notify(obj,alerts.ansi_alert("M/A reactor is being dumped by engineering!"))
            setter.do_set_main_reactor(self,0.0,obj)
            obj.db.main["exist"] = 0
            #Ejecting core stuff here...
        elif(self.args == "eject aux " + obj.db.engineering["override"]):
            alerts.console_message(self.caller,["engineering"],alerts.ansi_alert("Dumping Fusion reactor!"))
            alerts.do_all_console_notify(obj,alerts.ansi_alert("Fusion reactor is being dumped by engineering!"))
            setter.do_set_aux_reactor(self,0.0,obj)
            obj.db.aux["exist"] = 0
            #Ejecting core stuff here...
                        
        elif(self.args == "abort" and obj.db.engineering["start_sequence"] != 0):
            alerts.console_message(self.caller,["engineering"],alerts.ansi_warn("Aborting... Please stand by..."))
            obj.db.engineering["start_sequence"]=-1
            for i in range(1,11):
                yield(5)
                self.caller.msg("Aborting sequence "+ str(i*10) + "% complete...")
            alerts.console_message(self.caller,["engineering"],alerts.ansi_notify("Restart is now possible."))
            obj.db.engineering["start_sequence"]=0
        elif(self.args == "shutdown" and obj.db.engineering["start_sequence"] == 0 and obj.db.status["active"] == 1):
            self.caller.msg("Shutting down engines for " + obj.name)
            alerts.console_message(self.caller,["engineering"],alerts.ansi_warn("Shutting down engines... type 'engine abort' to stop the process."))
            obj.db.engineering["start_sequence"]=-1
            for i in range(1,10):
                yield(10)
                if(obj.db.engineering["start_sequence"]==0):
                    return
                self.caller.msg("Shutdown sequence "+ str(i*10) + "% complete...")
            setter.do_set_inactive(self.caller,obj)
            alerts.console_message(self.caller,["engineering"],alerts.ansi_notify("Engines have stopped. Restart is now possible."))
            obj.db.engineering["start_sequence"]=0
        elif((self.args == "shutdown" or self.args=="start") and obj.db.engineering["start_sequence"] < 0):
            self.caller.msg(alerts.ansi_red("Shutdown sequence already in progress..."))
        elif((self.args == "shutdown" or self.args=="start") and obj.db.engineering["start_sequence"] > 0):
            self.caller.msg(alerts.ansi_red("Startup sequence already in progress..."))
        else:
            self.caller.msg("Command not found: " + self.args)
    def step1(self):
        obj_x = search_object(self.caller.location)[0]
        ship_obj = search_object(obj_x.db.ship)[0]
        if(ship_obj.db.engineering["start_sequence"]<0):
            return
        alerts.console_message(self.caller,["engineering"],alerts.ansi_cmd(self.caller.name,"System core temp at 2.500.000K"))
        utils.delay(120,self.step2)
        
        do_set_main_reactor
        
    def step2(self):
        obj_x = search_object(self.caller.location)[0]
        ship_obj = search_object(obj_x.db.ship)[0]
        if(ship_obj.db.engineering["start_sequence"]<0):
            return
        alerts.console_message(self.caller,["engineering"],alerts.ansi_cmd(self.caller.name,"Injecting antimatter..."))
        utils.delay(120,self.step3)
        
    def step3(self):
        obj_x = search_object(self.caller.location)[0]
        ship_obj = search_object(obj_x.db.ship)[0]
        if(ship_obj.db.engineering["start_sequence"]<0):
            return
        alerts.console_message(self.caller,["engineering"],alerts.ansi_cmd(self.caller.name,"Building up pressure..."))
        utils.delay(60,self.step4)
    
    def step4(self):
        obj_x = search_object(self.caller.location)[0]
        ship_obj = search_object(obj_x.db.ship)[0]
        if(ship_obj.db.engineering["start_sequence"]<0):
            return
        ship_obj.db.engineering["start_sequence"]=0
        setter.do_set_active(self.caller,ship_obj)