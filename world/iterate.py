"""
Iterates the world and it's settings
"""

import time
from world import constants, alerts, utils, balance, damage
from world import set as setter
from evennia.utils.search import search_tag,search_object
from evennia import gametime
from evennia.scripts.tickerhandler import TICKER_HANDLER
import math
import random
import sys

from world.unparse import unparse_identity, unparse_type

def up_alloc_balance(self):
    balance.balance_eng_power(self)
    balance.balance_helm_power(self)
    balance.balance_shield_power(self)
    balance.balance_tact_power(self)
    balance.balance_sensor_power(self)
    balance.balance_ops_power(self)
    alerts.report_eng_power(self)
    alerts.report_helm_power(self)
    alerts.report_tact_power(self)
    alerts.report_ops_power(self)
    self.db.alloc["version"] = 0
    self.db.engine["version"] = 1
    self.db.sensor["version"] = 1
    self.db.cloak["version"] = 1
    
def up_main_io(self):
    if self.db.main["gw"]:
        if (self.db.main["out"] > self.db.main["in"]):
            self.db.main["out"] -= self.db.move["dt"] / 30.0
            if (self.db.main["out"] <= self.db.main["in"]):
                self.db.main["out"] = self.db.main["in"]
                alerts.main_balance(self)
        elif(self.db.main["out"] < self.db.main["in"]):
            self.db.main["out"] += self.db.move["dt"] / 60.0
            if (self.db.main["out"] >= self.db.main["in"]):
                self.db.main["out"] = self.db.main["in"]
                alerts.main_balance(self)
    self.db.power["main"] = self.db.main["gw"] * self.db.main["out"]
    self.db.power["version"] = 1
    
def up_aux_io(self):
    if self.db.aux["gw"]:
        if (self.db.aux["out"] > self.db.aux["in"]):
            self.db.aux["out"] -= self.db.move["dt"] / 5.0
            if (self.db.aux["out"] <= self.db.aux["in"]):
                self.db.aux["out"] = self.db.aux["in"]
                alerts.aux_balance(self)
        elif(self.db.aux["out"] < self.db.main["in"]):
            self.db.aux["out"] += self.db.move["dt"] / 10.0
            if (self.db.aux["out"] >= self.db.aux["in"]):
                self.db.aux["out"] = self.db.aux["in"]
                alerts.aux_balance(self)
    self.db.power["aux"] = self.db.aux["gw"] * self.db.aux["out"]
    self.db.power["version"] = 1

def up_batt_io(self):
    self.db.batt["out"] = self.db.batt["in"]
    alerts.batt_balance(self)
    self.db.power["batt"] = self.db.batt["gw"] * self.db.batt["out"]
    self.db.power["version"] = 1
    

def up_main_damage(self):
    if (self.db.main["exist"] == 1):
        dmg = (self.db.main["out"] - self.db.main["damage"]) * self.db.move["dt"] / self.db.tech["main_max"] / 1000.0
        if (self.db.main["damage"] > 0.0 and (self.db.main["damage"] - dmg) <= 0.0):
            alerts.main_overload(self)
        self.db.main["damage"] -= dmg
        if (self.db.main["damage"] <= -1.0):
            self.db.main["damage"] = -1.0
            alerts.all_console_notify(self,alerts.ansi_warn("Impulse Drive core breach."))
            damage.damage_structure(self.db.power["main"] * (random(0,100)+1.0))
            self.db.main["in"] = 0.0
            self.db.main["out"] = 0.0
            self.db.power["main"] = 0.0
            self.db.power["version"] = 1
            

def up_aux_damage(self):
    if (self.db.aux["exist"] == 1):
        dmg = (self.db.aux["out"] - self.db.aux["damage"]) * self.db.move["dt"] / self.db.tech["aux_max"] / 1000.0
        if (self.db.aux["damage"] > 0.0 and (self.db.aux["damage"] - dmg) <= 0.0):
            alerts.aux_overload(self)
        self.db.aux["damage"] -= dmg
        if (self.db.aux["damage"] <= -1.0):
            self.db.aux["damage"] = -1.0
            alerts.all_console_notify(self,alerts.ansi_warn("fusion reactor core breach."))
            damage.damage_structure(self.db.power["aux"] * (random(0,100)+1.0))
            self.db.aux["in"] = 0.0
            self.db.aux["out"] = 0.0
            self.db.power["aux"] = 0.0
            self.db.power["version"] = 1

def up_fuel(self):
    mloss = self.db.main["out"] * self.db.main["out"] * self.db.main["gw"] * 100.0 / self.db.tech["fuel"] * self.db.move["dt"]
    aloss = self.db.aux["out"] * self.db.aux["out"] * self.db.aux["gw"] * 100.0 / self.db.tech["fuel"] * self.db.move["dt"]
    
    self.db.fuel["antimatter"] -= mloss
    self.db.fuel["deuterium"] -= mloss + aloss
    if (self.db.fuel["antimatter"] < 0.0):
        if(self.db.main["out"] > 0.0):
            alerts.anti_runout(self)
        self.db.fuel["antimatter"] = 0.0
        self.db.main["in"] = 0.0
        self.db.main["out"] = 0.0
        self.db.power["main"] = 0.0
        self.db.power["version"] = 1
        
    if (self.db.fuel["deuterium"] < 0.0):
        if (self.db.aux["out"] > 0.0 or self.db.main["out"] > 0.0):
            alerts.deut_runout(self)
        self.db.fuel["deuterium"] = 0.0
        self.db.main["in"] = 0.0
        self.db.main["out"] = 0.0
        self.db.power["main"] = 0.0
        self.db.aux["in"] = 0.0
        self.db.aux["out"] = 0.0
        self.db.power["aux"] = 0.0
        self.db.power["version"] = 1
        
def up_reserve(self):
    self.db.fuel["reserves"] += (((self.db.power["main"] + self.db.power["aux"] + self.db.power["batt"]) * self.db.alloc["miscellaneous"]) - self.db.power["batt"]) * self.db.move["dt"]
    if (self.db.fuel["reserves"] < 0.0):
        self.db.fuel["reserves"] = 0.0
        self.db.batt["in"] = 0.0
        self.db.batt["out"] = 0.0
        self.db.power["batt"] = 0.0
        alerts.batt_runout(self)
    elif (self.db.fuel["reserves"] > utils.sdb2max_reserves(self)):
        self.db.fuel["reserves"] = utils.sdb2max_reserves(self)
        
