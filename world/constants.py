"""
List all constants here
"""
COCHRANE = 12927.238000
PARSEC = 3085659622.014257
LIGHTYEAR = 946057498.117920
LIGHTSPEED = 29.979246

SENSOR_FAIL = -100
VACANCY_FAIL = -101
BAD_SDB_FAIL = -102
ARC_FAIL = -103

MAX_SHIELD_NAME = 6
MAX_EMPIRE_NAME = 12
MAX_SYSTEM_NAME = 19
MAX_QUADRANT_NAME = 4
MAX_TYPE_NAME = 12
MAX_BEAM_NAME = 22
MAX_MISSILE_NAME = 18

MIN_SPACE_OBJECTS = 1
MAX_SPACE_OBJECTS = 1500

MIN_CONSOLE_COUNT = 1
MAX_CONSOLE_COUNT = 20

MAX_DOCKING_DISTANCE = 1.0
MAX_LANDING_DISTANCE = 1.0
MAX_WORMHOLE_DISTANCE = 10.0
MAX_TRANSPORTER_DISTANCE = 5.0
MAX_NOTIFICATION_DISTANCE = 100.0 * PARSEC

MIN_COMMS_OBJECTS = 1
MAX_COMMS_OBJECTS = 2000
MIN_COMMS_FREQUENCY = 1.0
MAX_COMMS_FREQUENCY = 1000.0
EXECUTE_ATTR_NAME = "EXECUTE"
ENCRYPTION_ATTR_NAME = "ENCRYPTION"

CONSOLE_SECURITY = 7950
CONSOLE_HELM = 2087
CONSOLE_ENGINEERING = 2088
CONSOLE_OPERATION = 12337
CONSOLE_SCIENCE = 2954
CONSOLE_DAMAGE = 2086
CONSOLE_COMMUNICATION = 2085
CONSOLE_TACTICAL = 2084
CONSOLE_TRANSPORTER = 2083
CONSOLE_MONITOR = 19362
CONSOLE_FIGHTER = 23308
CONSOLE_LIST = ["security","helm","engineering","operation","science","damage","communication","tactical","transporter","monitor","fighter"]
SHIELD_NAME = ["Forward shield","Starboard shield","Aft shield","Port shield","Dorsal shield","Ventral shield"]

NO_SDB_ATTR = 2000
NO_LOCATION_ATTR = 2002
NO_SPACE_ATTR = 2003

NO_ALLOCATE_ATTR = 1002
NO_BEAM_ATTR = 1003
NO_BEAM_ACTIVE_ATTR = 1004
NO_BEAM_NAME_ATTR = 1005
NO_BEAM_DAMAGE_ATTR = 1006
NO_BEAM_BONUS_ATTR = 1007
NO_BEAM_COST_ATTR = 1008
NO_BEAM_RANGE_ATTR = 1009
NO_BEAM_ARCS_ATTR = 1010
NO_BEAM_LOCK_ATTR = 1011
NO_BEAM_LOAD_ATTR = 1012
NO_MISSILE_ATTR = 1013
NO_MISSILE_ACTIVE_ATTR = 1014
NO_MISSILE_NAME_ATTR = 1015
NO_MISSILE_DAMAGE_ATTR = 1016
NO_MISSILE_WARHEAD_ATTR = 1017
NO_MISSILE_COST_ATTR = 1018
NO_MISSILE_RANGE_ATTR = 1019
NO_MISSILE_ARCS_ATTR = 1020
NO_MISSILE_LOCK_ATTR = 1021
NO_MISSILE_LOAD_ATTR = 1022
NO_ENGINE_ATTR = 1023
NO_STRUCTURE_ATTR = 1024
NO_POWER_ATTR = 1025
NO_SENSOR_ATTR = 1026
NO_SENSOR_LIST_ATTR = 1027
NO_SHIELD_ATTR = 1028
NO_TECHNOLOGY_ATTR = 1029
NO_MOVEMENT_ATTR = 1030
NO_CLOAK_ATTR = 1031
NO_TRANS_ATTR = 1032
NO_TRACT_ATTR = 1033
NO_COORDS_ATTR = 1034
NO_COURSE_ATTR = 1035
NO_MAIN_ATTR = 1036
NO_AUX_ATTR = 1037
NO_BATT_ATTR = 1038
NO_FUEL_ATTR = 1039
NO_STATUS_ATTR = 1040
NO_BEAM_RECYCLE_ATTR = 1041
NO_MISSILE_RECYCLE_ATTR = 1042
NO_CONSOLE_ATTR = 1100


