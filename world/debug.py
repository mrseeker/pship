from evennia.utils.search import search_tag
from world import utils

objects = search_tag(category="space_object")
for obj in objects:
    print("Debugging " + obj.name)
    if(utils.debug_space(obj) == 1):
        print("{:s}: OK".format(obj.name))
    else:
        print("{:s}: NOK".format(obj.name))