def up_total_power(self):
    self.db.power["total"] = self.db.power["main"] + self.db.power["aux"] + self.db.power["batt"]
    self.db.power["version"] = 0
    self.db.engine["version"] = 1
    self.db.sensor["version"] = 1
    self.db.cloak["version"] = 1
    up_turn_rate(self)
    
def up_warp_damage(self):
    if (self.db.engine["warp_exist"] == 1):
        if(math.fabs(self.db.move["out"]) >= 1.0):
            if (math.fabs(self.db.move["out"]) > self.db.engine["warp_cruise"]):
                self.db.engine["warp_damage"] -= (math.fabs(self.db.move["out"]) - self.db.engine["warp_cruise"]) * self.db.move["dt"] / self.db.tech["main_max"] / 10000.0
                if (self.db.engine["warp_damage"] < 0.0):
                    self.db.move["in"] = 0.0
                    self.db.move["out"] = 0.0
                    self.db.move["v"] = 0.0
                    alerts.warp_overload(self)
                    alerts.speed_stop(self)
                    alerts.ship_exit_warp(self)
                up_warp_max(self)

def up_impulse_damage(self):
    if(self.db.engine["impulse_exist"] == 1):
        if(math.fabs(self.db.move["out"]) < 1.0):
            if(math.fabs(self.db.move["out"]) > self.db.engine["impulse_cruise"] and math.fabs(self.db.move["in"]) < 1.0):
                self.db.engine["impulse_damage"] -= (math.fabs(self.db.move["out"])-self.db.engine["impulse_cruise"]) * self.db.move["dt"] / self.db.tech["aux_max"] / 10000.0
                if (self.db.engine["impulse_damage"] < 0.0):
                    self.db.move["in"] = 0.0
                    self.db.move["out"] = 0.0
                    self.db.move["v"] = 0.0
                    alerts.impulse_overload(self)
                    alerts.speed_stop(self)
                up_impulse_max(self)

def up_warp_max(self):
    self.db.engine["warp_max"] = utils.sdb2max_warp(self)
    self.db.engine["warp_cruise"] = utils.sdb2cruise_warp(self)
    
    if((self.db.move["in"] >= 1.0) and (self.db.move["in"] > self.db.engine["warp_max"])):
        self.db.move["in"] = self.db.engine["warp_max"]
    elif((self.db.move["in"] <= -1.0) and (self.db.move["in"] < (self.db.engine["warp_max"] / 2.0))):
        self.db.move["in"] = -self.db.engine["warp_max"] / 2.0

def up_impulse_max(self):
    self.db.engine["impulse_max"] = utils.sdb2max_impulse(self)
    self.db.engine["impulse_cruise"] = utils.sdb2cruise_impulse(self)
    
    if((self.db.move["in"] >= 0.0) and (self.db.move["in"] < 1.0) and (self.db.move["in"] > self.db.engine["impulse_max"])):
        self.db.move["in"] = self.db.engine["impulse_max"]
    elif((self.db.move["in"] > -1.0) and (self.db.move["in"] < 0.0) and (self.db.move["in"] < (-self.db.engine["impulse_max"] / 2.0))):
        self.db.move["in"] = -self.db.engine["impulse_max"] / 2.0

def up_tract_status(self):
    if(self.db.status["tractoring"] == 1):
        x = self.db.status["tractoring"]
        obj_x = search_object(x)[0]
        p = self.db.tract["damage"] * self.db.power["total"] * self.db.alloc["tractors"] / (utils.sdb2range(self,obj_x) + 1.0)
        if((obj_x.db.tract["active"] and p < obj_x.db.tract["damage"] * obj_x.db.power["total"] * obj_x.db.alloc["tractors"]) or p < 1.0):
            alerts.tract_lost(self)
            self.db.tract["lock"] = 0
            self.db.status["tractoring"] = 0
            obj_x.db.status["tractored"] = 0
            self.db.power["version"] = 1
            obj_x.db.power["version"] = 1
        elif(self.db.status["tractored"] and self.db.tract["active"]):
            x = self.db.status["tractored"]
            obj_x = search_object(x)[0]
            p = self.db.tract["damage"] * self.db.power["total"] * self.db.alloc["tractors"] / (utils.sdb2range(obj_x,self) + 1.0)
            if (p < (self.db.tract["damage"] * self.db.power["total"] * self.db.alloc["tractors"])):
                alerts.tract_lost(self)
                obj_x.db.tract["lock"]=0
                obj_x.db.status["tractoring"] = 0
                self.db.status["tractored"] = 0
                self.db.power["version"] = 1
                obj_x.db.power["version"] = 1

def up_cloak_status(self):
    if(self.db.cloak["active"] == 1):
        if(self.db.alloc["cloak"] * self.db.power["total"] < self.db.cloak["cost"]):
            alerts.cloak_failure(self)
            alerts.ship_cloak_offline(self)
            self.db.cloak["active"] = 0
            self.db.sensor["version"] = 1
            self.db.engine["version"] = 1
    self.db.cloak["version"] = 0

def up_beam_io(self):
    if(self.db.beam["out"] > self.db.beam["in"]):
        self.db.beam["out"] = self.db.beam["in"]
        alerts.beam_balance(self)
    elif(self.db.alloc["beams"] * self.db.power["total"] > 0.0):
        self.db.beam["out"] += self.db.alloc["beams"] * self.db.power["total"] * self.db.move["dt"]
        if (self.db.beam["out"] >= self.db.beam["in"]):
            self.db.beam["out"] = self.db.beam["in"]
            alerts.beam_charged(self)
    if(self.db.beam["out"] < 0.0):
        self.db.beam["out"] = 0.0
    self.db.sensor["version"] = 1
    
