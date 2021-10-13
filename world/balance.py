"""
The world must be in balance, else we are having issues.
"""

from world import constants

def balance_eng_power(self):
    total = self.db.alloc["helm"] + self.db.alloc["tactical"] + self.db.alloc["operations"]
    if (total > 0.0):
        self.db.alloc["helm"] /= total
        self.db.alloc["tactical"] /= total
        self.db.alloc["operations"] /= total
    else:
        self.db.alloc["helm"] = 0.0
        self.db.alloc["tactical"] = 0.0
        self.db.alloc["operations"] = 1.0

def balance_helm_power(self):
    if (self.db.alloc["helm"] > 0.0):
        total = self.db.alloc["movement"] + self.db.alloc["shields"] + self.db.alloc["cloak"]
        if (total > 0.0):
            total /= self.db.alloc["helm"]
            self.db.alloc["movement"] /= total
            self.db.alloc["shields"] /= total
            self.db.alloc["cloak"] /= total
        else:
            self.db.alloc["shields"] = self.db.alloc["helm"]
            self.db.alloc["movement"] = 0.0
            self.db.alloc["cloak"] = 0.0
    else:
        self.db.alloc["movement"] = 0.0
        self.db.alloc["shields"] = 0.0
        self.db.alloc["cloak"] = 0.0

def balance_shield_power(self):
    total = 0.0
    if(self.db.alloc["shields"] > 0.0):
        for i in range(constants.MAX_SHIELD_NAME):
            total += self.db.alloc["shield"][i]
        if (total > 0.0):
            total /= self.db.alloc["shields"]
            for i in range(constants.MAX_SHIELD_NAME):
                self.db.alloc["shield"][i] /= total
        else:
            for i in range(constants.MAX_SHIELD_NAME):
                self.db.alloc["shield"][i] = self.db.alloc["shields"] / constants.MAX_SHIELD_NAME
    else:
        for i in range(constants.MAX_SHIELD_NAME):
            self.db.alloc["shield"][i] = 0

def balance_tact_power(self):
    if (self.db.alloc["tactical"] > 0.0):
        total = self.db.alloc["beams"] + self.db.alloc["missiles"] + self.db.alloc["sensors"]
        if (total > 0.0):
            total /= self.db.alloc["tactical"]
            self.db.alloc["beams"] /= total
            self.db.alloc["missiles"] /= total
            self.db.alloc["sensors"] /= total
        else:
            self.db.alloc["beams"] = 0
            self.db.alloc["missiles"] = 0
            self.db.alloc["sensors"] = self.db.alloc["tactical"]
    else:
        self.db.alloc["beams"] = 0.0
        self.db.alloc["missiles"] = 0.0
        self.db.alloc["sensors"] = 0.0

def balance_sensor_power(self):
    if (self.db.alloc["sensors"] > 0.0):
        total = self.db.alloc["ecm"] + self.db.alloc["eccm"]
        if (total > 0.0):
            total /= self.db.alloc["sensors"]
            self.db.alloc["ecm"] /= total
            self.db.alloc["eccm"] /= total
        else:
            self.db.alloc["ecm"] = self.db.alloc["sensors"] / 2.0
            self.db.alloc["eccm"] = self.db.alloc["sensors"] / 2.0 
    else:
        self.db.alloc["ecm"] = 0.0
        self.db.alloc["eccm"] = 0.0

def balance_ops_power(self):
    if (self.db.alloc["operations"] > 0.0):
        total = self.db.alloc["transporters"] + self.db.alloc["tractors"] + self.db.alloc["miscellaneous"]
        if (total > 0.0):
            total /= self.db.alloc["operations"]
            self.db.alloc["transporters"] /= total
            self.db.alloc["tractors"] /= total
            self.db.alloc["miscellaneous"] /= total
        else:
            self.db.alloc["transporters"] = 0.0
            self.db.alloc["tractors"] = 0.0
            self.db.alloc["miscellaneous"] = self.db.alloc["operations"]
    else:
        self.db.alloc["transporters"] = 0.0
        self.db.alloc["tractors"] = 0.0
        self.db.alloc["miscellaneous"] = 0.0
