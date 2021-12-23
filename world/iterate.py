"""
Iterates the world and it's settings
"""

import time
from world import constants, alerts, utils, balance, damage, unparse
from world import set as setter
from evennia.utils.search import search_tag, search_object
from evennia import gametime
from evennia.scripts.tickerhandler import TICKER_HANDLER
import math
import random
import sys


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
    main = dict(self.db.main)
    dt = self.db.move["dt"]
    if main["gw"] != 0.0:
        if (main["out"] > main["in"]):
            main["out"] -= dt / 30.0
            if (main["out"] <= main["in"]):
                main["out"] = main["in"]
                self.db.main = main
                alerts.main_balance(self)
        elif(main["out"] < main["in"]):
            main["out"] += dt / 60.0
            if (main["out"] >= main["in"]):
                main["out"] = main["in"]
                self.db.main = main
                alerts.main_balance(self)
    self.db.power["main"] = main["gw"] * main["out"]
    self.db.power["version"] = 1
    self.db.main = main


def up_aux_io(self):
    aux = dict(self.db.aux)
    dt = self.db.move["dt"]
    if aux["gw"] != 0.0:
        if (aux["out"] > aux["in"]):
            aux["out"] -= dt / 5.0
            if (aux["out"] <= aux["in"]):
                aux["out"] = aux["in"]
                self.db.aux = aux
                alerts.aux_balance(self)
        elif(aux["out"] < aux["in"]):
            aux["out"] += dt / 10.0
            if (aux["out"] >= aux["in"]):
                aux["out"] = aux["in"]
                self.db.aux = aux
                alerts.aux_balance(self)
    self.db.power["aux"] = aux["gw"] * aux["out"]
    self.db.power["version"] = 1
    self.db.aux = aux


def up_batt_io(self):
    batt = dict(self.db.batt)
    batt["out"] = batt["in"]
    self.db.batt = batt
    alerts.batt_balance(self)
    self.db.power["batt"] = batt["gw"] * batt["out"]
    self.db.power["version"] = 1


def up_main_damage(self):
    main = dict(self.db.main)
    if (main["exist"] == 1):
        dmg = (main["out"] - main["damage"]) * \
            self.db.move["dt"] / self.db.tech["main_max"] / 1000.0
        if (main["damage"] > 0.0 and (main["damage"] - dmg) <= 0.0):
            alerts.main_overload(self)
        main["damage"] -= dmg
        if (main["damage"] <= -1.0):
            main["damage"] = -1.0
            alerts.do_all_console_notify(
                self, alerts.ansi_warn("Impulse Drive core breach."))
            self.db.main = main
            damage.damage_structure(
                self, self.db.power["main"] * (random.randint(0, 99)+1.0))
            self.db.main["in"] = 0.0
            self.db.main["out"] = 0.0
            self.db.power["main"] = 0.0
            self.db.power["version"] = 1
        else:
            self.db.main = main


def up_aux_damage(self):
    aux = dict(self.db.aux)
    if (aux["exist"] == 1):
        dmg = (aux["out"] - aux["damage"]) * self.db.move["dt"] / \
            self.db.tech["aux_max"] / 1000.0
        if (aux["damage"] > 0.0 and (aux["damage"] - dmg) <= 0.0):
            alerts.aux_overload(self)
        aux["damage"] -= dmg
        if (aux["damage"] <= -1.0):
            aux["damage"] = -1.0
            alerts.do_all_console_notify(
                self, alerts.ansi_warn("fusion reactor core breach."))
            self.db.aux = aux
            damage.damage_structure(
                self, self.db.power["aux"] * (random.randint(0, 99)+1.0))
            self.db.aux["in"] = 0.0
            self.db.aux["out"] = 0.0
            self.db.power["aux"] = 0.0
            self.db.power["version"] = 1
        else:
            self.db.aux = aux


def up_fuel(self):
    main = dict(self.db.main)
    aux = dict(self.db.aux)
    fuel = dict(self.db.fuel)
    power = dict(self.db.power)
    mloss = main["out"] * main["out"] * main["gw"] * \
        100.0 / self.db.tech["fuel"] * self.db.move["dt"]
    aloss = aux["out"] * aux["out"] * aux["gw"] * \
        100.0 / self.db.tech["fuel"] * self.db.move["dt"]

    fuel["antimatter"] -= mloss
    fuel["deuterium"] -= mloss + aloss
    if (fuel["antimatter"] < 0.0):
        if(main["out"] > 0.0):
            alerts.anti_runout(self)
        fuel["antimatter"] = 0.0
        main["in"] = 0.0
        main["out"] = 0.0
        power["main"] = 0.0
        power["version"] = 1

    if (fuel["deuterium"] < 0.0):
        if (aux["out"] > 0.0 or main["out"] > 0.0):
            alerts.deut_runout(self)
        fuel["deuterium"] = 0.0
        main["in"] = 0.0
        main["out"] = 0.0
        power["main"] = 0.0
        aux["in"] = 0.0
        aux["out"] = 0.0
        power["aux"] = 0.0
        power["version"] = 1
    self.db.main = main
    self.db.aux = aux
    self.db.fuel = fuel
    self.db.power = power