def up_empire(self):
    space_obj = search_tag(constants.EMPIRE_ATTR_NAME,category="space_object")
    best_range = sys.maxsize
    best_empire = ""
    for obj in space_obj:
        if(obj.db.status["active"] == 1):
            if (obj.db.space != 0 and self.db.space != obj.db.space):
                continue
            dx = (obj.db.coords["x"] - self.db.coords["x"]) / constants.PARSEC
            dy = (obj.db.coords["y"] - self.db.coords["y"]) / constants.PARSEC
            dz = (obj.db.coords["z"] - self.db.coords["z"]) / constants.PARSEC
            range = (dx * dx + dy * dy + dz * dz)
            inside_range = math.fabs(range - (obj.db.radius * obj.db.radius))
            
            if (range <= (obj.db.radius * obj.db.radius)): #object in radius
                if (best_empire == "" or inside_range < best_range): #closer to center than previous best
                    best_range = range
                    best_empire = obj.name
    if (self.db.move["empire"] != best_empire):
        if (self.db.move["empire"] != ""):
            same = 0
            if (self.db.move["empire"] == best_empire):
                same = 1
            if (same == 0):
                alerts.exit_empire(self)
                if(random.randint(1,100) < (self.db.sensor["lrs_signature"] * self.db.sensor["visibility"] * 100.0)):
                    alerts.border_cross(self,0)
        if (self.db.move["empire"] == ""):
            self.db.move["empire"] = best_empire
            alerts.enter_empire(self)
            if(random.randint(1,100) < (self.db.sensor["lrs_signature"] * self.db.sensor["visibility"] * 100.0)):
                alerts.border_cross(self,1)
        self.db.move["empire"] = best_empire
    
def up_missile_io(self):
    if (self.db.missile["out"] > self.db.missile["in"]):
        self.db.missile["out"] = self.db.missile["in"]
        alerts.missile_balance(self)
    elif(self.db.alloc["missiles"] * self.db.power["total"] > 0.0):
        self.db.missile["out"] += self.db.alloc["missiles"] * self.db.power["total"] * self.db.move["dt"]
        if (self.db.missile["out"] >= self.db.missile["in"]):
            self.db.missile["out"] = self.db.missile["in"]
            alerts.missile_charged(self)
    if(self.db.missile["out"] < 0.0):
        self.db.missile["out"] = 0.0
    self.db.sensor["version"] = 1
        
def up_autopilot(self):
    r = utils.xyz2range(self.db.coords["x"],self.db.coords["y"],self.db.coords["z"],self.db.coords["xd"],self.db.coords["yd"],self.db.coords["zd"])
    speed = 99
    autopilot = self.db.status["autopilot"]
    
    if(r < 1.0):
        speed = 0
        autopilot = 0
        alerts.console_message(self,["helm"],alerts.ansi_notify("Autopilot destination reached"))
    elif(r < 2):
        speed = 0.01
        autopilot = 1
    elif(r < 4):
        speed = 0.02
        autopilot = 2
    elif(r < 8):
        speed = 0.04
        autopilot = 3
    elif(r < 16):
        speed = 0.08
        autopilot = 4
    elif(r < 32):
        speed = 0.16
        autopilot = 5
    elif(r < 64):
        speed = 0.32
        autopilot = 6
    elif(r < 128):
        speed = 0.64
        autopilot = 7
    else:
        r /= self.db.move["cochranes"] * constants.LIGHTSPEED
        if (r < 1.0):
            speed = 0.999
            autopilot = 8
        elif(r < 10.0):
            speed = math.pow(r / int(r),0.3)
            autopilot = 9
        elif(r < 20.0):
            speed = 1.2
            autopilot = 10
        elif(r < 40.0):
            speed = 1.5
            autopilot = 11
        elif(r < 80.0):
            speed = 1.9
            autopilot = 12
        elif(r < 160.0):
            speed = 2.3
            autopilot = 13
            
        elif(r < 320.0):
            speed = 2.8
            autopilot = 14
        elif(r < 640.0):
            speed = 3.5
            autopilot = 15
        elif(r < 1280.0):
            speed = 4.3
            autopilot = 16
        elif(r < 2560.0):
            speed = 5.2
            autopilot = 17
        elif(r < 5120.0):
            speed = 6.5
            autopilot = 18
        elif(r < 10240.0):
            speed = 8.0
            autopilot = 19
        elif(r < 20480.0):
            speed = 9.8
            autopilot = 20
        elif(r < 40960.0):
            speed = 12.1
            autopilot = 21
        elif(r < 81920.0):
            speed = 14.9
            autopilot = 22
        elif(r < 163840.0):
            speed = 18.4
            autopilot = 23
        elif(r < 327680.0):
            speed = 22.6
            autopilot = 24
        elif(r < 655360.0):
            speed = 27.9
            autopilot = 25
        elif(r < 1310720.0):
            speed = 34.3
            autopilot = 26
        elif(r < 2621440.0):
            speed = 42.2
            autopilot = 27
        elif(r < 5242880.0):
            speed = 52.0
            autopilot = 28
        elif(r < 10485760.0):
            speed = 64.0
            autopilot = 29
    
    if(self.db.status["autopilot"] != autopilot):
        self.db.status["autopilot"] = autopilot
        self.db.course["yaw_in"] = utils.xy2bearing(self.db.coords["xd"] - self.db.coords["x"],self.db.coords["yd"] - self.db.coords["y"])
        self.db.course["pitch_in"] = utils.xyz2elevation(self.db.coords["xd"] - self.db.coords["x"],self.db.coords["yd"] - self.db.coords["y"],self.db.coords["zd"] - self.db.coords["z"])
        if(self.db.move["in"] > speed):
            if (speed >=1.0 and speed > self.db.engine["warp_cruise"]):
                speed = self.db.engine["warp_cruise"]
            if (speed < 1.0 and speed > self.db.engine["impulse_cruise"]):
                speed = self.db.engine["impulse_cruise"]
            self.db.move["in"] = speed

