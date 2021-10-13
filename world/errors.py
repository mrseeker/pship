"""
All the error codes given by the ship
"""
from world import alerts,constants

def error_on_console(self,obj):
    if(obj.db.structure["type"] == 0):
        alerts.notify(self, alerts.ansi_red("Space object not loaded"))
    elif(obj.db.status["crippled"] == 2):
        alerts.notify(self, alerts.ansi_red("Space object destroyed"))
    elif(not obj.db.status["active"]):
        alerts.notify(self, alerts.ansi_red(obj.name + " systems are inactive."))
    elif(obj.db.status["crippled"]):
        alerts.notify(self, alerts.ansi_red("Controls are inoperative."))
    else:
        obj.db.status["time"] = obj.db.move["time"]
        return 0
    return 1

def error_on_contact(self,n1,n2):
    if (n2 == constants.SENSOR_FAIL):
        alerts.notify(self, alerts.ansi_red("That is not a valid sensor contact."))
    elif(n2.db.structure["type"] == 0):
        alerts.notify(self, alerts.ansi_red("That is not a valid sensor contact."))
        alerts.write_spacelog(self, n2, "BUG:Sensor contact has bad TYPE")
    elif(n2.db.space != n1.db.space):
        alerts.notify(self, alerts.ansi_red("That is not a valid sensor contact."))
        alerts.write_spacelog(self, n2, "BUG:Sensor contact has bad SPACE")
    else:
        return 0
    return 1
    