def up_reserve(self):
    fuel = dict(self.db.fuel)
    batt = dict(self.db.batt)
    power = dict(self.db.power)
    fuel["reserves"] += (((power["main"] + power["aux"] + power["batt"]) *
                         self.db.alloc["miscellaneous"]) - power["batt"]) * self.db.move["dt"]
    if (fuel["reserves"] < 0.0):
        fuel["reserves"] = 0.0
        batt["in"] = 0.0
        batt["out"] = 0.0
        power["batt"] = 0.0
        alerts.batt_runout(self)
    elif (fuel["reserves"] > batt["gw"] * 3600.0):
        fuel["reserves"] = batt["gw"] * 3600.0
    self.db.fuel = fuel
    self.db.batt = batt
    self.db.power = power


def up_total_power(self):
    power = dict(self.db.power)
    power["total"] = power["main"] + power["aux"] + power["batt"]
    power["version"] = 0
    self.db.power = power
    self.db.engine["version"] = 1
    self.db.sensor["version"] = 1
    self.db.cloak["version"] = 1
    up_turn_rate(self)


def up_warp_damage(self):
    move = dict(self.db.move)
    engine = dict(self.db.engine)
    if (engine["warp_exist"] == 1):
        if(math.fabs(move["out"]) >= 1.0):
            if (math.fabs(move["out"]) > engine["warp_cruise"]):
                self.db.engine["warp_damage"] = engine["warp_damage"] - (math.fabs(
                    move["out"]) - engine["warp_cruise"]) * move["dt"] / self.db.tech["main_max"] / 10000.0
                if (self.db.engine["warp_damage"] < 0.0):
                    move["in"] = 0.0
                    move["out"] = 0.0
                    move["v"] = 0.0
                    self.db.move = move
                    alerts.warp_overload(self)
                    alerts.speed_stop(self)
                    alerts.ship_exit_warp(self)
                up_warp_max(self)


def up_impulse_damage(self):
    move = dict(self.db.move)
    engine = dict(self.db.engine)
    if(engine["impulse_exist"] == 1):
        if(math.fabs(move["out"]) < 1.0):
            if(math.fabs(move["out"]) > engine["impulse_cruise"] and math.fabs(move["in"]) < 1.0):
                self.db.engine["impulse_damage"] = engine["impulse_damage"] - (math.fabs(
                    move["out"])-engine["impulse_cruise"]) * move["dt"] / self.db.tech["aux_max"] / 10000.0
                if (self.db.engine["impulse_damage"] < 0.0):
                    move["in"] = 0.0
                    move["out"] = 0.0
                    move["v"] = 0.0
                    self.db.move = move
                    alerts.impulse_overload(self)
                    alerts.speed_stop(self)
                up_impulse_max(self)


def up_warp_max(self):
    move = dict(self.db.move)
    engine = dict(self.db.engine)
    engine["warp_max"] = utils.sdb2max_warp(self)
    engine["warp_cruise"] = utils.sdb2cruise_warp(self)

    if((move["in"] >= 1.0) and (move["in"] > engine["warp_max"])):
        move["in"] = engine["warp_max"]
    elif((move["in"] <= -1.0) and (move["in"] < (engine["warp_max"] / 2.0))):
        move["in"] = -engine["warp_max"] / 2.0
    self.db.engine = engine
    self.db.move = move


def up_impulse_max(self):
    move = dict(self.db.move)
    engine = dict(self.db.engine)
    engine["impulse_max"] = utils.sdb2max_impulse(self)
    engine["impulse_cruise"] = utils.sdb2cruise_impulse(self)

    if((move["in"] >= 0.0) and (move["in"] < 1.0) and (move["in"] > engine["impulse_max"])):
        move["in"] = engine["impulse_max"]
    elif((move["in"] > -1.0) and (move["in"] < 0.0) and (move["in"] < (-engine["impulse_max"] / 2.0))):
        move["in"] = -engine["impulse_max"] / 2.0
    self.db.engine = engine
    self.db.move = move


def up_tract_status(self):
    if(self.db.status["tractoring"] == 1):
        obj_x = utils.name2sdb(self.db.status["tractoring"])
        p = self.db.tract["damage"] * self.db.power["total"] * \
            self.db.alloc["tractors"] / (utils.sdb2range(self, obj_x) + 1.0)
        if((obj_x.db.tract["active"] and p < obj_x.db.tract["damage"] * obj_x.db.power["total"] * obj_x.db.alloc["tractors"]) or p < 1.0):
            alerts.tract_lost(self)
            self.db.tract["lock"] = 0
            self.db.status["tractoring"] = 0
            obj_x.db.status["tractored"] = 0
            self.db.power["version"] = 1
            obj_x.db.power["version"] = 1
        elif(self.db.status["tractored"] == 1 and self.db.tract["active"] == 1):
            obj_x = utils.name2sdb(self.db.status["tractored"])
            p = self.db.tract["damage"] * self.db.power["total"] * \
                self.db.alloc["tractors"] / \
                (utils.sdb2range(obj_x, self) + 1.0)
            if (p < (self.db.tract["damage"] * self.db.power["total"] * self.db.alloc["tractors"])):
                alerts.tract_lost(self)
                obj_x.db.tract["lock"] = 0
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
    beam = dict(self.db.beam)
    if(beam["out"] > beam["in"]):
        beam["out"] = beam["in"]
        alerts.beam_balance(self)
    elif(self.db.alloc["beams"] * self.db.power["total"] > 0.0):
        beam["out"] += self.db.alloc["beams"] * \
            self.db.power["total"] * self.db.move["dt"]
        if (beam["out"] >= beam["in"]):
            beam["out"] = beam["in"]
            alerts.beam_charged(self)
    if(beam["out"] < 0.0):
        beam["out"] = 0.0
    self.db.sensor["version"] = 1
    self.db.beam = beam