def up_speed_io(self):
    if (self.db.move["ratio"] <= 0.0):
        return
    if (math.fabs(self.db.move["out"]) < 1.0):
        if(math.fabs(self.db.move["in"]) >= 1.0):
            a = self.db.power["main"] * 0.99 + self.db.power["total"] * self.db.alloc["movement"] * 0.01
        else:
            a = self.db.power["aux"] * 0.9 + self.db.power["total"] * self.db.alloc["movement"] * 0.1
        a *= (1.0 - math.fabs(self.db.move["out"]))/ self.db.move["ratio"] / 50.0
    else:
        a = (self.db.power["main"] * 0.99 + self.db.power["total"] * self.db.alloc["movement"] * 0.01) / self.db.move["ratio"] / math.fabs(self.db.move["out"]) / 5.0
    a *= (self.db.move["ratio"] + 1.0) / self.db.move["ratio"] * self.db.move["dt"]
    
    if (self.db.move["out"] < 0.0):
        a /= 2.0
    
    if (self.db.status["tractoring"]):
        x = self.db.status["tractoring"]
        obj_x = search_object(x)[0]
        
        a *= (self.db.structure["displacement"] + 0.1) / (obj_x.db.structure["displacement"] + self.db.structure["displacement"] + 0.1)
    elif(self.db.status["tractored"]):
        x = self.db.status["tractored"]
        obj_x = search_object(x)[0]
        a *= (self.db.structure["displacement"] + 0.1) / (obj_x.db.structure["displacement"] + self.db.structure["displacement"] + 0.1)
    
    if (a < 0.01):
        a = 0.01
    
    if((self.db.move["in"] >= 1.0) and (self.db.move["in"] > self.db.engine["warp_max"])):
        self.db.move["in"] = self.db.engine["warp_max"]
    elif((self.db.move["in"] <= -1.0) and (self.db.move["in"] < (-self.db.engine["warp_max"] / 2.0))):
        self.db.move["in"] = -self.db.engine["warp_max"] / 2.0
    elif((self.db.move["in"] >= 0.0) and (self.db.move["in"] < 1.0) and (self.db.move["in"] > self.db.engine["impulse_max"])):
        self.db.move["in"] = self.db.engine["impulse_max"]
    elif((self.db.move["in"] <= 0.0) and (self.db.move["in"] > -1.0) and (self.db.move["in"] < (-self.db.engine["impulse_max"] / 2.0))):
        self.db.move["in"] = - self.db.engine["impulse_max"] / 2.0
        
    if(self.db.move["out"] > self.db.move["in"]):
        if (self.db.move["out"] >= 1.0):
            if (self.db.move["in"] >= 1.0):
                self.db.move["out"] = self.db.move["in"]
                alerts.speed_warp(self)
            elif(self.db.move["in"] > 0.0 and self.db.move["in"] < 1.0):
                self.db.move["out"] = self.db.move["in"]
                alerts.speed_impulse(self)
                alerts.ship_exit_warp(self)
            elif(self.db.move["in"] <= 0.0):
                self.db.move["out"] = 0.0
                alerts.speed_stop(self)
                alerts.ship_exit_warp(self)
                
            elif(self.db.move["out"] > 0.0 and self.db.move["out"] < 1.0):
                if (self.db.move["in"] > 0.0):
                    self.db.move["out"] = self.db.move["in"]
                    alerts.speed_impulse(self)
                elif(self.db.move["in"] <= 0.0):
                    self.db.move["out"] = 0.0
                    alerts.speed_stop(self)
            elif(self.db.move["out"] <= 0.0):
                if (self.db.move["out"] > -1.0):
                    self.db.move["out"] -= a
                    if (self.db.move["out"] <= self.db.move["in"]):
                        self.db.move["out"] = self.db.move["in"]
                        if (self.db.move["out"] > -1.0):
                            alerts.speed_impulse(self)
                        else:
                            alerts.speed_warp(self)
                            alerts.ship_enter_warp(self)
                    elif(self.db.move["out"] <= -1.0):
                        alerts.ship_enter_warp(self)
            else:
                self.db.move["out"] -= a
                if (self.db.move["out"] <= self.db.move["in"]):
                    self.db.move["out"] = self.db.move["in"]
                    alerts.speed_warp(self)
    elif(self.db.move["out"] < self.db.move["in"]):
        if (self.db.move["out"] <= -1.0):
            if (self.db.move["in"] <= -1.0):
                self.db.move["out"] = self.db.move["in"]
                alerts.speed_warp(self)
            elif(self.db.move["in"]< 0.0 and self.db.move["in"] > -1.0):
                self.db.move["out"] = self.db.move["in"]
                alerts.speed_impulse(self)
                alerts.ship_exit_warp(self)
            elif(self.db.move["in"] >= 0.0):
                self.db.move["out"] = 0.0
                alerts.speed_stop(self)
                alerts.ship_exit_warp(self)
        elif (self.db.move["out"] < 0.0 and self.db.move["out"] > -1.0):
            if (self.db.move["in"] < 0.0):
                self.db.move["out"] = self.db.move["in"]
                alerts.speed_impulse(self)
            elif(self.db.move["in"] >= 0.0):
                self.db.move["out"] = 0.0
                alerts.speed_stop(self)
        elif(self.db.move["out"] >= 0.0):
            if (self.db.move["out"] < 1.0):
                self.db.move["out"] += a
                if (self.db.move["out"] >= self.db.move["in"]):
                    self.db.move["out"] = self.db.move["in"]
                    if (self.db.move["out"] < 1.0):
                        alerts.speed_impulse(self)
                    else:
                        alerts.speed_warp(self)
                        alerts.ship_enter_warp(self)
                elif(self.db.move["out"] >= 1.0):
                    alerts.ship_enter_warp(self)
            else:
                self.db.move["out"] += a
                if (self.db.move["out"] >= self.db.move["in"]):
                    self.db.move["out"] = self.db.move["in"]
                    alerts.speed_warp(self)
    
    self.db.sensor["version"] = 1

def up_turn_rate(self):
    a = 0
    if(self.db.move["ratio"] <= 0.0):
        return
    if(math.fabs(self.db.move["out"]) < 1.0):
        if(math.fabs(self.db.move["in"]) >= 1.0):
            a = self.db.power["main"] * 0.99 + self.db.power["total"] * self.db.alloc["movement"] * 0.01
        else:
            a = self.db.power["aux"] * 0.9 + self.db.power["total"] * self.db.alloc["movement"] * 0.1
        a *= 3.6 * (1.0 - math.fabs(self.db.move["out"])) / self.db.move["ratio"]
    else:
        a = 3.6 * (self.db.power["main"] * 0.99 + self.db.power["total"] * self.db.alloc["movement"] * 0.01) / self.db.move["ratio"] / math.fabs(self.db.move["out"])
    
    a *= (self.db.move["ratio"] + 1.0) / self.db.move["ratio"] * self.db.move["dt"]
    
    if (self.db.move["out"] < 0.0):
        a /= 2.0
    
    if (self.db.status["tractoring"] == 1):
        x = self.db.status["tractoring"]
        obj_x = search_object(x)[0]
        
        a *= (self.db.structure["displacement"] + 0.1) / (obj_x.db.structure["displacement"] + self.db.structure["displacement"] + 0.1)
    elif(self.db.status["tractored"] == 1):
        x = self.db.status["tractored"]
        obj_x = search_object(x)[0]
        a *= (self.db.structure["displacement"] + 0.1) / (obj_x.db.structure["displacement"] + self.db.structure["displacement"] + 0.1)
    
    if(a < 1.0):
        a = 1.0
        
    self.db.course["rate"] = a

