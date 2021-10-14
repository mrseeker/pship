"""
Handles the ticker, needs to be run once...
"""

from evennia.scripts.tickerhandler import TICKER_HANDLER
from world import iterate
TICKER_HANDLER.add(1, iterate.do_space_db_iterate)