def up_empire(self):
    space_obj = search_tag(constants.EMPIRE_ATTR_NAME, category="space_object")
    best_range = sys.maxsize
    best_empire = ""
    for obj in space_obj:
        if(obj.db.status["active"] == 1):
            if (obj.db.space != 0 and self.db.space != obj.db.space):
                continue
            self_coords = dict(self.db.coords)
            obj_coords = dict(obj.db.coords)
            dx = (obj_coords["x"] - self_coords["x"]) / constants.PARSEC
            dy = (obj_coords["y"] - self_coords["y"]) / constants.PARSEC
            dz = (obj_coords["z"] - self_coords["z"]) / constants.PARSEC
            range = (dx * dx + dy * dy + dz * dz)
            radius = obj.db.radius
            inside_range = math.fabs(range - (radius * radius))

            if (range <= (radius * radius)):  # object in radius
                # closer to center than previous best
                if (best_empire == "" or inside_range < best_range):
                    best_range = range
                    best_empire = obj.name
    empire = self.db.move["empire"]
    if (empire != best_empire):
        if (empire != ""):
            same = 0
            if (empire == best_empire):
                same = 1
            if (same == 0):
                alerts.exit_empire(self)
                if(random.randint(1, 100) < (self.db.sensor["lrs_signature"] * self.db.sensor["visibility"] * 100.0)):
                    alerts.border_cross(self, 0)
        if (empire == ""):
            self.db.move["empire"] = best_empire
            alerts.enter_empire(self)
            if(random.randint(1, 100) < (self.db.sensor["lrs_signature"] * self.db.sensor["visibility"] * 100.0)):
                alerts.border_cross(self, 1)
        self.db.move["empire"] = best_empire


def up_missile_io(self):
    missile = dict(self.db.missile)
    if (missile["out"] > missile["in"]):
        missile["out"] = missile["in"]
        alerts.missile_balance(self)
    elif(self.db.alloc["missiles"] * self.db.power["total"] > 0.0):
        missile["out"] += self.db.alloc["missiles"] * \
            self.db.power["total"] * self.db.move["dt"]
        if (missile["out"] >= missile["in"]):
            missile["out"] = missile["in"]
            alerts.missile_charged(self)
    if(missile["out"] < 0.0):
        missile["out"] = 0.0
    self.db.sensor["version"] = 1
    self.db.missile = missile


def up_autopilot(self):
    coords = dict(self.db.coords)
    r = utils.xyz2range(coords["x"], coords["y"], coords["z"],
                        coords["xd"], coords["yd"], coords["zd"])
    speed = 99
    autopilot = self.db.status["autopilot"]

    if(r < 1.0):
        speed = 0
        autopilot = 0
        alerts.console_message(self, ["helm"], alerts.ansi_notify(
            "Autopilot destination reached"))
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
            speed = math.pow(r / int(r), 0.3)
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
        self.db.course["yaw_in"] = utils.xy2bearing(
            coords["xd"] - coords["x"], coords["yd"] - coords["y"])
        self.db.course["pitch_in"] = utils.xyz2elevation(
            coords["xd"] - coords["x"], coords["yd"] - coords["y"], coords["zd"] - coords["z"])
        if(self.db.move["in"] > speed):
            if (speed >= 1.0 and speed > self.db.engine["warp_cruise"]):
                speed = self.db.engine["warp_cruise"]
            if (speed < 1.0 and speed > self.db.engine["impulse_cruise"]):
                speed = self.db.engine["impulse_cruise"]
            self.db.move["in"] = speed


