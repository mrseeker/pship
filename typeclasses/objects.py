"""
Object

The Object is the "naked" base class for things in the game world.

Note that the default Character, Room and Exit does not inherit from
this Object, but from their respective default implementations in the
evennia library. If you want to use this class as a parent to change
the other types, you can do so by adding this as a multiple
inheritance.

"""
from evennia.contrib.rpsystem import ContribRPObject
from world import constants


class Object(ContribRPObject):
    """
    This is the root typeclass object, implementing an in-game Evennia
    game object, such as having a location, being able to be
    manipulated or looked at, etc. If you create a new typeclass, it
    must always inherit from this object (or any of the other objects
    in this file, since they all actually inherit from BaseObject, as
    seen in src.object.objects).

    The BaseObject class implements several hooks tying into the game
    engine. By re-implementing these hooks you can control the
    system. You should never need to re-implement special Python
    methods, such as __init__ and especially never __getattribute__ and
    __setattr__ since these are used heavily by the typeclass system
    of Evennia and messing with them might well break things for you.


    * Base properties defined/available on all Objects

     key (string) - name of object
     name (string)- same as key
     dbref (int, read-only) - unique #id-number. Also "id" can be used.
     date_created (string) - time stamp of object creation

     account (Account) - controlling account (if any, only set together with
                       sessid below)
     sessid (int, read-only) - session id (if any, only set together with
                       account above). Use `sessions` handler to get the
                       Sessions directly.
     location (Object) - current location. Is None if this is a room
     home (Object) - safety start-location
     has_account (bool, read-only)- will only return *connected* accounts
     contents (list of Objects, read-only) - returns all objects inside this
                       object (including exits)
     exits (list of Objects, read-only) - returns all exits from this
                       object, if any
     destination (Object) - only set if this object is an exit.
     is_superuser (bool, read-only) - True/False if this user is a superuser

    * Handlers available

     aliases - alias-handler: use aliases.add/remove/get() to use.
     permissions - permission-handler: use permissions.add/remove() to
                   add/remove new perms.
     locks - lock-handler: use locks.add() to add new lock strings
     scripts - script-handler. Add new scripts to object with scripts.add()
     cmdset - cmdset-handler. Use cmdset.add() to add new cmdsets to object
     nicks - nick-handler. New nicks with nicks.add().
     sessions - sessions-handler. Get Sessions connected to this
                object with sessions.get()
     attributes - attribute-handler. Use attributes.add/remove/get.
     db - attribute-handler: Shortcut for attribute-handler. Store/retrieve
            database attributes using self.db.myattr=val, val=self.db.myattr
     ndb - non-persistent attribute handler: same as db but does not create
            a database entry when storing data

    * Helper methods (see src.objects.objects.py for full headers)

     search(ostring, global_search=False, attribute_name=None,
             use_nicks=False, location=None, ignore_errors=False, account=False)
     execute_cmd(raw_string)
     msg(text=None, **kwargs)
     msg_contents(message, exclude=None, from_obj=None, **kwargs)
     move_to(destination, quiet=False, emit_to_obj=None, use_destination=True)
     copy(new_key=None)
     delete()
     is_typeclass(typeclass, exact=False)
     swap_typeclass(new_typeclass, clean_attributes=False, no_default=True)
     access(accessing_obj, access_type='read', default=False)
     check_permstring(permstring)

    * Hooks (these are class methods, so args should start with self):

     basetype_setup()     - only called once, used for behind-the-scenes
                            setup. Normally not modified.
     basetype_posthook_setup() - customization in basetype, after the object
                            has been created; Normally not modified.

     at_object_creation() - only called once, when object is first created.
                            Object customizations go here.
     at_object_delete() - called just before deleting an object. If returning
                            False, deletion is aborted. Note that all objects
                            inside a deleted object are automatically moved
                            to their <home>, they don't need to be removed here.

     at_init()            - called whenever typeclass is cached from memory,
                            at least once every server restart/reload
     at_cmdset_get(**kwargs) - this is called just before the command handler
                            requests a cmdset from this object. The kwargs are
                            not normally used unless the cmdset is created
                            dynamically (see e.g. Exits).
     at_pre_puppet(account)- (account-controlled objects only) called just
                            before puppeting
     at_post_puppet()     - (account-controlled objects only) called just
                            after completing connection account<->object
     at_pre_unpuppet()    - (account-controlled objects only) called just
                            before un-puppeting
     at_post_unpuppet(account) - (account-controlled objects only) called just
                            after disconnecting account<->object link
     at_server_reload()   - called before server is reloaded
     at_server_shutdown() - called just before server is fully shut down

     at_access(result, accessing_obj, access_type) - called with the result
                            of a lock access check on this object. Return value
                            does not affect check result.

     at_before_move(destination)             - called just before moving object
                        to the destination. If returns False, move is cancelled.
     announce_move_from(destination)         - called in old location, just
                        before move, if obj.move_to() has quiet=False
     announce_move_to(source_location)       - called in new location, just
                        after move, if obj.move_to() has quiet=False
     at_after_move(source_location)          - always called after a move has
                        been successfully performed.
     at_object_leave(obj, target_location)   - called when an object leaves
                        this object in any fashion
     at_object_receive(obj, source_location) - called when this object receives
                        another object

     at_traverse(traversing_object, source_loc) - (exit-objects only)
                              handles all moving across the exit, including
                              calling the other exit hooks. Use super() to retain
                              the default functionality.
     at_after_traverse(traversing_object, source_location) - (exit-objects only)
                              called just after a traversal has happened.
     at_failed_traverse(traversing_object)      - (exit-objects only) called if
                       traversal fails and property err_traverse is not defined.

     at_msg_receive(self, msg, from_obj=None, **kwargs) - called when a message
                             (via self.msg()) is sent to this obj.
                             If returns false, aborts send.
     at_msg_send(self, msg, to_obj=None, **kwargs) - called when this objects
                             sends a message to someone via self.msg().

     return_appearance(looker) - describes this object. Used by "look"
                                 command by default
     at_desc(looker=None)      - called by 'look' whenever the
                                 appearance is requested.
     at_get(getter)            - called after object has been picked up.
                                 Does not stop pickup.
     at_drop(dropper)          - called when this object has been dropped.
     at_say(speaker, message)  - by default, called if an object inside this
                                 object speaks

     """

    def at_object_creation(self):
        super().at_object_creation()

