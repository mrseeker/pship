"""
Handles all engine-related commands
"""

from evennia import default_cmds
from world import set as setter
from world import alerts, errors,unparse,constants
from world import utils as WorldUtils
from evennia import CmdSet
from evennia.utils.search import search_object
from evennia.utils import evtable, utils

class EngineeringCmdSet(CmdSet):
        
        key = "EngineeringCmdSet"
    
        def at_cmdset_creation(self):
            self.add(CmdEngine())
            self.add(CmdAlloc())

class EngineeringFighterCmdSet(CmdSet):
        key = "EngineeringFighterCmdSet"

        def at_cmdset_creation(self):
            self.add(CmdEngine())
            self.add(CmdAlloc_Fighter())

class CmdAlloc_Fighter(default_cmds.MuxCommand):
    """
    Commands related to the allocation of the engine.

    Usage: alloc <command> <value>
    
    Command list:
    status - Gives a full status of the allocations
    HTO - Sets the allocation of the Helm, Tactical and Operations
    MSC - Sets the allocation of the Movement, Shields and Cloak
    shield - Allocation of the shields (forward, starboard, aft, port, dorsal, ventral)
    main - Allocation of the M/A reactor
    aux - Allocation of the Fusion reactor
    batt - Allocation of the batteries
    """

    key = "alloc"
    help_category = "Engineering"
    
    def func(self):
        self.args = self.args.split(" ")
        caller = self.caller
        obj_x = search_object(self.caller.location)[0]
        obj = search_object(obj_x.db.ship)[0]
        if(errors.error_on_console(self.caller,obj)):
                return 0
        if (self.args[0] == "HTO" and len(self.args) == 4):
            setter.do_set_eng_alloc(self.caller,float(self.args[1]),float(self.args[2]),float(self.args[3]),obj)
        elif (self.args[0] == "main" and len(self.args) == 2):
            setter.do_set_main_reactor(self.caller,float(self.args[1]),obj)
        elif (self.args[0] == "aux" and len(self.args) == 2):
            setter.do_set_aux_reactor(self.caller,float(self.args[1]),obj)
        elif (self.args[0] == "batt" and len(self.args) == 2):
            setter.do_set_battery(self.caller,float(self.args[1]),obj)
        if (self.args[0] == "MSC" and len(self.args) == 4):
            setter.do_set_helm_alloc(self.caller,float(self.args[1]),float(self.args[2]),float(self.args[3]),obj)
        elif (self.args[0] == "shield" and len(self.args) == 7):
            setter.do_set_shield_alloc(self.caller,float(self.args[1]),float(self.args[2]),float(self.args[3]),float(self.args[4]),float(self.args[5]),float(self.args[6]),obj)
        elif (self.args[0] == "status"):
            #Give a full report back
            buffer = "|y|[bTotal Allocation Report|n\n"
            table = evtable.EvTable("|cAllocation|n","|cEPS Power|n","|cPercentage|n","")
            table.add_row("|cTotal EPS|n",unparse.unparse_power(obj.db.power["total"]),unparse.unparse_percent(1.0))
            table.add_row("|cTotal Helm|n",unparse.unparse_power(obj.db.alloc["helm"]*obj.db.power["total"]),unparse.unparse_percent(obj.db.alloc["helm"]))
            table.add_row("|cMovement|n",unparse.unparse_power(obj.db.alloc["movement"]*obj.db.power["total"]),unparse.unparse_percent(obj.db.alloc["movement"]),alerts.ansi_rainbow_scale(obj.db.alloc["movement"],35))
            table.add_row("|cShields|n",unparse.unparse_power(obj.db.alloc["shields"]*obj.db.power["total"]),unparse.unparse_percent(obj.db.alloc["shields"]))
            for i in range(constants.MAX_SHIELD_NAME):
                table.add_row("|c"+unparse.unparse_shield(i) + "|n",unparse.unparse_power(obj.db.alloc["shield"][i]*obj.db.power["total"]),unparse.unparse_percent(obj.db.alloc["shield"][i]),alerts.ansi_rainbow_scale(obj.db.alloc["shield"][i],35))
            table.add_row("|c"+constants.cloak_name[obj.db.cloak["exist"]]+"|n",unparse.unparse_power(obj.db.alloc["cloak"]*obj.db.power["total"]),unparse.unparse_percent(obj.db.alloc["cloak"]),alerts.ansi_rainbow_scale(obj.db.alloc["cloak"],35))
            table.add_row("|cTotal Tactical|n",unparse.unparse_power(obj.db.alloc["tactical"]*obj.db.power["total"]),unparse.unparse_percent(obj.db.alloc["tactical"]))
            table.add_row("|cBeam Weapons|n",unparse.unparse_power(obj.db.alloc["beams"]*obj.db.power["total"]),unparse.unparse_percent(obj.db.alloc["beams"]),alerts.ansi_rainbow_scale(obj.db.alloc["beams"],35))
            table.add_row("|cMissile Weapons|n",unparse.unparse_power(obj.db.alloc["missiles"]*obj.db.power["total"]),unparse.unparse_percent(obj.db.alloc["missiles"]),alerts.ansi_rainbow_scale(obj.db.alloc["missiles"],35))
            table.add_row("|cEW Systems|n",unparse.unparse_power(obj.db.alloc["sensors"]*obj.db.power["total"]),unparse.unparse_percent(obj.db.alloc["sensors"]))
            table.add_row("|cECM|n",unparse.unparse_power(obj.db.alloc["ecm"]*obj.db.power["total"]),unparse.unparse_percent(obj.db.alloc["ecm"]),alerts.ansi_rainbow_scale(obj.db.alloc["ecm"],35))
            table.add_row("|cECCM|n",unparse.unparse_power(obj.db.alloc["eccm"]*obj.db.power["total"]),unparse.unparse_percent(obj.db.alloc["eccm"]),alerts.ansi_rainbow_scale(obj.db.alloc["eccm"],35))
            table.add_row("|cBeam Weapons|n",unparse.unparse_power(obj.db.alloc["beams"]*obj.db.power["total"]),unparse.unparse_percent(obj.db.alloc["beams"]),alerts.ansi_rainbow_scale(obj.db.alloc["beams"],35))
            table.add_row("|cTotal Operations|n",unparse.unparse_power(obj.db.alloc["operations"]*obj.db.power["total"]),unparse.unparse_percent(obj.db.alloc["operations"]))
            table.add_row("|cTransporters|n",unparse.unparse_power(obj.db.alloc["transporters"]*obj.db.power["total"]),unparse.unparse_percent(obj.db.alloc["transporters"]),alerts.ansi_rainbow_scale(obj.db.alloc["transporters"],35))
            table.add_row("|cTractors|n",unparse.unparse_power(obj.db.alloc["tractors"]*obj.db.power["total"]),unparse.unparse_percent(obj.db.alloc["tractors"]),alerts.ansi_rainbow_scale(obj.db.alloc["tractors"],35))
            table.add_row("|cMiscellaneous|n",unparse.unparse_power(obj.db.alloc["miscellaneous"]*obj.db.power["total"]),unparse.unparse_percent(obj.db.alloc["miscellaneous"]),alerts.ansi_rainbow_scale(obj.db.alloc["miscellaneous"],35))
            alerts.notify(self.caller,buffer + str(table) + "\n")
        else:    
            self.caller.msg("Command not found: " + str(self.args))