def up_speed_io(self):
    move = dict(self.db.move)
    power = dict(self.db.power)
    engine = dict(self.db.engine)
    alloc = self.db.alloc["movement"]
    structure = dict(self.db.structure)

    if (move["ratio"] <= 0.0):
        return
    if (math.fabs(move["out"]) < 1.0):
        if(math.fabs(move["in"]) >= 1.0):
            a = power["main"] * 0.99 + power["total"] * alloc * 0.01
        else:
            a = power["aux"] * 0.9 + power["total"] * alloc * 0.1
        a *= (1.0 - math.fabs(move["out"])) / move["ratio"] / 50.0
    else:
        a = (power["main"] * 0.99 + power["total"] * alloc * 0.01) / \
            move["ratio"] / math.fabs(move["out"]) / 5.0
    a *= (move["ratio"] + 1.0) / move["ratio"] * move["dt"]

    if (move["out"] < 0.0):
        a /= 2.0
    obj_x = utils.name2sdb(self.db.status["tractoring"])
    if (obj_x == constants.SENSOR_FAIL):
        obj_x = utils.name2sdb(self.db.status["tractored"])
    if (obj_x != constants.SENSOR_FAIL):
        a *= (structure["displacement"] + 0.1) / \
            (obj_x.db.structure["displacement"] +
             structure["displacement"] + 0.1)
    if (a < 0.01):
        a = 0.01

    if((move["in"] >= 1.0) and (move["in"] > engine["warp_max"])):
        move["in"] = engine["warp_max"]
    elif((move["in"] <= -1.0) and (move["in"] < (-engine["warp_max"] / 2.0))):
        move["in"] = -engine["warp_max"] / 2.0
    elif((move["in"] >= 0.0) and (move["in"] < 1.0) and (move["in"] > engine["impulse_max"])):
        move["in"] = engine["impulse_max"]
    elif((move["in"] <= 0.0) and (move["in"] > -1.0) and (move["in"] < (-engine["impulse_max"] / 2.0))):
        move["in"] = - engine["impulse_max"] / 2.0

    if(move["out"] > self.db.move["in"]):
        if (move["out"] >= 1.0):
            if (move["in"] >= 1.0):
                move["out"] = move["in"]
                self.db.move = move
                alerts.speed_warp(self)
            elif(move["in"] > 0.0 and move["in"] < 1.0):
                move["out"] = move["in"]
                self.db.move = move
                alerts.speed_impulse(self)
                alerts.ship_exit_warp(self)
            elif(move["in"] <= 0.0):
                move["out"] = 0.0
                alerts.speed_stop(self)
                alerts.ship_exit_warp(self)

            elif(move["out"] > 0.0 and move["out"] < 1.0):
                if (move["in"] > 0.0):
                    move["out"] = move["in"]
                    self.db.move = move
                    alerts.speed_impulse(self)
                elif(move["in"] <= 0.0):
                    move["out"] = 0.0
                    alerts.speed_stop(self)
            elif(move["out"] <= 0.0):
                if (move["out"] > -1.0):
                    move["out"] -= a
                    if (move["out"] <= move["in"]):
                        move["out"] = move["in"]
                        if (move["out"] > -1.0):
                            self.db.move = move
                            alerts.speed_impulse(self)
                        else:
                            self.db.move = move
                            alerts.speed_warp(self)
                            alerts.ship_enter_warp(self)
                    elif(move["out"] <= -1.0):
                        self.db.move = move
                        alerts.ship_enter_warp(self)
            else:
                move["out"] -= a
                if (move["out"] <= move["in"]):
                    move["out"] = move["in"]
                    self.db.move = move
                    alerts.speed_warp(self)
    elif(move["out"] < move["in"]):
        if (move["out"] <= -1.0):
            if (move["in"] <= -1.0):
                move["out"] = move["in"]
                self.db.move = move
                alerts.speed_warp(self)
            elif(move["in"] < 0.0 and move["in"] > -1.0):
                move["out"] = move["in"]
                self.db.move = move
                alerts.speed_impulse(self)
                alerts.ship_exit_warp(self)
            elif(move["in"] >= 0.0):
                move["out"] = 0.0
                alerts.speed_stop(self)
                alerts.ship_exit_warp(self)
        elif (move["out"] < 0.0 and move["out"] > -1.0):
            if (move["in"] < 0.0):
                move["out"] = move["in"]
                self.db.move = move
                alerts.speed_impulse(self)
            elif(move["in"] >= 0.0):
                move["out"] = 0.0
                alerts.speed_stop(self)
        elif(move["out"] >= 0.0):
            if (move["out"] < 1.0):
                move["out"] += a
                if (move["out"] >= move["in"]):
                    move["out"] = move["in"]
                    if (move["out"] < 1.0):
                        self.db.move = move
                        alerts.speed_impulse(self)
                    else:
                        self.db.move = move
                        alerts.speed_warp(self)
                        alerts.ship_enter_warp(self)
                elif(move["out"] >= 1.0):
                    alerts.ship_enter_warp(self)
            else:
                move["out"] += a
                if (move["out"] >= move["in"]):
                    move["out"] = move["in"]
                    self.db.move = move
                    alerts.speed_warp(self)

    self.db.sensor["version"] = 1
    self.db.move = move


def up_turn_rate(self):
    move = dict(self.db.move)
    power = dict(self.db.power)
    alloc = float(self.db.alloc["movement"])

    a = 0
    if(move["ratio"] <= 0.0):
        return
    if(math.fabs(move["out"]) < 1.0):
        if(math.fabs(move["in"]) >= 1.0):
            a = power["main"] * 0.99 + power["total"] * alloc * 0.01
        else:
            a = power["aux"] * 0.9 + power["total"] * alloc * 0.1
        a *= 3.6 * (1.0 - math.fabs(move["out"])) / move["ratio"]
    else:
        a = 3.6 * (power["main"] * 0.99 + power["total"] *
                   alloc * 0.01) / move["ratio"] / math.fabs(move["out"])

    a *= (move["ratio"] + 1.0) / move["ratio"] * move["dt"]

    if (move["out"] < 0.0):
        a /= 2.0

    obj_x = utils.name2sdb(self.db.status["tractoring"])
    if (obj_x == constants.SENSOR_FAIL):
        obj_x = utils.name2sdb(self.db.status["tractored"])
    if (obj_x != constants.SENSOR_FAIL):
        a *= (self.db.structure["displacement"] + 0.1) / (
            obj_x.db.structure["displacement"] + self.db.structure["displacement"] + 0.1)

    if(a < 1.0):
        a = 1.0

    self.db.course["rate"] = a


