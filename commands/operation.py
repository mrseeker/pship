"""
Handles all operations-related commands
"""

from evennia import default_cmds, CmdSet
from evennia.utils.search import search_object
from world import alerts, errors, set as setter, utils
from world import constants
from world.format import l_line

class OperationCmdSet(CmdSet):
        
        key = "OperationCmdSet"
    
        def at_cmdset_creation(self):
            self.add(CmdReFuel())
            self.add(CmdDeFuel())
            self.add(CmdFreq())
            self.add(CmdConnect())
            self.add(CmdDocking())
            self.add(CmdLanding())

class CmdReFuel(default_cmds.MuxCommand):
    """
    Commands related to the fueling of a spaceship.

    Usage: refuel <shipname> <type> <value>
    
    Command list:
    None
    """

    key = "refuel"
    aliases = ["fuel"]
    help_category = "Operation"
    
    def func(self):
        self.args = self.args.split(" ")
        caller = self.caller
        obj_x = search_object(self.caller.location)[0]
        obj = search_object(obj_x.db.ship)[0]
        receiver = search_object(self.args[0])
        if len(receiver) > 0:
            receiver = receiver[0]
        else:
            receiver = None
        if(errors.error_on_console(caller,obj)):
                return 0
        if(len(self.args) == 3):
            setter.do_set_refuel(caller,obj,receiver,self.args[1],int(self.args[2]))
        else:
            self.caller.msg("Command not found: " + str(self.args))

class CmdDeFuel(default_cmds.MuxCommand):
    """
    Commands related to the dumping of fuel from a spaceship.

    Usage: defuel [shipname] <type> <value>
    
    Command list:
    None
    """

    key = "defuel"
    aliases = ["dump"]
    help_category = "Operation"
    
    def func(self):
        self.args = self.args.split(" ")
        caller = self.caller
        obj_x = search_object(self.caller.location)[0]
        obj = search_object(obj_x.db.ship)[0]
        receiver = search_object(self.args[0])
        if len(receiver) > 0:
            receiver = receiver[0]
        elif (obj == receiver):
            #transferring it to itself...
            receiver = None
        else:
            receiver = None
        if(errors.error_on_console(caller,obj)):
                return 0
        if(len(self.args) == 2):
            setter.do_set_defuel(caller,obj,None,self.args[0],int(self.args[1]))
        elif(len(self.args) == 3):
            setter.do_set_defuel(caller,obj,receiver,self.args[1],int(self.args[2]))
        else:
            self.caller.msg("Command not found: " + str(self.args))

class CmdFreq(default_cmds.MuxCommand):
    """
    Commands related to the setting of frequencies.

    Usage: freq <device> <freq>

    Command list:
    device - Type of device (tract or trans)
    first - Frequency in Ghz (1.000 to 999.999)
    """

    key="freq"
    help_category = "Operation"

    def func(self):
        self.args = self.args.split(" ")
        caller = self.caller
        obj_x = search_object(self.caller.location)[0]
        obj = search_object(obj_x.db.ship)[0]

        if(errors.error_on_console(self.caller,obj)):
            return 0
    
        if(len(self.args) == 2):
            if self.args[0][0] == "tract":
                setter.do_set_tract_freq(self,obj,float(self.args[1]))
            elif self.args[0][0] == "trans":
                setter.do_set_trans_freq(self,obj,float(self.args[1]))
            else:
                alerts.notify(self,alerts.ansi_red("Wrong device: {.s}".format(self.args[0])))    
        else:
            alerts.notify(self,alerts.ansi_red("Wrong command entered."))


class CmdConnect(default_cmds.MuxCommand):
    """
    Commands related to opening/closing of the airlock.

    Usage: airlock [shipname] <open/close>
    
    Aliases: connect, con

    Command list:
    None
    """

    key = "airlock"
    aliases = ["connect","con"]
    help_category = "Operation"
    
    def func(self):
        self.args = self.args.split(" ")
        caller = self.caller
        obj_x = search_object(self.caller.location)[0]
        obj = search_object(obj_x.db.ship)[0]
        ship_airlock = utils.name2sdb(self.args[0])
        if(errors.error_on_console(caller,obj)):
                return 0
        elif ship_airlock == constants.SENSOR_FAIL:
            alerts.notify(caller,alerts.ansi_red("That is not a valid contact."))
            return 0
        elif(ship_airlock not in obj.contents):
            alerts.notify(caller,alerts.ansi_red("That is not a valid contact."))
            return 0
        elif(self.args[1][0] != "o" and self.args[1][0] != "c"):
            alerts.notify(caller,alerts.ansi_red("That is not a valid command."))
            return 0
        elif(self.args[1][0] == "o"):
            ship_airlock.db.status["connected"] = 1
            alerts.do_console_notify(obj,["operations","security"],alerts.ansi_cmd(caller,"{:s} has been connected.".format(ship_airlock.name)))
            alerts.do_console_notify(ship_airlock,["operations","security"],alerts.ansi_notify("{:s} opens the airlock.".format(obj.name)))
        elif(self.args[1][0] == "c"):
            ship_airlock.db.status["connected"] = 0
            alerts.do_console_notify(obj,["operations","security"],alerts.ansi_cmd(caller,"{:s} has been disconnected.".format(ship_airlock.name)))
            alerts.do_console_notify(ship_airlock,["operations","security"],alerts.ansi_notify("{:s} closes the airlock.".format(obj.name)))
        else:
            self.caller.msg("Command not found: " + str(self.args))