def up_cochranes(self):
    self.db.move["cochranes"] = utils.xyz2cochranes(self.db.coords["x"],self.db.coords["y"],self.db.coords["z"])

def up_velocity(self):
    if (self.db.engine["warp_exist"] or self.db.engine["impulse_exist"]):
        if (self.db.move["out"] >= 1.0):
            self.db.move["v"] = constants.LIGHTSPEED * pow(self.db.move["out"],3.333333)
        elif (self.db.move["out"] <= -1.0):
            self.db.move["v"] = constants.LIGHTSPEED * -pow(math.fabs(self.db.move["out"]),3.333333)
        else:
            self.db.move["v"] = constants.LIGHTSPEED * self.db.move["out"]

def up_quadrant(self):
    q = -1
    if(self.db.coords["x"] > 0.0):
        if (self.db.coords["y"] > 0.0):
            q = 3
        else:
            q = 2
    else:
        if (self.db.coords["y"] > 0.0):
            q = 1
        else:
            q = 0
    if(self.db.move["quadrant"] != q):
        self.db.move["quadrant"] = q
        alerts.enter_quadrant(self)

def up_visibility(self):
    if (self.db.status["docked"] == 1 or self.db.status["landed"] == 1):
        self.db.sensor["visibility"] = 1.0
    else:
        self.db.sensor["visibility"] = float(utils.xyz2vis(self.db.coords["x"],self.db.coords["y"],self.db.coords["z"]))

def up_yaw_io(self):
    if(self.db.course["yaw_out"] < self.db.course["yaw_in"]):
        if((self.db.course["yaw_in"] - self.db.course["yaw_out"]) <= 180.0):
            self.db.course["yaw_out"] += self.db.course["rate"] * self.db.move["dt"]
            if (self.db.course["yaw_out"] >= self.db.course["yaw_in"]):
                self.db.course["yaw_out"] = self.db.course["yaw_in"]
                alerts.yaw(self)
        else:
            self.db.course["yaw_out"] -=self.db.course["rate"] * self.db.move["dt"]
            if (self.db.course["yaw_out"] < 0.0):
                self.db.course["yaw_out"] += 360.0
                if (self.db.course["yaw_out"] <= self.db.course["yaw_in"]):
                    self.db.course["yaw_out"] = self.db.course["yaw_in"]
                    alerts.yaw(self)
    
    else:
        if((self.db.course["yaw_out"] - self.db.course["yaw_in"]) <= 180.0):
            self.db.course["yaw_out"] -= self.db.course["rate"] * self.db.move["dt"]
            if (self.db.course["yaw_out"] <= self.db.course["yaw_in"]):
                self.db.course["yaw_out"] = self.db.course["yaw_in"]
                alerts.yaw(self)
        else:
            self.db.course["yaw_out"] +=self.db.course["rate"] * self.db.move["dt"]
            if (self.db.course["yaw_out"] >= 0.0):
                self.db.course["yaw_out"] -= 360.0
                if (self.db.course["yaw_out"] >= self.db.course["yaw_in"]):
                    self.db.course["yaw_out"] = self.db.course["yaw_in"]
                    alerts.yaw(self)

    self.db.course["version"] = 1

def up_pitch_io(self):
    if(self.db.course["pitch_out"] < self.db.course["pitch_in"]):
        if((self.db.course["pitch_in"] - self.db.course["pitch_out"]) <= 180.0):
            self.db.course["pitch_out"] += self.db.course["rate"] * self.db.move["dt"]
            if (self.db.course["pitch_out"] >= self.db.course["pitch_in"]):
                self.db.course["pitch_out"] = self.db.course["pitch_in"]
                alerts.pitch(self)
        else:
            self.db.course["pitch_out"] -=self.db.course["rate"] * self.db.move["dt"]
            if (self.db.course["pitch_out"] < 0.0):
                self.db.course["pitch_out"] += 360.0
                if (self.db.course["pitch_out"] <= self.db.course["pitch_in"]):
                    self.db.course["pitch_out"] = self.db.course["pitch_in"]
                    alerts.pitch(self)
    
    else:
        if((self.db.course["pitch_out"] - self.db.course["pitch_in"]) <= 180.0):
            self.db.course["pitch_out"] -= self.db.course["rate"] * self.db.move["dt"]
            if (self.db.course["pitch_out"] <= self.db.course["pitch_in"]):
                self.db.course["pitch_out"] = self.db.course["pitch_in"]
                alerts.pitch(self)
        else:
            self.db.course["pitch_out"] +=self.db.course["rate"] * self.db.move["dt"]
            if (self.db.course["pitch_out"] >= 0.0):
                self.db.course["pitch_out"] -= 360.0
                if (self.db.course["pitch_out"] >= self.db.course["pitch_in"]):
                    self.db.course["pitch_out"] = self.db.course["pitch_in"]
                    alerts.pitch(self)

    self.db.course["version"] = 1