def up_cochranes(self):
    coords = dict(self.db.coords)
    self.db.move["cochranes"] = utils.xyz2cochranes(
        coords["x"], coords["y"], coords["z"])


def up_velocity(self):
    move = dict(self.db.move)
    if (self.db.engine["warp_exist"] or self.db.engine["impulse_exist"]):
        if (move["out"] >= 1.0):
            move["v"] = constants.LIGHTSPEED * pow(move["out"], 3.333333)
        elif (move["out"] <= -1.0):
            move["v"] = constants.LIGHTSPEED * - \
                pow(math.fabs(move["out"]), 3.333333)
        else:
            move["v"] = constants.LIGHTSPEED * move["out"]
    self.db.move = move


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
    coords = dict(self.db.coords)
    if (self.db.status["docked"] == 1 or self.db.status["landed"] == 1):
        self.db.sensor["visibility"] = 1.0
    else:
        self.db.sensor["visibility"] = float(
            utils.xyz2vis(coords["x"], coords["y"], coords["z"]))


def up_yaw_io(self):
    course = dict(self.db.course)
    dt = self.db.move["dt"]
    if(course["yaw_out"] < course["yaw_in"]):
        if((course["yaw_in"] - course["yaw_out"]) <= 180.0):
            course["yaw_out"] += course["rate"] * dt
            if (course["yaw_out"] >= course["yaw_in"]):
                course["yaw_out"] = course["yaw_in"]
                self.db.course = course
                alerts.yaw(self)
        else:
            course["yaw_out"] -= course["rate"] * dt
            if (course["yaw_out"] < 0.0):
                course["yaw_out"] += 360.0
                if (course["yaw_out"] <= course["yaw_in"]):
                    course["yaw_out"] = course["yaw_in"]
                    self.db.course = course
                    alerts.yaw(self)

    else:
        if((course["yaw_out"] - course["yaw_in"]) <= 180.0):
            course["yaw_out"] -= course["rate"] * dt
            if (course["yaw_out"] <= course["yaw_in"]):
                course["yaw_out"] = course["yaw_in"]
                self.db.course = course
                alerts.yaw(self)
        else:
            course["yaw_out"] += course["rate"] * dt
            if (course["yaw_out"] >= 0.0):
                course["yaw_out"] -= 360.0
                if (course["yaw_out"] >= course["yaw_in"]):
                    course["yaw_out"] = course["yaw_in"]
                    self.db.course = course
                    alerts.yaw(self)

    course["version"] = 1
    self.db.course = course


def up_pitch_io(self):
    course = dict(self.db.course)
    dt = self.db.move["dt"]
    if(course["pitch_out"] < course["pitch_in"]):
        if((course["pitch_in"] - course["pitch_out"]) <= 180.0):
            course["pitch_out"] += course["rate"] * dt
            if (course["pitch_out"] >= course["pitch_in"]):
                course["pitch_out"] = course["pitch_in"]
                self.db.course = course
                alerts.pitch(self)
        else:
            course["pitch_out"] -= course["rate"] * dt
            if (course["pitch_out"] < 0.0):
                course["pitch_out"] += 360.0
                if (course["pitch_out"] <= course["pitch_in"]):
                    course["pitch_out"] = course["pitch_in"]
                    self.db.course = course
                    alerts.pitch(self)

    else:
        if((course["pitch_out"] - course["pitch_in"]) <= 180.0):
            course["pitch_out"] -= course["rate"] * dt
            if (course["pitch_out"] <= course["pitch_in"]):
                course["pitch_out"] = course["pitch_in"]
                self.db.course = course
                alerts.pitch(self)
        else:
            course["pitch_out"] += course["rate"] * dt
            if (course["pitch_out"] >= 0.0):
                course["pitch_out"] -= 360.0
                if (course["pitch_out"] >= course["pitch_in"]):
                    course["pitch_out"] = course["pitch_in"]
                    self.db.course = course
                    alerts.pitch(self)

    course["version"] = 1
    self.db.course = course


def up_roll_io(self):
    course = dict(self.db.course)
    dt = self.db.move["dt"]
    if(course["roll_out"] < course["roll_in"]):
        if((course["roll_in"] - course["roll_out"]) <= 180.0):
            course["roll_out"] += course["rate"] * dt
            if (course["roll_out"] >= course["roll_in"]):
                course["roll_out"] = course["roll_in"]
                self.db.course = course
                alerts.roll(self)
        else:
            course["roll_out"] -= course["rate"] * dt
            if (course["roll_out"] < 0.0):
                course["roll_out"] += 360.0
                if (course["roll_out"] <= course["roll_in"]):
                    course["roll_out"] = course["roll_in"]
                    self.db.course = course
                    alerts.roll(self)

    else:
        if((course["roll_out"] - course["roll_in"]) <= 180.0):
            course["roll_out"] -= course["rate"] * dt
            if (course["roll_out"] <= course["roll_in"]):
                course["roll_out"] = course["roll_in"]
                self.db.course = course
                alerts.roll(self)
        else:
            course["roll_out"] += course["rate"] * dt
            if (course["roll_out"] >= 0.0):
                course["roll_out"] -= 360.0
                if (course["roll_out"] >= course["roll_in"]):
                    course["roll_out"] = course["roll_in"]
                    self.db.course = course
                    alerts.roll(self)

    course["version"] = 1
    self.db.course = course


