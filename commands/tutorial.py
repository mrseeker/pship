from evennia.utils.create import create_object
from evennia.utils.search import search_tag, search_object
from typeclasses.Ships.Generic import Shuttle
from world import alerts, utils,constants
import time
import random
from evennia import gametime
from evennia import default_cmds, CmdSet
from evennia.scripts.tickerhandler import TICKER_HANDLER
import commands.tutorial as tut

class TutorialCmdSet(CmdSet):
        
        key = "TutorialCmdSet"
        def at_cmdset_creation(self):
            self.add(CmdTutorial())

class CmdTutorial(default_cmds.MuxCommand):
    """
    Commands related to ending the tutorial

    Usage: tutorial <stop>

    Command list:
    stop - Stops the tutorial
    """

    key="tutorial"
    help_category = "Tutorial"

    def func(self):
        self.args = self.args.split(" ")
        caller = self.caller
        obj_x = utils.name2sdb(caller.location)
        if (obj_x != constants.SENSOR_FAIL):
            obj = utils.name2sdb(obj_x.db.ship)
        if (len(self.args) == 1):
            create_tutorial(caller)
        if (self.args[0] == "stop" and obj != constants.SENSOR_FAIL):
            obj.tags.remove(category="tutorial")
            obj.cmdset.remove("typeclasses.tutorial.TutorialCmdSet", persistent=True)

def create_tutorial(caller):
    obj = create_object(Shuttle,key="TUTORIAL-" + str(random.randint(0,10000)))
    obj.tags.add(obj.name,category="tutorial")
    TICKER_HANDLER.add(10,update_tutorial,"tutorial")
    obj.db.tutorial = [gametime.gametime(absolute=True),0]
    obj.db.fuel = {"antimatter":utils.sdb2max_antimatter(obj),"deuterium":utils.sdb2max_deuterium(obj),"reserves":utils.sdb2max_reserves(obj)}
    obj.cmdset.add("commands.tutorial.TutorialCmdSet",persistent = True)
    utils.debug_space(obj)
    caller.move_to(obj)