class CmdDocking(default_cmds.MuxCommand):
    """
    Commands related to opening/closing of the docking doors.

    Usage: docking <open/close/status>
    
    Aliases: dock, door

    Command list:
    None
    """

    key = "docking"
    aliases = ["dock","door"]
    help_category = "Operation"
    
    def func(self):
        self.args = self.args.split(" ")
        caller = self.caller
        obj_x = search_object(self.caller.location)[0]
        obj = search_object(obj_x.db.ship)[0]
        if(errors.error_on_console(caller,obj)):
                return 0
        elif(obj.db.structure["has_docking_bay"] == 0):
            alerts.notify(caller,alerts.ansi_red("{:s} has no docking bay.".format(obj.name)))
            return 0
        elif(self.args[0][0] != "o" and self.args[0][0] != "c" and self.args[0][0] !="s"):
            alerts.notify(caller,alerts.ansi_red("That is not a valid command."))
            return 0
        elif(self.args[0][0] == "o"):
            obj.db.status["open_docking"] = 1
            alerts.do_console_notify(obj,["helm","engineering","operations"],alerts.ansi_cmd(caller,"Docking doors have been opened"))
            alerts.do_space_notify_one(obj, ["helm","engineering", "operations"], "opens the docking doors")
        elif(self.args[0][0] == "c"):
            obj.db.status["open_docking"] = 0
            alerts.do_console_notify(obj,["helm","engineering","operations"],alerts.ansi_cmd(caller,"Docking doors have been closed"))
            alerts.do_space_notify_one(obj, ["helm","engineering", "operations"], "closes the docking doors")
        elif(self.args[0][0] == "s"):
            doors = "|b--[|yDocking Report|b]-------------------------------------------------------------|n\n"
            if obj.db.status["open_docking"] == 1:
                doors += "|cCurrent status: |gOpen|n\n"
            else:
                doors += "|cCurrent status: |rClosed|n\n"
            docked = []
            if obj.contents:
                for con in obj.contents:
                    if (con.tags.get(category="space_object") == constants.SHIP_ATTR_NAME):
                        if ((con.db.cloak["active"] != 1 or con.db.status["connected"] == 1) and con.db.status["docked"] != 0):
                            docked.append(con.name)
                        elif(con.db.cloak["active"] != 1):
                            docked.append("Ship")
                            alerts.write_spacelog(caller,con,"BUG: Bad location SDB")
                        else:
                            alerts.write_spacelog(caller,con,"BUG: Bad location SDB")
            if docked:
                doors += "Docked ships: " + ", ".join(docked)        
            doors += l_line()
            alerts.notify(caller,doors)
        else:
            caller.msg("Command not found: " + str(self.args))

class CmdLanding(default_cmds.MuxCommand):
    """
    Commands related to opening/closing of the landing pads.

    Usage: landing <open/close/status>
    
    Aliases: land, pad

    Command list:
    None
    """

    key = "landing"
    aliases = ["land","pad"]
    help_category = "Operation"
    
    def func(self):
        self.args = self.args.split(" ")
        caller = self.caller
        obj_x = search_object(self.caller.location)[0]
        obj = search_object(obj_x.db.ship)[0]
        if(errors.error_on_console(caller,obj)):
                return 0
        elif(obj.db.structure["has_landing_pad"] == 0):
            alerts.notify(caller,alerts.ansi_red("{:s} has no landing pad.".format(obj.name)))
            return 0
        elif(self.args[0][0] != "o" and self.args[0][0] != "c" and self.args[0][0] !="s"):
            alerts.notify(caller,alerts.ansi_red("That is not a valid command."))
            return 0
        elif(self.args[0][0] == "o"):
            obj.db.status["open_landing"] = 1
            alerts.do_console_notify(obj,["helm","engineering","operations"],alerts.ansi_cmd(caller,"Landing pads have been opened."))
            alerts.do_space_notify_one(obj, ["helm","engineering", "operations"], "opens the landing pad.")
        elif(self.args[0][0] == "c"):
            obj.db.status["open_landing"] = 0
            alerts.do_console_notify(obj,["helm","engineering","operations"],alerts.ansi_cmd(caller,"Landing pads have been closed."))
            alerts.do_space_notify_one(obj, ["helm","engineering", "operations"], "closes the landing pad.")
        elif(self.args[0][0] == "s"):
            doors = "|b--[|yLanding Report|b]-------------------------------------------------------------|n\n"
            if obj.db.status["open_landing"] == 1:
                doors += "|cCurrent status: |gOpen|n\n"
            else:
                doors += "|cCurrent status: |rClosed|n\n"
            docked = []
            if obj.contents:
                for con in obj.contents:
                    if (con.tags.get(category="space_object") == constants.SHIP_ATTR_NAME):
                        if ((con.db.cloak["active"] != 1 or con.db.status["connected"] == 1) and con.db.status["landed"] != 0):
                            docked.append(con.name)
                        elif(con.db.cloak["active"] != 1):
                            docked.append("Ship")
                            alerts.write_spacelog(caller,con,"BUG: Bad location SDB")
                        else:
                            alerts.write_spacelog(caller,con,"BUG: Bad location SDB")
            if docked:
                doors += "Landed ships: " + ", ".join(docked)        
            doors += l_line()
            alerts.notify(caller,doors)
        else:
            caller.msg("Command not found: " + str(self.args))