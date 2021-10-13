"""
Handles all helm-related commands
"""

from evennia import default_cmds
from world import set as setter
from world import alerts, errors,unparse, utils,constants
from evennia import CmdSet
from evennia.utils.search import search_object
from evennia.utils import evtable

class HelmCmdSet(CmdSet):
        
        key = "HelmCmdSet"
        def at_cmdset_creation(self):
            self.add(CmdCoords())
            self.add(CmdEngage())
            self.add(CmdStatus())

class FighterCmdSet(CmdSet):
        key = "FighterCmdSet"
        
        def at_cmdset_creation(self):
            self.add(CmdCoords())
            self.add(CmdEngage())
            self.add(CmdStatus_Fighter())

class CmdStatus_Fighter(default_cmds.MuxCommand):
    """
    Status of various systems

    Usage: status
    
    Command list:
    Does not have any commands
    """

    key = "status"
    help_category = "Helm"

    def func(self):
        self.args = self.args.strip()
        self.args = self.args.split(" ")
        caller = self.caller
        obj_x = search_object(self.caller.location)[0]
        obj = search_object(obj_x.db.ship)[0]
        if(errors.error_on_console(self.caller,obj)):
            return 0
        buffer = "|y|[bCondensed Status Report|n\n"
        buffer += "|cName:|n "+ obj.name + " "
        buffer += "|cClass:|n " + unparse.unparse_class(obj) + "\n"
        buffer += "|cVisibility:|n " + unparse.unparse_percent_3(obj.db.sensor["visibility"]) + " "
        buffer += "|cCochranes:|n " + str(obj.db.move["cochranes"]) + "\n"
        buffer += "|cCourse:|n " + unparse.unparse_course(obj) + " "
        buffer += "|cTotal Power:|n " + unparse.unparse_power(obj.db.power["total"]) + "\n"
        buffer += "|cSpeed:|n " + unparse.unparse_movement(obj) + " "
        buffer += "|cVelocity:|n " + unparse.unparse_velocity(obj) + "\n"
        if (obj.db.main["exist"] or obj.db.aux["exist"] or obj.db.batt["exist"]):
            if (obj.db.main["exist"]):
                m = utils.sdb2max_antimatter(obj)
                buffer += "|cAntimatter:|n " + "{:.2f}".format(obj.db.fuel["antimatter"] / 1000000.0) + "/" + "{:.2f}".format(m) + " tons: " + "{:.4s}".format(unparse.unparse_percent(obj.db.fuel["antimatter"] / m))+ " " + alerts.ansi_stoplight_scale(obj.db.fuel["antimatter"] / m, 20) + "\n"
            if (obj.db.aux["exist"]):
                m = utils.sdb2max_deuterium(obj)
                buffer += "|cDeuterium:|n " + "{:.2f}".format(obj.db.fuel["deuterium"] / 1000000.0) + "/" + "{:.2f}".format(m) + " tons: " + "{:.4s}".format(unparse.unparse_percent(obj.db.fuel["deuterium"] / m))+ " " + alerts.ansi_stoplight_scale(obj.db.fuel["deuterium"] / m, 20) + "\n"
            if (obj.db.batt["exist"]):
                m = utils.sdb2max_reserves(obj)
                buffer += "|cReserves:|n " + "{:.2f}".format(obj.db.fuel["reserves"] / 3600.0) + "/" + "{:.2f}".format(m) + " GW^H: " + "{:.4s}".format(unparse.unparse_percent(obj.db.fuel["reserves"] / m))+ " " + alerts.ansi_stoplight_scale(obj.db.fuel["reserves"] / m, 20) + "\n"
        if (obj.db.beam["exist"]):
            if (obj.db.beam["in"] == 0.0):
                buffer += "|cBeam Power:|n ("+ unparse.unparse_power(obj.db.power["total"] * obj.db.alloc["beams"]) + ")\n"
            else:
                buffer += "|cBeam Power:|n " + "{:.15s}".format(unparse.unparse_power(obj.db.beam["out"]))+ "/" + "{:.15s}".format(unparse.unparse_power(obj.db.beam["in"])) + ": " + "{:.5s}".format(unparse.unparse_percent(obj.db.beam["out"]/obj.db.beam["in"])) + " " + alerts.ansi_rainbow_scale(obj.db.beam["out"]/obj.db.beam["in"],20) + "\n"
        if (obj.db.missile["exist"]):
            if (obj.db.missile["in"] == 0.0):
                buffer += "|cMissile Power:|n ("+ unparse.unparse_power(obj.db.power["total"] * obj.db.alloc["missiles"]) + ")\n"
            else:
                buffer += "|cMissile Power:|n " + "{:.15s}".format(unparse.unparse_power(obj.db.missile["out"]))+ "/" + "{:.15s}".format(unparse.unparse_power(obj.db.missile["in"])) + ": " + "{:.5s}".format(unparse.unparse_percent(obj.db.missile["out"]/obj.db.missile["in"])) + " " + alerts.ansi_rainbow_scale(obj.db.Missile["out"]/obj.db.missile["in"],20) + "\n"
        if (obj.db.shield["exist"]):
            for i in range(constants.MAX_SHIELD_NAME):
                buffer += "|c"+unparse.unparse_shield(i)+"|n " + "{:.5s}".format(unparse.unparse_percent(obj.db.shield[i]["damage"])) + " " + unparse.unparse_damage(obj.db.shield[i]["damage"])+"\n"
                d = utils.sdb2dissipation(obj,i)
                if (not obj.db.shield[i]["active"] or not d):
                    buffer+= "|cRating:|n "+ "{:.15s}".format(unparse.unparse_power(obj.db.shield[i]["maximum"]/obj.db.shield[i]["ratio"])) + " " + "{:.15s}".format(unparse.unparse_power(obj.db.shield[i]["maximum"]))+ " "+ ":.15s".format(unparse.unparse_power(obj.db.alloc["shield"][i]*obj.db.power["total"]))+"\n"
                else:
                    buffer += "{:.15s}".format(unparse.unparse_power(d)) + " " + "{:.5s}".format(unparse.unparse_percent(1.0 - (1.0 / d)))+ " " + alerts.ansi_red_scale(obj.db.shield[i]["damage"], 20) + "\n"
                if (i < constants.MAX_SHIELD_NAME -1):
                    buffer += "\n"
        alerts.console_message(self.caller,["engineering"],buffer)