SDB_ATTR_NAME = "SDB"
LOCATION_ATTR_NAME = "LOCATION"
SPACE_ATTR_NAME = "SPACE"
CLASS_ATTR_NAME = "CLASS"
CONSOLE_ATTR_NAME = "CONSOLES"
CONSOLE_USER_ATTR_NAME = "USER"
SHIP_ATTR_NAME = "SHIP"

ALLOCATE_ATTR_NAME = "ALLOCATE"
ALLOCATE_DATA_NUMBER = 21

BEAM_ATTR_NAME = "BEAM"
BEAM_DATA_NUMBER = 5
BEAM_ACTIVE_ATTR_NAME = "BEAM_ACTIVE"
BEAM_NAME_ATTR_NAME = "BEAM_NAME"
BEAM_RECYCLE_ATTR_NAME = "BEAM_RECYCLE" 
BEAM_DAMAGE_ATTR_NAME = "BEAM_DAMAGE"
BEAM_BONUS_ATTR_NAME = "BEAM_BONUS"
BEAM_COST_ATTR_NAME = "BEAM_COST"
BEAM_RANGE_ATTR_NAME = "BEAM_RANGE"
BEAM_ARCS_ATTR_NAME = "BEAM_ARCS"
BEAM_LOCK_ATTR_NAME = "BEAM_LOCK"
BEAM_LOAD_ATTR_NAME = "BEAM_LOAD"
MAX_BEAM_BANKS = 20

MISSILE_ATTR_NAME = "MISSILE"
MISSILE_DATA_NUMBER = 5
MISSILE_ACTIVE_ATTR_NAME = "MISSILE_ACTIVE"
MISSILE_NAME_ATTR_NAME = "MISSILE_NAME"
MISSILE_RECYCLE_ATTR_NAME = "MISSILE_RECYCLE"
MISSILE_DAMAGE_ATTR_NAME = "MISSILE_DAMAGE"
MISSILE_WARHEAD_ATTR_NAME = "MISSILE_WARHEAD"
MISSILE_COST_ATTR_NAME = "MISSILE_COST"
MISSILE_RANGE_ATTR_NAME = "MISSILE_RANGE"
MISSILE_ARCS_ATTR_NAME = "MISSILE_ARCS"
MISSILE_LOCK_ATTR_NAME = "MISSILE_LOCK"
MISSILE_LOAD_ATTR_NAME = "MISSILE_LOAD"
MAX_MISSILE_TUBES = 20

ENGINE_ATTR_NAME = "ENGINE"
ENGINE_DATA_NUMBER = 9

STRUCTURE_ATTR_NAME = "STRUCTURE"
STRUCTURE_DATA_NUMBER = 12

POWER_ATTR_NAME = "POWER"
POWER_DATA_NUMBER = 5

SENSOR_ATTR_NAME = "SENSOR"
SENSOR_DATA_NUMBER = 17

SENSOR_LIST_ATTR_NAME = "SENSOR_LIST"
SENSOR_LIST_DATA_NUMBER = 3
MAX_SENSOR_CONTACTS = 30

SHIELD_ATTR_NAME = "SHIELD"
SHIELD_DATA_NUMBER = 16

TECHNOLOGY_ATTR_NAME = "TECHNOLOGY"
TECHNOLOGY_DATA_NUMBER = 9

MOVEMENT_ATTR_NAME = "MOVEMENT"
MOVEMENT_DATA_NUMBER = 9

CLOAK_ATTR_NAME = "CLOAK"
CLOAK_DATA_NUMBER = 6

TRANS_ATTR_NAME = "TRANS"
TRANS_DATA_NUMBER = 7

TRACT_ATTR_NAME = "TRACT"
TRACT_DATA_NUMBER = 6

COORDS_ATTR_NAME = "COORDS"
COORDS_DATA_NUMBER = 9

COURSE_ATTR_NAME = "COURSE"
COURSE_DATA_NUMBER = 17

MAIN_ATTR_NAME = "MAIN"
MAIN_DATA_NUMBER = 5

AUX_ATTR_NAME = "AUX"
AUX_DATA_NUMBER = 5

BATT_ATTR_NAME = "BATT"
BATT_DATA_NUMBER = 5

FUEL_ATTR_NAME = "FUEL"
FUEL_DATA_NUMBER = 3

STATUS_ATTR_NAME = "STATUS"
STATUS_DATA_NUMBER = 10

IFF_ATTR_NAME = "IFF"
IFF_DATA_NUMBER = 1
