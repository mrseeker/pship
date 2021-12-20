"""
Handles all communication-related commands
"""

from evennia import default_cmds, CmdSet
from evennia.utils.search import search_object
from world import alerts, errors
from world import constants

class CommunicationCmdSet(CmdSet):
        
        key = "CommunicationCmdSet"
    
        def at_cmdset_creation(self):
            self.add(CmdTransmit())
            self.add(CmdFreq())

class CmdFreq(default_cmds.MuxCommand):
    """
    Commands related to the setting of frequencies.

    Usage: freq <device> <min> <max>

    Command list:
    device - Type of device (comms)
    min - Frequency in Mhz (1.000 to 999.999)
    max - Frequency in Mhz (1.000 to 999.999)
    """

    key="freq"
    help_category = "Communication"

    def func(self):
        self.args = self.args.split(" ")
        caller = self.caller
        obj_x = search_object(caller.location)[0]
        obj = search_object(obj_x.db.ship)[0]

        if(errors.error_on_console(caller,obj)):
            return 0
    
        if(len(self.args) == 3):
            if self.args[0][0] == "c" and self.args[0][1] == "o":
                if (float(self.args[1]) > constants.MAX_COMMS_FREQUENCY or float(self.args[1]) < constants.MIN_COMMS_FREQUENCY or float(self.args[2]) > constants.MAX_COMMS_FREQUENCY or float(self.args[2]) < constants.MIN_COMMS_FREQUENCY):
                    alerts.notify(caller,alerts.ansi_red("Wrong frequency. Make sure the frequency is between 1 and 1000 Mhz"))
                else:
                    obj.db.freq["min"] = float(self.args[1])
                    obj.db.freq["max"] = float(self.args[2])
            else:
                alerts.notify(caller,alerts.ansi_red("Wrong device: {.s}".format(self.args[0])))    
        else:
            alerts.notify(caller,alerts.ansi_red("Wrong command entered."))

class CmdTransmit(default_cmds.MuxCommand):
    """
    Commands related to the transmitting a message.

    Usage: transmit/[switch] <freq> <range> <message>
    
    Switches:
    enc - Send an encrypted message (<freq> <range> <code> <message>)
    lang - Send a message in another language (<freq> <range> <language> <message>)
    enclang - Send an encrypted message in another language (<freq> <range> <code> <language> <message>)

    Command list:
    freq - Frequency in Mhz (1.000 to 999.999)
    range - Range to transmit in parsecs
    message - Message to be sent
    """

    key = "transmit"
    aliases = ["trans"]
    help_category = "Communication"
    
    def func(self):
        self.args = self.args.split(" ")
        caller = self.caller
        obj_x = search_object(self.caller.location)[0]
        obj = search_object(obj_x.db.ship)[0]

        if(errors.error_on_console(caller,obj)):
                return 0
        if("enc" in self.switches):
            alerts.transmit_message(caller,obj,float(self.args[0]),float(self.args[1]),self.args[2],' '.join(self.args[3:]))
        elif("enclang" in self.switches):
            alerts.transmit_message(caller,obj,float(self.args[0]),float(self.args[1]),self.args[2],' '.join(self.args[4:]),self.args[3])
        elif("lang" in self.switches):
            alerts.transmit_message(caller,obj,float(self.args[0]),float(self.args[1]),None,' '.join(self.args[3:]),self.args[2])
        elif(len(self.args) > 3):
            alerts.transmit_message(caller,obj,float(self.args[0]),float(self.args[1]),None,' '.join(self.args[2:]))
        else:
            self.caller.msg("Command not found: " + str(self.args))