class space_object(Object):
    """
    This creates a default space_object.
    """

    def at_object_creation(self):
        super().at_object_creation()
        self.db.desc = "This is a space object. You should not see this message."
        self.db.type = constants.type_name[0]
        self.db.sdesc = "Default Space Object"
        self.db.location = 0
        self.db.space = 0
        self.db.language = "default"
        self.db.cost = 0
        self.tags.add(tag=constants.type_name[0],category="space_object")
        self.db.coords = {"x":0.0,"y":0.0,"z":0.0,"xo":0.0,"yo":0.0,"zo":0.0,"xd":0.0,"yd":0.0,"zd":0.0}
        self.db.move = {"time":0,"dt":0,"in":0.0,"out":0.0,"ratio":1.0,"cochranes":0.0,"v":0.0,"empire":"","quadrant":0}
        self.db.course = {"version":0,"yaw_in":0.0,"yaw_out":0.0,"pitch_in":0.0,"pitch_out":0.0,"roll_in":0.0,"roll_out":0.0,"d":[[0,0,0],[0,0,0],[0,0,0]],"rate":0.0}
        self.db.iff = {"frequency":0.0}
        shield_combo = {"ratio":0.0,"maximum":0,"freq":0.0,"exist":0}
        for i in range(constants.MAX_SHIELD_NAME):
            shield_combo[i] = {"active":0,"damage":0}
        self.db.shield = shield_combo
        self.db.alloc = {"version":1,"helm":0.0,"tactical":0.0,"operations":0.0,"movement":0.0,"shields":0.0,"shield":[0.0]*constants.MAX_SHIELD_NAME,"cloak":0.0,"beams":0.0,"missiles":0.0,"sensors":0.0,"ecm":0.0,"eccm":0.0,"transporters":0.0,"tractors":0.0,"miscellaneous":0.0}
        self.db.power = {"version":1,"main":0.0,"aux":0.0,"batt":0.0,"total":0.0}
        self.db.sensor = {"version":1,"lrs_damage":1.0,"lrs_active":0,"lrs_exist":0,"lrs_resolution":1.0,"srs_signature":1.0,"srs_damage":1.0,"srs_active":0,"srs_exist":0,"srs_resolution":1.0,"srs_signature":1.0,"ew_damage":1.0,"ew_exist":0,"visibility":1.0,"contacts":0,"counter":0}
        self.db.tech = {"firing":1.0,"fuel":1.0,"stealth":1.0,"cloak":1.0,"sensors":1.0,"aux_max":1.0,"main_max":1.0,"armor":1.0,"ly_range":1.0}
        self.db.engine = {"version":1,"warp_damage":1.0,"warp_max":1.0,"warp_exist":0,"impulse_damage":1.0,"impulse_max":1.0,"impulse_exist":1,"warp_cruise":0.0,"impulse_cruise":0.0}
        self.db.cloak = {"version":1,"cost":0,"freq":0.0,"exist":0,"active":0,"damage":0.0}
        self.db.trans = {"cost":0,"freq":0.0,"exist":0,"active":0,"damage":1.0,"d_lock":0,"s_lock":0}
        self.db.tract = {"cost":0,"freq":0.0,"exist":0,"active":0,"damage":1.0,"lock":0}
        self.db.main = {"in":0.0,"out":0.0,"damage":1.0,"gw":0.0,"exist":0}
        self.db.aux = {"in":0.0,"out":0.0,"damage":1.0,"gw":0.0,"exist":0}
        self.db.batt = {"in":0.0,"out":0.0,"damage":1.0,"gw":0.0,"exist":0}
        self.db.structure = {"type":0,"displacement":1.0,"cargo_hold":0.0, "cargo_mass":0.0, "superstructure":0.0,"has_landing_pad":0,"has_docking_bay":0,"can_land":0,"can_dock":0,"repair":0.0,"max_repair":0}
        self.db.status = {"active":0,"docked":0,"landed":0,"connected":0,"crippled":0,"tractoring":0,"tractored":0,"open_landing":0,"open_docking":0,"link":0,"autopilot":0}
        self.db.fuel = {"antimatter":0,"deuterium":0,"reserves":0}
        self.db.beam = {"in":0.0,"out":0.0,"freq":0.0,"exist":0,"banks":0}
        self.db.missile = {"in":0.0,"out":0.0,"freq":0.0,"exist":0,"tubes":0}
        beam_combo = {}
        for i in range(constants.MAX_BEAM_BANKS):
            beam_combo[i] = {"active":0,"name":0,"lock":"","damage":0.0,"bonus":0,"cost":0,"range":0,"arcs":0,"load":0,"recycle":0}
        self.db.blist = beam_combo
        missile_combo = {}
        for i in range(constants.MAX_MISSILE_TUBES):
            missile_combo[i] = {"active":0,"name":0,"lock":"","damage":0.0,"warhead":0,"cost":0,"range":0,"arcs":0,"load":0,"recycle":0}
        self.db.mlist = missile_combo
        sensor_combo = {}
        for i in range(constants.MAX_SENSOR_CONTACTS):
            sensor_combo[i] = {"key":"","num":0,"lev":0.0}
        self.db.slist = sensor_combo
        
    def get_display_name(self,looker, **kwargs):
       idstr = "(#%s)" % self.id if self.access(looker, access_type="control") else ""
       selfdesc = self.name if self.access(looker, access_type="control") else self.db.sdesc
       return "%s%s" % (selfdesc, idstr)