def up_roll_io(self):
    if(self.db.course["roll_out"] < self.db.course["roll_in"]):
        if((self.db.course["roll_in"] - self.db.course["roll_out"]) <= 180.0):
            self.db.course["roll_out"] += self.db.course["rate"] * self.db.move["dt"]
            if (self.db.course["roll_out"] >= self.db.course["roll_in"]):
                self.db.course["roll_out"] = self.db.course["roll_in"]
                alerts.roll(self)
        else:
            self.db.course["roll_out"] -=self.db.course["rate"] * self.db.move["dt"]
            if (self.db.course["roll_out"] < 0.0):
                self.db.course["roll_out"] += 360.0
                if (self.db.course["roll_out"] <= self.db.course["roll_in"]):
                    self.db.course["roll_out"] = self.db.course["roll_in"]
                    alerts.roll(self)
    
    else:
        if((self.db.course["roll_out"] - self.db.course["roll_in"]) <= 180.0):
            self.db.course["roll_out"] -= self.db.course["rate"] * self.db.move["dt"]
            if (self.db.course["roll_out"] <= self.db.course["roll_in"]):
                self.db.course["roll_out"] = self.db.course["roll_in"]
                alerts.roll(self)
        else:
            self.db.course["roll_out"] +=self.db.course["rate"] * self.db.move["dt"]
            if (self.db.course["roll_out"] >= 0.0):
                self.db.course["roll_out"] -= 360.0
                if (self.db.course["roll_out"] >= self.db.course["roll_in"]):
                    self.db.course["roll_out"] = self.db.course["roll_in"]
                    alerts.roll(self)

    self.db.course["version"] = 1

def up_vectors(self):
    d2r = math.pi / 180.0
    sy = math.sin(self.db.course["yaw_out"] * d2r)
    cy = math.cos(self.db.course["yaw_out"] * d2r)
    sp = math.sin(self.db.course["pitch_out"] * d2r)
    cp = math.cos(self.db.course["pitch_out"] * d2r)
    sr = math.sin(self.db.course["roll_out"] * d2r)
    cr = math.cos(self.db.course["roll_out"] * d2r)

    self.db.course["d"][0][0] = cy * cp
    self.db.course["d"][0][1] = sy * cp
    self.db.course["d"][0][2] = sp
    self.db.course["d"][1][0] = -(sy * cr) + (cy * sp * sr)
    self.db.course["d"][1][1] = (cy * cr) + (sy * sp * sr)
    self.db.course["d"][1][2] = -(cp * sr)
    self.db.course["d"][2][0] = -(sy * sr) - (cy * sp * cr)
    self.db.course["d"][2][1] = (cy * sr) - (sy * sp * cr)
    self.db.course["d"][2][2] = (cp * cr)
    self.db.course["version"] = 0
    
def up_position(self):
    dv = self.db.move["v"] * self.db.move["dt"]
    if (math.fabs(self.db.move["out"]) >= 1.0):
        dv *= self.db.move["cochranes"]
    if (self.db.status["tractoring"] != 0):
        x = self.db.status["tractoring"]
        obj_x = search_object(x)[0]
        obj_x.coords["x"] += dv * self.db.course["d"][0][0]
        obj_x.coords["y"] += dv * self.db.course["d"][0][1]
        obj_x.coords["z"] += dv * self.db.course["d"][0][2]
    elif (self.db.status["tractored"] != 0):
        x = self.db.status["tractored"]
        obj_x = search_object(x)[0]
        obj_x.coords["x"] += dv * self.db.course["d"][0][0]
        obj_x.coords["y"] += dv * self.db.course["d"][0][1]
        obj_x.coords["z"] += dv * self.db.course["d"][0][2]
    self.db.coords["x"] += dv * self.db.course["d"][0][0]
    self.db.coords["y"] += dv * self.db.course["d"][0][1]
    self.db.coords["z"] += dv * self.db.course["d"][0][2]

def up_wormhole(self,obj,obj_x):
    alerts.do_ship_notify(obj,"The {:s} shudders and rocks about violently for a few moments.".format(obj.name))
    alerts.do_space_notify_two(obj,obj_x,["helm","tactical","science"],"enters")
    if(obj.db.cloak["active"] == 1):
        alerts.cloak_voided(obj)
        alerts.ship_cloak_offline(obj)
        obj.db.cloak["active"] = 0
        obj.db.sensor["version"] = 1
        obj.db.engine["version"] = 1
    
    #clear contacts and reset sensors
    for i in range(obj.db.sensor["contacts"]):
        tmp_c = search_object(obj.db.slist[i]["key"])[0]
        alerts.console_message(obj,["helm","science","tactical"],"{:s} contact lost: {:s}".format(unparse_type(tmp_c),unparse_identity(obj,tmp_c)))
    obj.db.sensor["contacts"] = 0
    up_sensor_message(obj,0,[""] * constants.MAX_SENSOR_CONTACTS,[0] * constants.MAX_SENSOR_CONTACTS)
    obj_link = search_object(obj_x.db.status["link"])
    if (len(obj_link) == 0):
        alerts.notify(alerts.ansi_red("{:s} loops back on itself.".format(obj_x.name)))
        alerts.write_spacelog(self,obj_x,"BUG: Bad wormhole link")
        obj_link = obj_x
    else:
        obj_link = obj_link[0]    
    obj.db.space = obj_link.db.space
    obj.db.coords["x"] = obj_link.db.coords["x"]
    obj.db.coords["y"] = obj_link.db.coords["y"]
    obj.db.coords["z"] = obj_link.db.coords["z"]
    obj.db.status["autopilot"] = 0
    alerts.do_space_notify_one(obj_link,["helm","tactical","science"],"expells an unknown contact")
    up_cochranes(obj)
    up_empire(obj)
    up_quadrant(obj)
    up_resolution(obj)
    up_signature(obj)
    up_visibility(obj)
    return

def up_resolution(self):
    if(self.db.sensor["lrs_active"] == 1):
        self.db.sensor["lrs_resolution"] = self.db.tech["sensors"] * self.db.sensor["lrs_damage"]
        if (self.db.sensor["ew_active"] == 1):
            self.db.sensor["lrs_resolution"] *= utils.sdb2eccm_lrs(self)
        if (self.db.cloak["active"] == 1):
            self.db.sensor["lrs_resolution"] /= 10.0
    else:
        self.db.sensor["lrs_resolution"] = 0.0
    if (self.db.sensor["srs_active"] == 1):
        self.db.sensor["srs_resolution"] = self.db.tech["sensors"] * self.db.sensor["srs_damage"]
        if (self.db.sensor["ew_active"] == 1):
            self.db.sensor["srs_resolution"] *= utils.sdb2eccm_srs(self)
        if(self.db.cloak["active"] == 1):
            self.db.sensor["srs_resolution"] /= 10.0
    else:
        self.db.sensor["srs_resolution"] = 0.0
        
