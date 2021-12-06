from os import sys
from evennia.server.evennia_launcher import main

sys.argv = ["evennia","--log","start"]
main()