def update_tutorial():
    objects = search_tag(category="tutorial")
    count = 0
    timer = time.time()
    for obj in objects:
        if (obj.db.structure["type"] > 0):
            count = count + 1
            tutorial = list(obj.db.tutorial)
            now = gametime.gametime(absolute=True)
            dt = now - tutorial[0]
            if (dt > 60):
                done = False
                if(tutorial[1] == 0):
                    #Start of the tutorial
                    alerts.console_message(obj,["bridge"],alerts.ansi_cmd("Subel","*static noise* Hello and welcome to the tutorial. You can at any time stop this recording by typing 'tutorial stop'."))
                    done = True
                elif(tutorial[1] == 1):
                    alerts.console_message(obj,["bridge"],alerts.ansi_cmd("Subel","I am going to teach you the basics of a space ship, and how to fly it. But first, we need power."))
                    done = True
                elif(tutorial[1] == 2):
                    #Engines
                    alerts.console_message(obj,["bridge"],alerts.ansi_cmd("Subel","As you might notice, most commands won't work when the engine is off. Turn the engine on by typing '{:s}'".format("engine start")))
                    done = True
                elif(tutorial[1] == 3):
                    if (obj.db.status["active"] == 0):
                        alerts.console_message(obj,["bridge"],alerts.ansi_cmd("Subel","Turn the engine on by typing '{:s}'".format("engine start")))
                    else:
                        done = True
                        alerts.console_message(obj,["bridge"],alerts.ansi_cmd("Subel","Good. You should now be able to power things up. First put the main engine on full power: '{:s}'".format("alloc main 100")))
                elif(tutorial[1] == 4):
                    if (obj.db.status["active"] == 0):
                        alerts.console_message(obj,["bridge"],alerts.ansi_cmd("Subel","Turn the engine on by typing '{:s}'".format("engine start")))
                    else:
                        done = True
                        alerts.console_message(obj,["bridge"],alerts.ansi_cmd("Subel","Good. You should now be able to power things up. First put the main engine (warp drive) on full power: '{:s}'".format("alloc main 100")))
                elif(tutorial[1] == 5):
                    if (obj.db.power["main"] == 0):
                        alerts.console_message(obj,["bridge"],alerts.ansi_cmd("Subel","Turn the main engine on full power by typing '{:s}'".format("alloc main 100")))
                    else:
                        done = True
                        alerts.console_message(obj,["bridge"],alerts.ansi_cmd("Subel","Now the auxillary power for the impulse drive: '{:s}'".format("alloc aux 100")))
                elif(tutorial[1] == 6):
                    if (obj.db.power["aux"] == 0):
                        alerts.console_message(obj,["bridge"],alerts.ansi_cmd("Subel","Turn the auxillary engine on full power by typing '{:s}'".format("alloc aux 100")))
                    else:
                        done = True
                        alerts.console_message(obj,["bridge"],alerts.ansi_cmd("Subel","And at last the batteries, in case you want to save fuel: '{:s}'".format("alloc batt 100")))
                elif(tutorial[1] == 7):
                    if (obj.db.power["batt"] == 0):
                        alerts.console_message(obj,["bridge"],alerts.ansi_cmd("Subel","Turn the batteries on full power by typing '{:s}'".format("alloc batt 100")))
                    else:
                        done = True
                        alerts.console_message(obj,["bridge"],alerts.ansi_cmd("Subel","Good. You can check the status of the engine by typing '{:s}'".format("engine status")))
                elif(tutorial[1] == 8):
                    alerts.console_message(obj,["bridge"],alerts.ansi_cmd("Subel","Now, before we can actually fly we need to allocate power. Let's do that, shall we? Type this: '{:s}'".format("alloc HTO 90 0 10")))
                    done = True
                elif(tutorial[1] == 9):
                    if (obj.db.alloc["helm"] == 0):
                        alerts.console_message(obj,["bridge"],alerts.ansi_cmd("Subel","Allocate power to the helm by typing '{:s}' and '{:s}'".format("alloc HTO 90 0 10", "alloc MSC 100 0 0")))
                    else:
                        done = True
                        alerts.console_message(obj,["bridge"],alerts.ansi_cmd("Subel","Nice. We also allocate power to operations so that the batteries keep charged. Check it out with '{:s}'".format("alloc status")))
                elif(tutorial[1] == 10):
                    alerts.console_message(obj,["bridge"],alerts.ansi_cmd("Subel","Now we can actually fly! Type '{:s}' to set a location you want to go to, '{:s}' to set the speed and '{:s}' to engage the drive.".format("coords set X Y Z","speed <warp>","engage")))
                    done = True
                elif(tutorial[1] == 11):
                    alerts.console_message(obj,["bridge"],alerts.ansi_cmd("Subel","Since we are in space, we can also set our angles: '{:s}', '{:s}', '{:s}'".format("roll <angle>","pitch <angle>","yaw <angle>")))
                    done = True
                elif(tutorial[1] == 12):
                    alerts.console_message(obj,["bridge"],alerts.ansi_cmd("Subel","And the autopilot can be turned on using the command '{:s}'".format("autopilot on")))
                    done = True
                elif(tutorial[1] == 13):
                    alerts.console_message(obj,["bridge"],alerts.ansi_cmd("Subel","There are more commands for flying but these are the most basic ones."))
                    done = True
                elif(tutorial[1] == 14):
                    if (obj.db.move["v"] == 0):
                        alerts.console_message(obj,["bridge"],alerts.ansi_cmd("Subel","Let's fly, shall we? Set a course and type '{:s}'".format("engage")))
                    else:
                        done = True
                        alerts.console_message(obj,["bridge"],alerts.ansi_cmd("Subel","Good, you are flying! You can check your location and the status using the command '{:s}'".format("status")))
                elif(tutorial[1] == 15):
                    alerts.console_message(obj,["bridge"],alerts.ansi_cmd("Subel","Now, while we are flying, let's give you some handy extra's you might need."))
                    done = True
                elif(tutorial[1] == 16):
                    alerts.console_message(obj,["bridge"],alerts.ansi_cmd("Subel","To know what is around you, you can turn long-range and short-range sensors on using '{:s}' and '{:s}'. Make sure that you allocate power to them.".format("lrs on", "srs on")))
                    done = True
                elif(tutorial[1] == 17):
                    if (obj.db.sensor["lrs_active"] == 0 or obj.db.sensor["srs_active"] == 0):
                        alerts.console_message(obj,["bridge"],alerts.ansi_cmd("Subel","You really like to fly blind, do you? type '{:s}' and '{:s}' to turn the sensors on.".format("lrs on","srs on")))
                    else:
                        done = True
                        alerts.console_message(obj,["bridge"],alerts.ansi_cmd("Subel","You might have noticed some pings. To fully check what is around you, use the command '{:s}'".format("report")))
                elif(tutorial[1] == 18):
                    alerts.console_message(obj,["bridge"],alerts.ansi_cmd("Subel","It might be that your target is hostile. This ship has some weaponry that you can use to deter them. I will only give the sequence so you know how to use them."))
                    done = True
                elif(tutorial[1] == 19):
                    alerts.console_message(obj,["bridge"],alerts.ansi_cmd("Subel","First you need to allocate power to the beam weapons (since we only have beam weapons): '{:s}' and '{:s}'.".format("alloc hto 30 30 10", "alloc bms 100 0 0")))
                    done = True
                elif(tutorial[1] == 20):
                    alerts.console_message(obj,["bridge"],alerts.ansi_cmd("Subel","Then you need to turn the beam weapons on (this ship only has 1): '{:s}'".format("enable all")))
                    done = True
                elif(tutorial[1] == 21):
                    alerts.console_message(obj,["bridge"],alerts.ansi_cmd("Subel","If you know the shield frequency, you can set the weapon frequency here: '{:s}'".format("freq beam 1")))
                    done = True
                elif(tutorial[1] == 22):
                    alerts.console_message(obj,["bridge"],alerts.ansi_cmd("Subel","We then select our target: '{:s}'".format("target <target> all")))
                    done = True
                elif(tutorial[1] == 23):
                    alerts.console_message(obj,["bridge"],alerts.ansi_cmd("Subel","And last we fire our weapon: '{:s}'".format("fire")))
                    done = True
                elif(tutorial[1] == 24):
                    alerts.console_message(obj,["bridge"],alerts.ansi_cmd("Subel","Of course, if we fire, we will be fired upon. So we need to set shields too. First allocate power to shields: '{:s}' and '{:s}'".format("alloc hto 100 0 0", "alloc MSC 0 100 0")))
                    done = True
                elif(tutorial[1] == 25):
                    alerts.console_message(obj,["bridge"],alerts.ansi_cmd("Subel","Then set the frequency for the shields: '{:s}'. Make sure the others dont know!".format("freq shield 1")))
                    done = True
                elif(tutorial[1] == 26):
                    alerts.console_message(obj,["bridge"],alerts.ansi_cmd("Subel","And finally raise the shields: '{:s}'".format("alloc shield 16.6 16.6 16.6 16.6 16.6 16.6")))
                    done = True
                elif(tutorial[1] == 27):
                    alerts.console_message(obj,["bridge"],alerts.ansi_cmd("Subel","Now, the last thing I want to give to you is the communications array. You can hail other ships by setting the hailing frequency: '{:s}'".format("freq comms 100")))
                    done = True
                elif(tutorial[1] == 28):
                    alerts.console_message(obj,["bridge"],alerts.ansi_cmd("Subel","And you can transmit using the following command: '{:s}'".format("transmit <freq> <range> <message>")))
                    done = True
                elif(tutorial[1] == 29):
                    alerts.console_message(obj,["bridge"],alerts.ansi_cmd("Subel","That is all I can give for now. Good luck! *static noise*"))
                    done = True
                else:
                    obj.tags.remove(category="tutorial")
                if (done == True):
                    obj.db.tutorial[1] = tutorial[1] + 1
    if (count == 0):
        TICKER_HANDLER.remove(10,update_tutorial,"tutorial")
    return count