class CmdAlloc(default_cmds.MuxCommand):
    """
    Commands related to the allocation of the engine.

    Usage: alloc <command> <value>
    
    Command list:
    status - Gives a full status of the allocations
    HTO - Sets the allocation of the Helm, Tactical and Operations
    main - Allocation of the M/A reactor
    aux - Allocation of the Fusion reactor
    batt - Allocation of the batteries
    """

    key = "alloc"
    help_category = "Engineering"
    
    def func(self):
        self.args = self.args.split(" ")
        caller = self.caller
        obj_x = search_object(self.caller.location)[0]
        obj = search_object(obj_x.db.ship)[0]
        if(errors.error_on_console(self.caller,obj)):
                return 0
        if (self.args[0] == "HTO" and len(self.args) == 4):
            setter.do_set_eng_alloc(self.caller,float(self.args[1]),float(self.args[2]),float(self.args[3]),obj)
        elif (self.args[0] == "main" and len(self.args) == 2):
            setter.do_set_main_reactor(self.caller,float(self.args[1]),obj)
        elif (self.args[0] == "aux" and len(self.args) == 2):
            setter.do_set_aux_reactor(self.caller,float(self.args[1]),obj)
        elif (self.args[0] == "batt" and len(self.args) == 2):
            setter.do_set_battery(self.caller,float(self.args[1]),obj)
        elif (self.args[0] == "status"):
            #Give a full report back
            buffer = "|y|[bTotal Allocation Report|n\n"
            table = evtable.EvTable("|cAllocation|n","|cEPS Power|n","|cPercentage|n","")
            table.add_row("|cTotal EPS|n",unparse.unparse_power(obj.db.power["total"]),unparse.unparse_percent(1.0))
            table.add_row("|cTotal Helm|n",unparse.unparse_power(obj.db.alloc["helm"]*obj.db.power["total"]),unparse.unparse_percent(obj.db.alloc["helm"]))
            table.add_row("|cMovement|n",unparse.unparse_power(obj.db.alloc["movement"]*obj.db.power["total"]),unparse.unparse_percent(obj.db.alloc["movement"]),alerts.ansi_rainbow_scale(obj.db.alloc["movement"],35))
            table.add_row("|cShields|n",unparse.unparse_power(obj.db.alloc["shields"]*obj.db.power["total"]),unparse.unparse_percent(obj.db.alloc["shields"]))
            for i in range(constants.MAX_SHIELD_NAME):
                table.add_row("|c"+unparse.unparse_shield(i) + "|n",unparse.unparse_power(obj.db.alloc["shield"][i]*obj.db.power["total"]),unparse.unparse_percent(obj.db.alloc["shield"][i]),alerts.ansi_rainbow_scale(obj.db.alloc["shield"][i],35))
            table.add_row("|c"+constants.cloak_name[obj.db.cloak["exist"]]+"|n",unparse.unparse_power(obj.db.alloc["cloak"]*obj.db.power["total"]),unparse.unparse_percent(obj.db.alloc["cloak"]),alerts.ansi_rainbow_scale(obj.db.alloc["cloak"],35))
            table.add_row("|cTotal Tactical|n",unparse.unparse_power(obj.db.alloc["tactical"]*obj.db.power["total"]),unparse.unparse_percent(obj.db.alloc["tactical"]))
            table.add_row("|cBeam Weapons|n",unparse.unparse_power(obj.db.alloc["beams"]*obj.db.power["total"]),unparse.unparse_percent(obj.db.alloc["beams"]),alerts.ansi_rainbow_scale(obj.db.alloc["beams"],35))
            table.add_row("|cMissile Weapons|n",unparse.unparse_power(obj.db.alloc["missiles"]*obj.db.power["total"]),unparse.unparse_percent(obj.db.alloc["missiles"]),alerts.ansi_rainbow_scale(obj.db.alloc["missiles"],35))
            table.add_row("|cEW Systems|n",unparse.unparse_power(obj.db.alloc["sensors"]*obj.db.power["total"]),unparse.unparse_percent(obj.db.alloc["sensors"]))
            table.add_row("|cECM|n",unparse.unparse_power(obj.db.alloc["ecm"]*obj.db.power["total"]),unparse.unparse_percent(obj.db.alloc["ecm"]),alerts.ansi_rainbow_scale(obj.db.alloc["ecm"],35))
            table.add_row("|cECCM|n",unparse.unparse_power(obj.db.alloc["eccm"]*obj.db.power["total"]),unparse.unparse_percent(obj.db.alloc["eccm"]),alerts.ansi_rainbow_scale(obj.db.alloc["eccm"],35))
            table.add_row("|cBeam Weapons|n",unparse.unparse_power(obj.db.alloc["beams"]*obj.db.power["total"]),unparse.unparse_percent(obj.db.alloc["beams"]),alerts.ansi_rainbow_scale(obj.db.alloc["beams"],35))
            table.add_row("|cTotal Operations|n",unparse.unparse_power(obj.db.alloc["operations"]*obj.db.power["total"]),unparse.unparse_percent(obj.db.alloc["operations"]))
            table.add_row("|cTransporters|n",unparse.unparse_power(obj.db.alloc["transporters"]*obj.db.power["total"]),unparse.unparse_percent(obj.db.alloc["transporters"]),alerts.ansi_rainbow_scale(obj.db.alloc["transporters"],35))
            table.add_row("|cTractors|n",unparse.unparse_power(obj.db.alloc["tractors"]*obj.db.power["total"]),unparse.unparse_percent(obj.db.alloc["tractors"]),alerts.ansi_rainbow_scale(obj.db.alloc["tractors"],35))
            table.add_row("|cMiscellaneous|n",unparse.unparse_power(obj.db.alloc["miscellaneous"]*obj.db.power["total"]),unparse.unparse_percent(obj.db.alloc["miscellaneous"]),alerts.ansi_rainbow_scale(obj.db.alloc["miscellaneous"],35))
            alerts.notify(self.caller,buffer + str(table) + "\n")
        else:    
            self.caller.msg("Command not found: " + str(self.args))

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
            buffer = "|y|[bEngineering Status Report|n\n"
            table = evtable.EvTable("|cName|n","|cValue|n","")
            table.add_row("|cName|n",obj.name)
            table.add_row("|cClass|n",unparse.unparse_class(obj))
            table.add_row("")
            table.add_row("|cSpeed|n",unparse.unparse_movement(obj))
            table.add_row("|cTotal Power|n",unparse.unparse_power(obj.db.power["total"]))
            table.add_row("")
            if (obj.db.engine["warp_exist"] or obj.db.engine["impulse_exist"]):
                if(obj.db.engine["warp_exist"]):
                    table.add_row("|cWarp Cruise|n",str(obj.db.engine["warp_cruise"]))
                if(obj.db.engine["impulse_exist"]):
                    table.add_row("|cImpulse Cruise|n",unparse.unparse_percent_3(obj.db.engine["impulse_cruise"]))
                table.add_row("")
                if(obj.db.engine["warp_exist"]):
                    table.add_row("|cWarp Maximum|n",str(obj.db.engine["warp_max"]))
                if(obj.db.engine["impulse_exist"]):
                    table.add_row("|cImpulse Maximum|n",unparse.unparse_percent_3(obj.db.engine["impulse_max"]))
                table.add_row("")
            if(obj.db.main["exist"] or obj.db.aux["exist"] or obj.db.batt["exist"]):
                if (obj.db.main["exist"] and obj.db.main["gw"]):
                    m = WorldUtils.sdb2max_antimatter(obj)
                    table.add_row("|cAntimatter|n",str(obj.db.fuel["antimatter"]/ 1000000.0) + "/" + str(m / 1000000.0) + " tons (" +unparse.unparse_percent(obj.db.fuel["antimatter"] / m)+ ")",alerts.ansi_stoplight_scale(obj.db.fuel["antimatter"]/m,25))
                if (obj.db.aux["exist"] and obj.db.aux["gw"]):
                    m = WorldUtils.sdb2max_deuterium(obj)
                    table.add_row("|cDeuterium|n",str(obj.db.fuel["deuterium"]/ 1000000.0) + "/" + str(m / 1000000.0) + " tons (" +unparse.unparse_percent(obj.db.fuel["deuterium"] / m)+ ")",alerts.ansi_stoplight_scale(obj.db.fuel["deuterium"]/m,25))
                if (obj.db.batt["exist"] and obj.db.batt["gw"]):
                    m = WorldUtils.sdb2max_reserves(obj)
                    table.add_row("|cReserves|n",str(obj.db.fuel["reserves"]/ 3600.0) + "/"+ str(m / 3600.0) + " GW^H (" +unparse.unparse_percent(obj.db.fuel["reserves"] / m)+ ")",alerts.ansi_stoplight_scale(obj.db.fuel["reserves"]/m,25))
            buffer += str(table)
            alerts.notify(self.caller,buffer)        
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
        alerts.console_message(self.caller,["engineering"],alerts.ansi_cmd(self.caller.name,"Engine startup complete!"))
        ship_obj.db.engineering["start_sequence"]=0
        setter.do_set_active(self.caller,ship_obj)