def up_signature(self):
    base = math.pow(self.db.structure["displacement"],0.333333) / self.db.tech["stealth"] / 100.0
    sig = base
    
    if(self.db.cloak["active"] == 1):
        self.db.cloak["level"] = 0.001 / self.db.power["total"] / self.db.alloc["cloak"] / self.db.tech["cloak"] * self.db.cloak["cost"]
        if (self.db.status["tractored"] == 1):
            self.db.cloak["level"] *= 100.0
        if (self.db.status["tractoring"] == 1):
            self.db.cloak["level"] *= 100.0
        if (self.db.beam["out"] > 1.0):
            self.db.cloak["level"] *= self.db.beam["out"]
        if (self.db.missile["out"] > 1.0):
            self.db.cloak["level"] *= self.db.missile["out"]
        if (self.db.sensor["visibility"] < 1.0):
            self.db.cloak["level"] *= (1.0 - self.db.sensor["visibility"]) * 10000.0
        if (self.db.cloak["level"] > 1.0):
            self.db.cloak["level"] = 1.0
    else:
        self.db.cloak["level"] = 1.0
        
    self.db.sensor["lrs_signature"] = sig
    self.db.sensor["srs_signature"] = sig * 10.0
    self.db.sensor["lrs_signature"] *= self.db.move["out"] * self.db.move["out"] + 1.0
    self.db.sensor["srs_signature"] *= 1.0 + self.db.power["main"] + (self.db.power["aux"] / 10.0) + (self.db.power["batt"] / 100.0)
    if (self.db.sensor["ew_active"] == 1):
        self.db.sensor["lrs_signature"] /= utils.sdb2ecm_lrs(self)
        self.db.sensor["srs_signature"] /= utils.sdb2ecm_srs(self)
        
    self.db.sensor["version"] = 0
    
def up_sensor_message(self, contacts, t_sdb, t_lev):
    temp_num = [0] * constants.MAX_SENSOR_CONTACTS
    temp_sdb = t_sdb
    temp_lev = t_lev
    for i in range(contacts):
        gain = 0
        for j in range(contacts):
            if (temp_sdb[i] == self.db.slist[j]["key"]):
                gain = 1
                temp_num[i] = self.db.slist[j]["num"]
                break
        if (gain == 0):
            self.db.sensor["counter"] += 1
            if (self.db.sensor["counter"] > 999):
                self.db.sensor["counter"] = 1
            temp_num[i] = self.db.sensor["counter"]
            obj_x = search_object(temp_sdb[i])[0]
            alerts.console_message(self,["helm","science","tactical"],alerts.ansi_warn("New sensor contact ("+str(temp_num[i]) + "): " + str(constants.type_name[obj_x.db.structure["type"]])))
    for i in range(contacts):
        lose = 0
        for j in range(contacts):
            if(temp_sdb[j] == self.db.slist[i]["key"]):
                lose = 1
                break
        if (lose == 0):
            obj_x = search_object(self.db.slist[i]["key"])[0]
            alerts.console_message(self,["helm","science","tactical"],alerts.ansi_warn(str(constants.type_name[obj_x.db.structure["type"]]) + " contact lost: " + str(obj_x.db.name)))
            if (self.db.trans["s_lock"] == self.db.slist[i]["key"]):
                alerts.console_message(self,["operation","transporter"],alerts.ansi_warn("Transporters lost lock on " + str(obj_x.db.name)))
                self.db.trans.s_lock = 0
            if (self.db.trans["d_lock"] == self.db.slist[i]["key"]):
                alerts.console_message(self,["operation","transporter"],alerts.ansi_warn("Transporters lost lock on " + str(obj_x.db.name)))
                self.db.trans.d_lock = 0
            if (self.db.tract["lock"] == self.db.slist[i]["key"]):
                alerts.console_message(self,["helm","operation"],alerts.ansi_warn("Tractor beam lost lock on " + str(obj_x.db.name)))
                self.db.tract["lock"] = 0
                self.db.status["tractoring"] = 0
                obj_x.status["tractored"] = 0
                self.db.engine["version"] = 1
                obj_x.db.engine["version"] = 1
            flag = 0
            for j in range(self.db.beam["banks"]):
                if (self.db.blist[j]["lock"] == self.db.slist[i]["key"]):
                    flag = 1
                    self.db.blist[j]["lock"] = 0
            if (flag > 0):
                alerts.console_message(self,["tactical"],alerts.ansi_warn("Phaser Array lock lost on {:s}".format(obj_x.name)))
            flag = 0
            for j in range(self.db.missile["tubes"]):
                if (self.db.mlist[j]["lock"] == self.db.slist[i]["key"]):
                    flag = 1
                    self.db.mlist[j]["lock"] = 0
            if (flag > 0):
                alerts.console_message(self,["tactical"],alerts.ansi_warn("Missile lock lost on {:s}".format(obj_x.name)))
                
    self.db.sensor["contacts"] = contacts
    if (contacts == 0):
        self.db.sensor["counter"] = 0
    else:
        for i in range(contacts):
            self.db.slist[i]["key"] = temp_sdb[i]
            self.db.slist[i]["num"] = temp_num[i]
            self.db.slist[i]["lev"] = temp_lev[i]

def up_sensor_list(self):
    contacts = 0
    limit = constants.PARSEC * 100.0
    objects = search_tag(category="space_object")
    temp_sdb = [""]* constants.MAX_SENSOR_CONTACTS
    temp_lev = [0]* constants.MAX_SENSOR_CONTACTS
    
    for obj in objects:
        if (self.db.location == obj.db.location and self.db.space == obj.db.space and obj.db.structure["type"] > 0 and self.key != obj.key):
            x = math.fabs(self.db.coords["x"] - obj.db.coords["x"])
            if (x > limit):
                continue
            y = math.fabs(self.db.coords["y"] - obj.db.coords["y"])
            if (y > limit):
                continue
            z = math.fabs(self.db.coords["z"] - obj.db.coords["z"])
            if (z > limit):
                continue
            level = (self.db.sensor["srs_resolution"] + 0.01) * obj.db.sensor["srs_signature"] / (0.1 + (x * x + y * y + z * z) / 10101.010101)
            x /= constants.PARSEC
            y /= constants.PARSEC
            z /= constants.PARSEC
            if (level < 0.01):
                continue
            if(obj.db.cloak["active"] == 1):
                if (self.db.tech["sensors"] < 2.0):
                    level *= obj.db.cloak["level"]
            if (level < 0.01):
                continue
            temp_sdb.insert(contacts,obj.key)
            temp_lev.insert(contacts,level)
            contacts = contacts + 1
            if (contacts == constants.MAX_SENSOR_CONTACTS):
                break
    
    if (contacts != self.db.sensor["contacts"]):
        up_sensor_message(self,contacts,temp_sdb,temp_lev)
    else:
        for i in range(self.db.sensor["contacts"]):
            self.db.slist[i]["key"] = temp_sdb[i]
            self.db.slist[i]["lev"] = temp_lev[i]
    
