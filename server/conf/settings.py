r"""
Evennia settings file.

The available options are found in the default settings file found
here:

d:\data\git\evennia-dev\evennia\settings_default.py

Remember:

Don't copy more from the default file than you actually intend to
change; this will make sure that you don't overload upstream updates
unnecessarily.

When changing a setting requiring a file system path (like
path/to/actual/file.py), use GAME_DIR and EVENNIA_DIR to reference
your game folder and the Evennia library folders respectively. Python
paths (path.to.module) should be given relative to the game's root
folder (typeclasses.foo) whereas paths within the Evennia library
needs to be given explicitly (evennia.foo).

If you want to share your game dir, including its settings, you can
put secret game- or server-specific settings in secret_settings.py.

"""

# Use the defaults from Evennia unless explicitly overridden
from evennia.settings_default import *

######################################################################
# Evennia base server config
######################################################################

# This is the name of your game. Make it catchy!
SERVERNAME = "Space Combat Simulator"

# Short one-sentence blurb describing your game. Shown under the title
# on the website and could be used in online listings of your game etc.
GAME_SLOGAN = "The Python MUD/MU* creation system"
# Lockdown mode will cut off the game from any external connections
# and only allow connections from localhost. Requires a cold reboot.
LOCKDOWN_MODE = False
# If this is true, errors and tracebacks from the engine will be
# echoed as text in-game as well as to the log. This can speed up
# debugging. OBS: Showing full tracebacks to regular users could be a
# security problem -turn this off in a production game!
IN_GAME_ERRORS = True
# The default home location used for all objects. This is used as a
# fallback if an object's normal home location is deleted. Default
# is Limbo (#2).
DEFAULT_HOME = "#2"
# The start position for new characters. Default is Limbo (#2).
#  MULTISESSION_MODE = 0, 1 - used by default unloggedin create command
#  MULTISESSION_MODE = 2, 3 - used by default character_create command
START_LOCATION = "#2"
# The time factor dictates if the game world runs faster (timefactor>1)
# or slower (timefactor<1) than the real world.
TIME_FACTOR = 2.0
# The starting point of your game time (the epoch), in seconds.
# In Python a value of 0 means Jan 1 1970 (use negatives for earlier
# start date). This will affect the returns from the utils.gametime
# module. If None, the server's first start-time is used as the epoch.
TIME_GAME_EPOCH = None
# Normally, game time will only increase when the server runs. If this is True,
# game time will not pause when the server reloads or goes offline. This setting
# together with a time factor of 1 should keep the game in sync with
# the real time (add a different epoch to shift time)
TIME_IGNORE_DOWNTIMES = True
# The Evennia Game Index is a dynamic listing of Evennia games. You can add your game
# to this list also if it is in closed pre-alpha development.
GAME_INDEX_ENABLED = False
# This dict
GAME_INDEX_LISTING = {
    "game_name": "Mygame",  # usually SERVERNAME
    "game_status": "pre-alpha",  # pre-alpha, alpha, beta or launched
    "short_description": "",  # could be GAME_SLOGAN
    "long_description": "",
    "listing_contact": "",  # email
    "telnet_hostname": "",  # mygame.com
    "telnet_port": "",  # 1234
    "game_website": "",  # http://mygame.com
    "web_client_url": "",  # http://mygame.com/webclient
}
# While DEBUG is False, show a regular server error page on the web
# stuff, email the traceback to the people in the ADMINS tuple
# below. If True, show a detailed traceback for the web
# browser to display. Note however that this will leak memory when
# active, so make sure to turn it off for a production server!
DEBUG = True
# Emails are sent to these people if the above DEBUG value is False. If you'd
# rather prefer nobody receives emails, leave this commented out or empty.
ADMINS = ()  # 'Your Name', 'your_email@domain.com'),)
# These guys get broken link notifications when SEND_BROKEN_LINK_EMAILS is True.
MANAGERS = ADMINS
# This is a public point of contact for players or the public to contact
# a staff member or administrator of the site. It is publicly posted.
STAFF_CONTACT_EMAIL = None


######################################################################
# Settings given in secret_settings.py override those in this file.
######################################################################
try:
    from server.conf.secret_settings import *
except ImportError:
    print("secret_settings.py file not found or failed to import.")
