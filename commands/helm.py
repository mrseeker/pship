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
            self.add(CmdCalculate())
            self.add(CmdAutopilot())
            self.add(CmdAlloc())
            self.add(CmdIntercept())
            self.add(CmdFreq())
            self.add(CmdPitch())
            self.add(CmdPitch())
            self.add(CmdRoll())
            self.add(CmdAxis())
            self.add(CmdEvade())
            self.add(CmdIntercept())
            self.add(CmdParallel())

class FighterCmdSet(CmdSet):
        key = "FighterCmdSet"
        
        def at_cmdset_creation(self):
            self.add(CmdCoords())
            self.add(CmdEngage())
            self.add(CmdCalculate())
            self.add(CmdStatus_Fighter())
            self.add(CmdAutopilot())
            self.add(CmdIntercept())
            self.add(CmdFreq())
            self.add(CmdPitch())
            self.add(CmdPitch())
            self.add(CmdRoll())
            self.add(CmdAxis())
            self.add(CmdEvade())
            self.add(CmdIntercept())
            self.add(CmdParallel())

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
        obj_x = search_object(caller.location)[0]
        obj = search_object(obj_x.db.ship)[0]
        if(errors.error_on_console(caller,obj)):
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
                    buffer+= "|cRating:|n "+ "{:.15s}".format(unparse.unparse_power(obj.db.shield["maximum"]/obj.db.shield["ratio"])) + " " + "{:.15s}".format(unparse.unparse_power(obj.db.shield["maximum"]))+ " "+ ":.15s".format(unparse.unparse_power(obj.db.alloc["shield"][i]*obj.db.power["total"]))+"\n"
                else:
                    buffer += "{:.15s}".format(unparse.unparse_power(d)) + " " + "{:.5s}".format(unparse.unparse_percent(1.0 - (1.0 / d)))+ " " + alerts.ansi_red_scale(obj.db.shield[i]["damage"], 20) + "\n"
                if (i < constants.MAX_SHIELD_NAME -1):
                    buffer += "\n"
        alerts.console_message(obj,["engineering"],buffer)

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
        obj_x = search_object(caller.location)[0]
        obj = search_object(obj_x.db.ship)[0]
        if(errors.error_on_console(caller,obj)):
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
                    table.add_row(unparse.unparse_power(obj.db.alloc["cloak"] * obj.db.total["power"]),unparse.unparse_percent(obj.db.alloc["cloak"] * obj.db.power["total"] / obj.db.cloak["cost"]),"Cloaked")
                table.add_row("")
            if (obj.db.shield["exist"]):
                for i in range(constants.MAX_SHIELD_NAME):
                    table.add_row("|c"+unparse.unparse_shield(i)+"|n",unparse.unparse_percent(obj.db.shield[i]["damage"]),unparse.unparse_damage(obj.db.shield[i]["damage"]))
                    d = utils.sdb2dissipation(obj,i)
                    if (not obj.db.shield[i]["active"] or not d):
                        table.add_row("|cRating:|n",unparse.unparse_power(obj.db.shield["maximum"]/obj.db.shield[i]["ratio"]),unparse.unparse_power(obj.db.shield["maximum"]),unparse.unparse_power(obj.db.alloc["shield"][i]*obj.db.power["total"]))
                    else:
                        table.add_row(unparse.unparse_power(d),unparse.unparse_percent(1.0 - (1.0 / d)),alerts.ansi_red_scale(obj.db.shield[i]["damage"], 20))
                    if (i < constants.MAX_SHIELD_NAME -1):
                        table.add_row("")
                    
            buffer += str(table)
        alerts.notify(caller,buffer)

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
        obj_x = search_object(caller.location)[0]
        obj = search_object(obj_x.db.ship)[0]
        if(errors.error_on_console(caller,obj)):
                return 0

        if (self.args[0] == ""):
            caller.msg("Current location: " + str("{:10.3f}".format(obj.db.coords["x"])) + " " + str("{:10.3f}".format(obj.db.coords["y"])) + " " + str("{:10.3f}".format(obj.db.coords["z"])))
        elif(self.args[0] == "relative"):
            caller.msg("Relative coordinates: " + str("{:10.3f}".format(obj.db.coords["xo"])) + " " + str("{:10.3f}".format(obj.db.coords["yo"])) + " " + str("{:10.3f}".format(obj.db.coords["zo"])))
        elif(self.args[0] == "layin"):
            caller.msg("Laid in coordinates: " + str("{:10.3f}".format(obj.db.coords["xd"])) + " " + str("{:10.3f}".format(obj.db.coords["yd"])) + " " + str("{:10.3f}".format(obj.db.coords["zd"])))
        elif(self.args[0] == "set"):
            if (len(self.args) == 5):
                if (self.args[1] == "relative"):
                    setter.do_set_coords_manual(caller,obj,float(self.args[2]),float(self.args[3]),float(self.args[4]))
                else:
                    caller.msg(alerts.ansi_red("Incorrect data. " + str(self.args)))
            elif(len(self.args) == 4):
                    setter.do_set_coords_layin(caller,obj,float(self.args[1]),float(self.args[2]),float(self.args[3]))
            else:
                caller.msg(alerts.ansi_red("Incorrect data. " + str(self.args)))
        elif(self.args[0] == "reset"):
            setter.do_set_coords_reset(caller,obj)
        else:    
            caller.msg("Command not found: " + str(self.args))
            