def up_repair(self):
    self.db.structure["repair"] += self.db.move["dt"] * self.db.structure["max_repair"] / 1000.0 * (1.0 + math.sqrt(self.db.alloc["miscellaneous"] * self.db.power["total"]))
    if (self.db.structure["repair"] >= self.db.structure["max_repair"]):
        self.db.structure["repair"] = self.db.structure["max_repair"]
        alerts.max_repair(self)

def do_space_db_iterate():
    objects = search_tag(category="space_object")
    count = 0
    timer = time.time()
    for obj in objects:
        if (obj.db.status["active"] == 1 and obj.db.structure["type"] > 0):
            count = count + 1
            now = gametime.gametime(absolute=True)
            obj.db.move["dt"] = now - obj.db.move["time"]
            obj.db.move["time"] = now
            if (obj.db.move["dt"] > 0.0):
                if (obj.db.structure["type"] == 1):
                    if(obj.db.move["time"] - obj.db.status["time"] > 3600):
                        if(obj.db.main["in"] > 0.0):
                            setter.do_set_main_reactor(obj,0.0,obj)
                            obj.db.main["in"] = 0.0
                        if(obj.db.aux["in"] > 0.0):
                            setter.do_set_aux_reactor(obj,0.0,obj)
                            obj.db.aux["in"] = 0.0
                        if(obj.db.batt["in"] > 0.0):
                            setter.do_set_battery(obj,0.0,obj)
                        if(obj.db.power["total"] == 0.0):
                            setter.do_set_inactive(obj,obj)
                if(obj.db.move["dt"] > 60.0):
                    obj.db.move["dt"] = 60
                if(obj.db.alloc["version"] == 1):
                    up_alloc_balance(obj)
                if(obj.db.main["out"] != obj.db.main["in"]):
                    up_main_io(obj)
                if(obj.db.aux["out"] != obj.db.main["in"]):
                    up_aux_io(obj)
                if(obj.db.batt["out"] != obj.db.batt["in"]):
                    up_batt_io(obj)
                if(obj.db.main["out"] > 0.0):
                    if(obj.db.main["out"] > obj.db.main["damage"]):
                        up_main_damage(obj)
                if(obj.db.aux["out"] > 0.0):
                    if (obj.db.aux["out"] > obj.db.main["damage"]):
                        up_aux_damage(obj)
                if(obj.db.power["main"] > 0.0 or obj.db.power["aux"] > 0.0):
                    up_fuel(obj)
                if(obj.db.power["batt"] > 0.0 or obj.db.alloc["miscellaneous"] > 0.0):
                    up_reserve(obj)
                if(obj.db.power["version"]  == 1):
                    up_total_power(obj)
                    up_tract_status(obj)
                if(obj.db.beam["in"] != obj.db.beam["out"]):
                    up_beam_io(obj)
                if(obj.db.missile["in"] != obj.db.missile["out"]):
                    up_missile_io(obj)
                if(obj.db.engine["version"]  == 1):
                    up_warp_max(obj)
                    up_impulse_max(obj)
                    up_turn_rate(obj)
                    obj.db.engine["version"] = 0
                if(obj.db.status["autopilot"]  != 0):
                    up_autopilot(obj)
                if(obj.db.move["in"] != obj.db.move["out"]):
                    up_speed_io(obj)
                    up_velocity(obj)
                    up_turn_rate(obj)
                if(obj.db.move["out"] != 0.0):
                    up_warp_damage(obj)
                    up_impulse_damage(obj)
                if(obj.db.course["yaw_in"] != obj.db.course["yaw_out"]):
                    up_yaw_io(obj)
                if(obj.db.course["pitch_in"] != obj.db.course["pitch_out"]):
                    up_pitch_io(obj)
                if(obj.db.course["roll_in"] != obj.db.course["roll_out"]):
                    up_roll_io(obj)
                if(obj.db.course["version"] == 1):
                    up_vectors(obj)
                if(obj.db.move["v"] != 0.0):
                    up_position(obj)
                    up_cochranes(obj)
                    up_empire(obj)
                    up_quadrant(obj)
                    up_visibility(obj)
                if(obj.db.cloak["version"] == 1):
                    up_cloak_status(obj)
                if(obj.db.sensor["version"] == 1):
                    up_resolution(obj)
                    up_signature(obj)
                up_sensor_list(obj)
                if(obj.db.structure["repair"] != obj.db.structure["max_repair"]):
                    up_repair(obj)
    timer = time.time() - timer
    if (timer > constants.tickers[0]):
       print("WARN: Ticker delay too long: {:f} seconds".format(timer))
    else:
        tickers = constants.tickers
        for i in range(0,len(tickers)):
            if (timer > tickers[i]):
                if(TICKER_HANDLER.all(tickers[i-1]) is None):
                    print("WARN: Ticker delay too long: {:.3f}, setting new timer to {:d} seconds".format(timer,tickers[i-1]))
                    add_ticker(tickers[i-1])
                    return count
                else:
                    return count
        add_ticker(1)
    return count

def stop_tickers():
    for i in constants.tickers:
        ticker = TICKER_HANDLER.all(i)
        if(ticker is None):
            continue
        else:
            try:
                TICKER_HANDLER.remove(interval=i,callback=do_space_db_iterate,idstring="db_iterate")
            except KeyError:
                continue

def add_ticker(value):
    ticker = TICKER_HANDLER.all(value)
    if (ticker is None):
        stop_tickers()
        TICKER_HANDLER.add(value,do_space_db_iterate,"db_iterate")