def up_vectors(self):
    d2r = math.pi / 180.0
    course = dict(self.db.course)
    sy = math.sin(course["yaw_out"] * d2r)
    cy = math.cos(course["yaw_out"] * d2r)
    sp = math.sin(course["pitch_out"] * d2r)
    cp = math.cos(course["pitch_out"] * d2r)
    sr = math.sin(course["roll_out"] * d2r)
    cr = math.cos(course["roll_out"] * d2r)

    coursed0 = [0, 0, 0]
    coursed1 = [0, 0, 0]
    coursed2 = [0, 0, 0]

    coursed0[0] = cy * cp
    coursed0[1] = sy * cp
    coursed0[2] = sp
    coursed1[0] = -(sy * cr) + (cy * sp * sr)
    coursed1[1] = (cy * cr) + (sy * sp * sr)
    coursed1[2] = -(cp * sr)
    coursed2[0] = -(sy * sr) - (cy * sp * cr)
    coursed2[1] = (cy * sr) - (sy * sp * cr)
    coursed2[2] = (cp * cr)
    self.db.course["d"] = [coursed0, coursed1, coursed2]
    self.db.course["version"] = 0


def up_position(self):
    move = dict(self.db.move)
    status = dict(self.db.status)
    dv = move["v"] * move["dt"]
    if (math.fabs(move["out"]) >= 1.0):
        dv *= move["cochranes"]
    coursed0 = list(self.db.course["d"][0])
    obj_x = utils.name2sdb(status["tractoring"])
    if (obj_x == constants.SENSOR_FAIL):
        obj_x = utils.name2sdb(status["tractored"])
    if (obj_x != constants.SENSOR_FAIL):
        coords = dict(obj_x.db.coords)
        coords["x"] += dv * coursed0[0]
        coords["y"] += dv * coursed0[1]
        coords["z"] += dv * coursed0[2]
        obj_x.db.coords = coords
    coords = dict(self.db.coords)
    coords["x"] += dv * coursed0[0]
    coords["y"] += dv * coursed0[1]
    coords["z"] += dv * coursed0[2]
    self.db.coords = coords


def up_wormhole(self, obj, obj_x):
    alerts.do_ship_notify(
        obj, "The {:s} shudders and rocks about violently for a few moments.".format(obj.name))
    alerts.do_space_notify_two(
        obj, obj_x, ["helm", "tactical", "science"], "enters")
    if(obj.db.cloak["active"] == 1):
        alerts.cloak_voided(obj)
        alerts.ship_cloak_offline(obj)
        obj.db.cloak["active"] = 0
        obj.db.sensor["version"] = 1
        obj.db.engine["version"] = 1

    # clear contacts and reset sensors
    for i in range(obj.db.sensor["contacts"]):
        tmp_c = search_object(obj.db.slist[i]["key"])[0]
        alerts.console_message(obj, ["helm", "science", "tactical"], "{:s} contact lost: {:s}".format(
            unparse.unparse_type(tmp_c), unparse.unparse_identity(obj, tmp_c)))
    obj.db.sensor["contacts"] = 0
    up_sensor_message(
        obj, 0, [""] * constants.MAX_SENSOR_CONTACTS, [0] * constants.MAX_SENSOR_CONTACTS)
    obj_link = search_object(obj_x.db.status["link"])
    if (len(obj_link) == 0):
        alerts.notify(alerts.ansi_red(
            "{:s} loops back on itself.".format(obj_x.name)))
        alerts.write_spacelog(self, obj_x, "BUG: Bad wormhole link")
        obj_link = obj_x
    else:
        obj_link = obj_link[0]
    obj.db.space = obj_link.db.space
    coords = dict(obj.db.coords)
    link_coords = dict(obj_link.db.coords)
    coords["x"] = link_coords["x"]
    coords["y"] = link_coords["y"]
    coords["z"] = link_coords["z"]
    obj.db.coords = coords
    obj.db.status["autopilot"] = 0
    alerts.do_space_notify_one(
        obj_link, ["helm", "tactical", "science"], "expells an unknown contact")
    up_cochranes(obj)
    up_empire(obj)
    up_quadrant(obj)
    up_resolution(obj)
    up_signature(obj)
    up_visibility(obj)
    return 1


def up_resolution(self):
    sensor = dict(self.db.sensor)
    tech_sensors = self.db.tech["sensors"]
    if(sensor["lrs_active"] == 1):
        sensor["lrs_resolution"] = tech_sensors * sensor["lrs_damage"]
        if (sensor["ew_active"] == 1):
            sensor["lrs_resolution"] *= utils.sdb2eccm_lrs(self)
        if (self.db.cloak["active"] == 1):
            sensor["lrs_resolution"] /= 10.0
    else:
        sensor["lrs_resolution"] = 0.0
    if (sensor["srs_active"] == 1):
        sensor["srs_resolution"] = tech_sensors * sensor["srs_damage"]
        if (sensor["ew_active"] == 1):
            sensor["srs_resolution"] *= utils.sdb2eccm_srs(self)
        if(self.db.cloak["active"] == 1):
            sensor["srs_resolution"] /= 10.0
    else:
        sensor["srs_resolution"] = 0.0
    self.db.sensor = sensor
    return 1