class CmdStatus(default_cmds.MuxCommand):
    """
    Gives the status of the helm

    Usage: status
    
    Command list:
    Does not have any commands
    """

    key = "status"
    help_category = "Helm"

    def func(self):
        self.args = self.args.strip()
        self.args = self.args.split(" ")
        caller = self.caller
        obj_x = search_object(self.caller.location)[0]
        obj = search_object(obj_x.db.ship)[0]
        if(errors.error_on_console(self.caller,obj)):
            return 0
        buffer = "|y|[bHelm Status Report|n\n"
        table = evtable.EvTable("Name","Data")
        table.add_row("|cGalactic X Y Z|n",str(utils.su2pc(obj.db.coords["x"])) + " " + str(utils.su2pc(obj.db.coords["y"])) + " " + str(utils.su2pc(obj.db.coords["z"])))
        table.add_row("|cRelative X Y Z|n",str(utils.su2pc(obj.db.coords["x"] - obj.db.coords["xo"])) + " " + str(utils.su2pc(obj.db.coords["y"] - obj.db.coords["yo"])) + " " + str(utils.su2pc(obj.db.coords["z"] - obj.db.coords["zo"])))
        table.add_row("|cDestination X Y Z|n",str(utils.su2pc(obj.db.coords["xd"] - obj.db.coords["xo"])) + " " + str(utils.su2pc(obj.db.coords["yd"] - obj.db.coords["yo"])) + " " + str(utils.su2pc(obj.db.coords["zd"] - obj.db.coords["zo"])))
        table.add_row("")
        table.add_row("|cName|n",obj.name)
        table.add_row("|cClass|n",unparse.unparse_class(obj))
        table.add_row("")
        table.add_row("|cTerritory|n",unparse.unparse_empire(obj))
        table.add_row("|cQuadrant|n",unparse.unparse_quadrant(obj))
        table.add_row("")
        table.add_row("|cVisibility|n",unparse.unparse_percent_3(obj.db.sensor["visibility"]))
        table.add_row("|cCochranes|n",str(obj.db.move["cochranes"]))
        table.add_row("")
        table.add_row("|cCourse|n",unparse.unparse_course(obj))
        table.add_row("|cHelm Power|n",unparse.unparse_power(obj.db.alloc["helm"] * obj.db.power["total"]))
        table.add_row("")
        table.add_row("|cSpeed|n",unparse.unparse_movement(obj))
        table.add_row("|cVelocity|n",unparse.unparse_velocity(obj))
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
        if (obj.db.cloak["exist"] or obj.db.shield["exist"]):
            if (obj.db.shield["exist"]):
                table.add_row("|cShield Freq|n",unparse.unparse_freq(obj.db.shield["freq"]))
            if (obj.db.cloak["exist"]):
                table.add_row("|cCloak Freq|n",unparse.unparse_freq(obj.db.cloak["freq"]))
        buffer += str(table) + "\n"
        if (obj.db.cloak["exist"] or obj.db.shield["exist"]):
            buffer += "|y|[bHelm Damage Report|n\n"
            table = evtable.EvTable("Name","","","")
            if(obj.db.cloak["exist"]):
                table.add_row("|c" + constants.system_name[4] + "|n",unparse.unparse_percent(obj.db.cloak["damage"]),unparse.unparse_damage(obj.db.cloak["damage"]))
                if (not obj.db.cloak["active"]):
                    table.add_row("|cRating:|n",unparse.unparse_power(obj.db.cloak["cost"]),unparse.unparse_power(obj.db.alloc["cloak"] * obj.db.power["total"]))
                else:
                    table.add_row(unparse.unparse_power(obj.db.alloc["cloak"] * obj.db.total["power"]),unparse_unparse_percent(obj.db.alloc["cloak"] * obj.db.power["total"] / obj.db.cloak["cost"]),"Cloaked")
                table.add_row("")
            if (obj.db.shield["exist"]):
                for i in range(constants.MAX_SHIELD_NAME):
                    table.add_row("|c"+unparse.unparse_shield(i)+"|n",unparse.unparse_percent(obj.db.shield[i]["damage"]),unparse.unparse_damage(obj.db.shield[i]["damage"]))
                    d = utils.sdb2dissipation(obj,i)
                    if (not obj.db.shield[i]["active"] or not d):
                        table.add_row("|cRating:|n",unparse.unparse_power(obj.db.shield[i]["maximum"]/obj.db.shield[i]["ratio"]),unparse.unparse_power(obj.db.shield[i]["maximum"]),unparse.unparse_power(obj.db.alloc["shield"][i]*obj.db.power["total"]))
                    else:
                        table.add_row(unparse.unparse_power(d),unparse.unparse_percent(1.0 - (1.0 / d)),alerts.ansi_red_scale(obj.db.shield[i]["damage"], 20))
                    if (i < constants.MAX_SHIELD_NAME -1):
                        table.add_row("")
                    
            buffer += str(table)
        alerts.notify(self.caller,buffer)