class CmdCalculate(default_cmds.MuxCommand):
    """
    Calculates from one type to another type

    Usage: calc <command>
    
    Command list:
    ly2pc - Lightyear to Parsec
    ly2su - Lightyear to Standard Unit
    pc2ly - Parsec to Lightyear
    pc2su - Parsec to Standard Unit
    su2ly - Standard Unit to Lightyear
    su2pc - Standard Unit to Parsec
    """

    key = "calc"
    help_category = "Helm"
    
    def func(self):
        self.args = self.args.strip()
        self.args = self.args.split(" ")
        caller = self.caller
        obj_x = search_object(caller.location)[0]
        obj = search_object(obj_x.db.ship)[0]
        if(errors.error_on_console(caller,obj)):
                return 0

        if (self.args[0] == ""):
            caller.msg("Please fill in an unit for conversion")
        elif(self.args[0] == "ly2pc"):
            for arg in self.args[1:]:
                caller.msg(str(arg) + " - " + str(utils.ly2pc(float(arg))))
        elif(self.args[0] == "ly2su"):
            for arg in self.args[1:]:
                caller.msg(str(arg) + " - " + str(utils.ly2su(float(arg))))
        elif(self.args[0] == "pc2ly"):
            for arg in self.args[1:]:
                caller.msg(str(arg) + " - " + str(utils.pc2ly(float(arg))))
        elif(self.args[0] == "pc2su"):
            for arg in self.args[1:]:
                caller.msg(str(arg) + " - " + str(utils.pc2su(float(arg))))
        elif(self.args[0] == "su2ly"):
            for arg in self.args[1:]:
                caller.msg(str(arg) + " - " + str(utils.su2ly(float(arg))))
        elif(self.args[0] == "su2pc"):
            for arg in self.args[1:]:
                caller.msg(str(arg) + " - " + str(utils.su2pc(float(arg))))
        else:    
            caller.msg("Command not found: " + str(self.args))

class CmdAlloc(default_cmds.MuxCommand):
    """
    Commands related to the allocation of the helm.

    Usage: alloc <command> <value>
    
    Command list:
    status - Gives a full status of the allocations
    MSC - Sets the allocation of the Movement, Shields and Cloak
    shield - Allocation of the shields (forward, starboard, aft, port, dorsal, ventral)

    """

    key = "alloc"
    help_category = "Helm"
    
    def func(self):
        self.args = self.args.split(" ")
        caller = self.caller
        obj_x = search_object(caller.location)[0]
        obj = search_object(obj_x.db.ship)[0]
        if(errors.error_on_console(caller,obj)):
                return 0
        if (self.args[0] == "MSC" and len(self.args) == 4):
            setter.do_set_helm_alloc(caller,float(self.args[1]),float(self.args[2]),float(self.args[3]),obj)
        elif (self.args[0] == "shield" and len(self.args) == 7):
            setter.do_set_shield_alloc(caller,float(self.args[1]),float(self.args[2]),float(self.args[3]),float(self.args[4]),float(self.args[5]),float(self.args[6]),obj)
        elif (self.args[0] == "status"):
            #Give a full report back
            buffer = "|y|[bHelm Allocation Report|n\n"
            table = evtable.EvTable("|cAllocation|n","|cEPS Power|n","|cPercentage|n","")
            table.add_row("|cTotal Helm|n",unparse.unparse_power(obj.db.alloc["helm"]*obj.db.power["total"]),unparse.unparse_percent(obj.db.alloc["helm"]))
            table.add_row("|cMovement|n",unparse.unparse_power(obj.db.alloc["movement"]*obj.db.power["total"]),unparse.unparse_percent(obj.db.alloc["movement"]),alerts.ansi_rainbow_scale(obj.db.alloc["movement"],35))
            table.add_row("|cShields|n",unparse.unparse_power(obj.db.alloc["shields"]*obj.db.power["total"]),unparse.unparse_percent(obj.db.alloc["shields"]))
            for i in range(constants.MAX_SHIELD_NAME):
                table.add_row("|c"+unparse.unparse_shield(i) + "|n",unparse.unparse_power(obj.db.alloc["shield"][i]*obj.db.power["total"]),unparse.unparse_percent(obj.db.alloc["shield"][i]),alerts.ansi_rainbow_scale(obj.db.alloc["shield"][i],35))
            table.add_row("|c"+constants.cloak_name[obj.db.cloak["exist"]]+"|n",unparse.unparse_power(obj.db.alloc["cloak"]*obj.db.power["total"]),unparse.unparse_percent(obj.db.alloc["cloak"]),alerts.ansi_rainbow_scale(obj.db.alloc["cloak"],35))
            alerts.notify(caller,buffer + str(table) + "\n")
        else:    
            caller.msg("Command not found: " + str(self.args))