def up_signature(self):
    sensor = dict(self.db.sensor)
    cloak = dict(self.db.cloak)
    status = dict(self.db.status)
    tech = dict(self.db.tech)
    power = dict(self.db.power)
    base = math.pow(self.db.structure["displacement"],
                    0.333333) / tech["stealth"] / 100.0
    sig = base

    if(cloak["active"] == 1):
        cloak["level"] = 0.001 / power["total"] / \
            self.db.alloc["cloak"] / tech["cloak"] * cloak["cost"]
        if (status["tractored"] == 1):
            cloak["level"] *= 100.0
        if (status["tractoring"] == 1):
            cloak["level"] *= 100.0
        if (self.db.beam["out"] > 1.0):
            cloak["level"] *= self.db.beam["out"]
        if (self.db.missile["out"] > 1.0):
            cloak["level"] *= self.db.missile["out"]
        if (sensor["visibility"] < 1.0):
            cloak["level"] *= (1.0 - sensor["visibility"]) * 10000.0
        if (cloak["level"] > 1.0):
            cloak["level"] = 1.0
    else:
        cloak["level"] = 1.0

    sensor["lrs_signature"] = sig
    sensor["srs_signature"] = sig * 10.0
    sensor["lrs_signature"] *= self.db.move["out"] * self.db.move["out"] + 1.0
    sensor["srs_signature"] *= 1.0 + power["main"] + \
        (power["aux"] / 10.0) + (power["batt"] / 100.0)
    if (sensor["ew_active"] == 1):
        sensor["lrs_signature"] /= utils.sdb2ecm_lrs(self)
        sensor["srs_signature"] /= utils.sdb2ecm_srs(self)

    sensor["version"] = 0
    self.db.sensor = sensor
    self.db.cloak = cloak
    return 1


def up_sensor_message(self, contacts, temp_sdb, temp_lev):
    sensor = dict(self.db.sensor)
    temp_num = [0] * constants.MAX_SENSOR_CONTACTS
    for i in range(contacts):
        gain = 0
        for j in range(contacts):
            if (temp_sdb[i] == ""):
                gain = 1
                break
            if (temp_sdb[i] == self.db.slist[j]["key"]):
                gain = 1
                temp_num[i] = self.db.slist[j]["num"]
                break
        if (gain == 0):
            sensor["counter"] += 1
            if (sensor["counter"] > 999):
                sensor["counter"] = 1
            temp_num[i] = sensor["counter"]
            obj_x = utils.name2sdb(temp_sdb[i])
            alerts.console_message(self, ["helm", "science", "tactical"], alerts.ansi_warn(
                "New sensor contact ({:0d}): {:s}".format(temp_num[i],unparse.unparse_type(obj_x))))
    for i in range(contacts):
        lose = 0
        for j in range(contacts):
            if(temp_sdb[j] == ""):
                lose = 1
                break
            if(temp_sdb[j] == self.db.slist[i]["key"]):
                lose = 1
                break
        if (lose == 0 and self.db.slist[i]["key"] != "" and self.db.slist[i]["key"] != 0):
            obj_x = utils.name2sdb(self.db.slist[i]["key"])
            alerts.console_message(self, ["helm", "science", "tactical"], "{:s} contact lost: {:s}".format(unparse.unparse_type(obj_x), unparse.unparse_identity(self, obj_x)))
            if (self.db.trans["s_lock"] == self.db.slist[i]["key"]):
                alerts.console_message(self, ["operation", "transporter"], alerts.ansi_warn("Transporters lost lock on {:s}".format(unparse.unparse_identity(self, obj_x))))
                self.db.trans.s_lock = 0
            if (self.db.trans["d_lock"] == self.db.slist[i]["key"]):
                alerts.console_message(self, ["operation", "transporter"], alerts.ansi_warn("Transporters lost lock on {:s}".format(unparse.unparse_identity(self, obj_x))))
                self.db.trans.d_lock = 0
            if (self.db.tract["lock"] == self.db.slist[i]["key"]):
                alerts.console_message(self, ["helm", "operation"], alerts.ansi_warn("Tractor beam lost lock on {:s}".format(unparse.unparse_identity(self, obj_x))))
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
                alerts.console_message(self, ["tactical"], alerts.ansi_warn("Phaser Array lock lost on {:s}".format(unparse.unparse_identity(self, obj_x))))
            flag = 0
            for j in range(self.db.missile["tubes"]):
                if (self.db.mlist[j]["lock"] == self.db.slist[i]["key"]):
                    flag = 1
                    self.db.mlist[j]["lock"] = 0
            if (flag > 0):
                alerts.console_message(self, ["tactical"], alerts.ansi_warn("Missile lock lost on {:s}".format(unparse.unparse_identity(self, obj_x))))

    sensor["contacts"] = contacts
    if (contacts == 0):
        sensor["counter"] = 0
    else:
        for i in range(contacts):
            self.db.slist[i]["key"] = temp_sdb[i]
            self.db.slist[i]["num"] = temp_num[i]
            self.db.slist[i]["lev"] = temp_lev[i]
    self.db.sensor = sensor


