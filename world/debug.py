from evennia.utils.search import search_tag
import utils

objects = search_tag(category="space_object")
for obj in objects:
    utils.debug_space(obj)