class CmdFreq(default_cmds.MuxCommand):
    """
    Commands related to the setting of frequencies.

    Usage: freq <device> <freq>

    Command list:
    device - Type of device (shield,cloak)
    first - Frequency in Ghz (1.000 to 999.999)
    """

    key="freq"
    help_category = "Helm"

    def func(self):
        self.args = self.args.split(" ")
        caller = self.caller
        obj_x = search_object(caller.location)[0]
        obj = search_object(obj_x.db.ship)[0]

        if(errors.error_on_console(caller,obj)):
            return 0
    
        if(len(self.args) == 2):
            if self.args[0][0] == "s":
                setter.do_set_shield_freq(caller,obj,float(self.args[1]))
            elif self.args[0][0] == "c":
                setter.do_set_cloak_freq(caller,obj,float(self.args[1]))
            else:
                alerts.notify(caller,alerts.ansi_red("Wrong device: {.s}".format(self.args[0])))    
        else:
            alerts.notify(caller,alerts.ansi_red("Wrong command entered."))



class CmdAxis(default_cmds.MuxCommand):
    """
    Commands related to the axis of the ship.

    Usage: axis <pitch> <yaw> <roll>

    Command list:
    pitch - Sets the pitch in degrees
    yaw - Sets the yaw in degrees
    roll - Sets the roll in degrees
    """

    key="axis"
    help_category = "Helm"

    def func(self):
        self.args = self.args.split(" ")
        caller = self.caller
        obj_x = search_object(caller.location)[0]
        obj = search_object(obj_x.db.ship)[0]

        if(errors.error_on_console(caller,obj)):
            return 0
    
        if(len(self.args) == 3):
                setter.do_set_pitch(caller,obj,float(self.args[0]))
                setter.do_set_yaw(caller,obj,float(self.args[1]))
                setter.do_set_roll(caller,obj,float(self.args[2]))
        else:
            alerts.notify(caller,alerts.ansi_red("Wrong command entered."))

class CmdEvade(default_cmds.MuxCommand):
    """
    Commands related to evading a contact.

    Usage: evade <contact>

    Command list:
    contact - Contact number to evade
    """

    key="evade"
    help_category = "Helm"

    def func(self):
        self.args = self.args.split(" ")
        caller = self.caller
        obj_x = search_object(caller.location)[0]
        obj = search_object(obj_x.db.ship)[0]

        if(errors.error_on_console(caller,obj)):
            return 0
    
        if(len(self.args) == 1):
                setter.do_set_evade(caller,obj,int(self.args[0]))
        else:
            alerts.notify(caller,alerts.ansi_red("Wrong command entered."))

class CmdParallel(default_cmds.MuxCommand):
    """
    Commands related to go parallel to a contact.

    Usage: parallel <contact>

    Command list:
    contact - Contact number to side
    """

    key="parallel"
    help_category = "Helm"

    def func(self):
        self.args = self.args.split(" ")
        caller = self.caller
        obj_x = search_object(caller.location)[0]
        obj = search_object(obj_x.db.ship)[0]

        if(errors.error_on_console(caller,obj)):
            return 0
    
        if(len(self.args) == 1):
                setter.do_set_parallel(caller,obj,int(self.args[0]))
        else:
            alerts.notify(caller,alerts.ansi_red("Wrong command entered."))