def up_sensor_list(self):
    contacts = 0
    limit = constants.PARSEC * 100.0
    objects = search_tag(category="space_object")
    temp_sdb = [""] * constants.MAX_SENSOR_CONTACTS
    temp_lev = [0] * constants.MAX_SENSOR_CONTACTS
    coords = dict(self.db.coords)

    for obj in objects:
        if ((self.location or 0) == (obj.location or 0) and self.db.space == obj.db.space and obj.db.structure["type"] > 0 and self.name != obj.name):
            x = math.fabs(coords["x"] - obj.db.coords["x"])
            if (x > limit):
                continue
            y = math.fabs(coords["y"] - obj.db.coords["y"])
            if (y > limit):
                continue
            z = math.fabs(coords["z"] - obj.db.coords["z"])
            if (z > limit):
                continue
            level = (self.db.sensor["srs_resolution"] + 0.01) * obj.db.sensor["srs_signature"] / (0.1 + (x * x + y * y + z * z) / 10101.010101)
            x /= constants.PARSEC
            y /= constants.PARSEC
            z /= constants.PARSEC
            level += self.db.sensor["lrs_resolution"] * obj.db.sensor["lrs_signature"] / (1.0 + (x * x + y * y + z * z) * 99.0)
            level *= self.db.sensor["visibility"] * obj.db.sensor["visibility"]
            if (level < 0.01):
                continue
            if(obj.db.cloak["active"] == 1):
                if (self.db.tech["sensors"] < 2.0):
                    level *= obj.db.cloak["level"]
            if (level < 0.01):
                continue
            temp_sdb.insert(contacts, obj.dbref)
            temp_lev.insert(contacts, level)
            contacts = contacts + 1
            if (contacts == constants.MAX_SENSOR_CONTACTS):
                break

    if (contacts != self.db.sensor["contacts"]):
        up_sensor_message(self, contacts, temp_sdb, temp_lev)
    else:
        for i in range(self.db.sensor["contacts"]):
            self.db.slist[i]["key"] = temp_sdb[i]
            self.db.slist[i]["lev"] = temp_lev[i]


def up_repair(self):
    self.db.structure["repair"] += self.db.move["dt"] * self.db.structure["max_repair"] / \
        1000.0 * \
        (1.0 +
         math.sqrt(self.db.alloc["miscellaneous"] * self.db.power["total"]))
    if (self.db.structure["repair"] >= self.db.structure["max_repair"]):
        self.db.structure["repair"] = self.db.structure["max_repair"]
        alerts.max_repair(self)


def do_space_db_iterate(custom = None):
    if (custom is None):
        objects = search_tag(category="space_object")
    else:
        objects = custom
    count = 0
    timer = time.time()
    for obj in objects:
        if (obj.db.status["active"] == 1 and obj.db.structure["type"] > 0):
            count = count + 1
            now = gametime.gametime(absolute=True)
            dt = now - obj.db.move["time"]
            obj.db.move["dt"] = dt
            obj.db.move["time"] = now
            if (dt > 0.0):
                if (obj.db.structure["type"] == 1):
                    if(now - obj.db.status["time"] > 3600):
                        if(obj.db.main["in"] > 0.0):
                            setter.do_set_main_reactor(obj, 0.0, obj)
                            obj.db.main["in"] = 0.0
                        if(obj.db.aux["in"] > 0.0):
                            setter.do_set_aux_reactor(obj, 0.0, obj)
                            obj.db.aux["in"] = 0.0
                        if(obj.db.batt["in"] > 0.0):
                            setter.do_set_battery(obj, 0.0, obj)
                        if(obj.db.power["total"] == 0.0):
                            setter.do_set_inactive(obj, obj)
                if(dt > 60.0):
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
                if(obj.db.power["version"] == 1):
                    up_total_power(obj)
                    up_tract_status(obj)
                if(obj.db.beam["in"] != obj.db.beam["out"]):
                    up_beam_io(obj)
                if(obj.db.missile["in"] != obj.db.missile["out"]):
                    up_missile_io(obj)
                if(obj.db.engine["version"] == 1):
                    up_warp_max(obj)
                    up_impulse_max(obj)
                    up_turn_rate(obj)
                    obj.db.engine["version"] = 0
                if(obj.db.status["autopilot"] != 0):
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
    if (custom is not None):
        return count
    if (timer > constants.tickers[0]):
        print("WARN: Ticker delay too long: {:f} seconds".format(timer))
    else:
        tickers = constants.tickers
        for i in range(0, len(tickers)):
            if (timer > tickers[i]):
                if(TICKER_HANDLER.all(tickers[i-1]) is None):
                    print("WARN: Ticker delay too long: {:.3f}, setting new timer to {:d} seconds".format(
                        timer, tickers[i-1]))
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
                TICKER_HANDLER.remove(
                    interval=i, callback=do_space_db_iterate, idstring="db_iterate")
            except KeyError:
                continue


def add_ticker(value):
    ticker = TICKER_HANDLER.all(value)
    if (ticker is None):
        stop_tickers()
        TICKER_HANDLER.add(value, do_space_db_iterate, "db_iterate")