class CmdCoords(default_cmds.MuxCommand):
    """
    Set coordinates

    Usage: coords <command>
    
    Command list:
    <empty> - Gives the current coordinates
    relative - Gives the relative coordinates
    layin - Gives the laid in coordinates
    set relative X Y Z - Sets the relative coordinates
    set X Y Z - Lays in the coordinates
    reset - Resets the relative coordinates
    
    """

    key = "coords"
    help_category = "Helm"
    
    def func(self):
        self.args = self.args.strip()
        self.args = self.args.split(" ")
        caller = self.caller
        obj_x = search_object(self.caller.location)[0]
        obj = search_object(obj_x.db.ship)[0]
        if(errors.error_on_console(self.caller,obj)):
                return 0

        if (self.args[0] == ""):
            self.caller.msg("Current location: " + str("{:10.3f}".format(obj.db.coords["x"])) + " " + str("{:10.3f}".format(obj.db.coords["y"])) + " " + str("{:10.3f}".format(obj.db.coords["z"])))
        elif(self.args[0] == "relative"):
            self.caller.msg("Relative coordinates: " + str("{:10.3f}".format(obj.db.coords["xo"])) + " " + str("{:10.3f}".format(obj.db.coords["yo"])) + " " + str("{:10.3f}".format(obj.db.coords["zo"])))
        elif(self.args[0] == "layin"):
            self.caller.msg("Laid in coordinates: " + str("{:10.3f}".format(obj.db.coords["xd"])) + " " + str("{:10.3f}".format(obj.db.coords["yd"])) + " " + str("{:10.3f}".format(obj.db.coords["zd"])))
        elif(self.args[0] == "set"):
            if (len(self.args) == 5):
                if (self.args[1] == "relative"):
                    setter.do_set_coords_manual(self.caller,obj,float(self.args[2]),float(self.args[3]),float(self.args[4]))
                else:
                    self.caller.msg(alerts.ansi_red("Incorrect data. " + str(self.args)))
            elif(len(self.args) == 4):
                    setter.do_set_coords_layin(self.caller,obj,float(self.args[1]),float(self.args[2]),float(self.args[3]))
            else:
                self.caller.msg(alerts.ansi_red("Incorrect data. " + str(self.args)))
        elif(self.args[0] == "reset"):
            setter.do_set_coords_reset(self,obj)
        else:    
            self.caller.msg("Command not found: " + str(self.args))
            
class CmdEngage(default_cmds.MuxCommand):
    """
    Engages the engines

    Usage: engage
    
    Command list:
    None
    """

    key = "engage"
    help_category = "Helm"
    
    def func(self):
        #self.args = self.args.strip()
        caller = self.caller
        obj_x = search_object(self.caller.location)[0]
        obj = search_object(obj_x.db.ship)[0]
        if(errors.error_on_console(self.caller,obj)):
            return 0
        setter.do_set_coords_engage(self.caller,obj)