class CmdIntercept(default_cmds.MuxCommand):
    """
    Commands related to intercepting a contact.

    Usage: intercept <contact>

    Command list:
    contact - Contact number to intercept
    """

    key="intercept"
    help_category = "Helm"

    def func(self):
        self.args = self.args.split(" ")
        caller = self.caller
        obj_x = search_object(caller.location)[0]
        obj = search_object(obj_x.db.ship)[0]

        if(errors.error_on_console(caller,obj)):
            return 0
    
        if(len(self.args) == 1):
                setter.do_set_intercept(caller,obj,int(self.args[0]))
        else:
            alerts.notify(caller,alerts.ansi_red("Wrong command entered."))


class CmdYaw(default_cmds.MuxCommand):
    """
    Commands related to the yaw of the ship.

    Usage: yaw <degrees>

    Command list:
    degrees - Sets the yaw in degrees
    """

    key="yaw"
    help_category = "Helm"

    def func(self):
        self.args = self.args.split(" ")
        caller = self.caller
        obj_x = search_object(caller.location)[0]
        obj = search_object(obj_x.db.ship)[0]

        if(errors.error_on_console(caller,obj)):
            return 0
    
        if(len(self.args) == 0):
            alerts.yaw(obj)
        elif(len(self.args) == 1):
                setter.do_set_yaw(caller,obj,float(self.args[0]))
        else:
            alerts.notify(caller,alerts.ansi_red("Wrong command entered."))

class CmdPitch(default_cmds.MuxCommand):
    """
    Commands related to the pitch of the ship.

    Usage: pitch <degrees>

    Command list:
    degrees - Sets the pitch in degrees
    """

    key="pitch"
    help_category = "Helm"

    def func(self):
        self.args = self.args.split(" ")
        caller = self.caller
        obj_x = search_object(caller.location)[0]
        obj = search_object(obj_x.db.ship)[0]

        if(errors.error_on_console(caller,obj)):
            return 0
    
        if(len(self.args) == 0):
            alerts.pitch(obj)
        elif(len(self.args) == 1):
                setter.do_set_pitch(caller,obj,float(self.args[0]))
        else:
            alerts.notify(caller,alerts.ansi_red("Wrong command entered."))

class CmdRoll(default_cmds.MuxCommand):
    """
    Commands related to the roll of the ship.

    Usage: roll <degrees>

    Command list:
    degrees - Sets the roll in degrees
    """

    key="roll"
    help_category = "Helm"

    def func(self):
        self.args = self.args.split(" ")
        caller = self.caller
        obj_x = search_object(caller.location)[0]
        obj = search_object(obj_x.db.ship)[0]

        if(errors.error_on_console(caller,obj)):
            return 0
    
        if(len(self.args) == 0):
            alerts.roll(obj)
        elif(len(self.args) == 1):
                setter.do_set_roll(caller,obj,float(self.args[0]))
        else:
            alerts.notify(caller,alerts.ansi_red("Wrong command entered."))

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
        obj_x = search_object(caller.location)[0]
        obj = search_object(obj_x.db.ship)[0]
        if(errors.error_on_console(caller,obj)):
            return 0
        setter.do_set_coords_engage(caller,obj)

class CmdAutopilot(default_cmds.MuxCommand):
    """
    Turns the autopilot on/off

    Usage: autopilot [0-1]
    
    Command list:
    None
    """

    key = "autopilot"
    help_category = "Helm"
    
    def func(self):
        self.args = self.args.strip()
        self.args = self.args.split(" ")
        caller = self.caller
        obj_x = search_object(caller.location)[0]
        obj = search_object(obj_x.db.ship)[0]
        if(errors.error_on_console(caller,obj)):
            return 0
        if (len(self.args) == 1):
            setter.do_set_autopilot(caller,obj,int(self.args[0]))
        else:
            print("Current autopilot setting: " + obj.db.status["autopilot"])

class CmdSpeed(default_cmds.MuxCommand):
    """
    Sets the warp speed
    
    Usage: speed <warp>
    
    Command list:
    None
    """
    
    key = "speed"
    help_category = "Helm"
    
    def func(self):
        caller = self.caller
        obj_x = search_object(caller.location)[0]
        obj = search_object(obj_x.db.ship)[0]
        if(errors.error_on_console(caller,obj)):
            return 0
        if (len(self.args) == 1):
            setter.do_set_speed(caller,obj,float(self.args[0]))

class CmdIntercept(default_cmds.MuxCommand):
    """
    Intercepts a target
    
    Usage: intercept <target ID>
    
    Command list:
    None
    """
    
    key = "intercept"
    help_category = "Helm"
    
    def func(self):
        caller = self.caller
        obj_x = search_object(caller.location)[0]
        obj = search_object(obj_x.db.ship)[0]
        if(errors.error_on_console(caller,obj)):
            return 0
        if (len(self.args) == 1):
            setter.do_set_intercept(caller,obj,int(self.args[0]))