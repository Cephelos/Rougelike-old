
import math
import random
import shelve
import textwrap


import libtcodpy as libtcod
########################################################################################################################
#   Notes
#
#   Weapon Classes
#
#   LightBlade (Swords, Daggers)
#   HeavyBlade (Greatswords)
#   LightAxe (Hand Axe)
#   HeavyAxe (Greataxe)
#   Hammer (Mace, Club)
#   Staff (Quaterstaff)
#   LightTrowing (Throwing Knives)
#   HeavyThrowing (Hatchets)
#
#   Armor Classes
#
#   LightArmor (Leather, Hide)
#   MediumArmor (Chainmail, Studded)
#   HeavyArmor (Plate, Banded)
#   Cloak (Capes, Cloaks)
#   SmallShield (Round Shield, Kite Shield)
#   LargeShield (Tower Shield, Greatshield)
#
#   Schools of Magic
#
#   Weapon Art (Physical Skills)
#   Miracles (Healing+more)
#   Abjuration (Self-Buffs)
#   Sorcery (Direct Attacks)
#   Necromancy (Death-related)
#   Divination (Knowlage-Gaining)
#   Enchantment (Debuffs)
#   Alteration (Summoning and Changing)
#
#
#   Class
#   Primary Stats
#   Growths
#   Weapons
#   Armor
#   Schools of Magic
#   Starter Spells
#   Class Feats
#   Starting Items
#
#   Knight
#   Strength, Constitution, Intelligence
#   HP: 14+1-8 per level MP: 2-5 + 1 per level
#   LightBlade, HeavyBlade, Spear, LightAxe, HeavyAxe
#   Light, Medium, Heavy, SmallShield, LargeShield
#   Weapon Art, Miracles, Divination
#   Shield Bash
#   1 of:
#       LightBlade+1
#       Spear+1
#   Medium Armor +1
#   Helmet +0
#   SmallShield +0
#   Gloves +0
#   Food
#
#
#
#
#   Barbarian
#   Strength, Constitution, Endurance
#   HP: 14+1-10 per level MP: 1 + 1 per level
#   LightAxe, HeavyAxe, Hammer, HeavyBlade, HeavyThrowing
#   Medium, Heavy, SmallShield, LargeShield
#   Weapon Art, Alteration
#   None
#   Dual Wield, Breaking
#   1 of:
#       HeavyAxe+0
#       LightAxe+1 and LightAxe+0
#   Medium Armor +0
#   Food
#   1 in 6:
#   Oil Lamp
#
#   Mage
#   Intelligence, Wisdom, Constitution
#   HP: 10+1-6 per level MP: 5-7 + 1-2 per level
#   Staff, LightBlade, LightThrowing
#   Light, Cloak
#   Abjuration, Alteration, Necromancy, Divination, Enchantment, Sorcery
#   Force, 1 of: (1 spell from each school)
#   None
#   Staff +1
#   Cloak +0 of MagRes
#   Wand of (random)
#   3x Potion of (random)
#   3x Scroll of (random)
#   2x Ring of (random)
#
#
#
#   Cleric
#   Strength, Wisdom, Constitution
#   HP: 12+1-8 per level MP: 5-7 + 1-2 per level
#   Hammer, LightBlade, SmallShield, HeavyBlade, LightThrowing
#   Light, Medium, Cloak, SmallShield
#   Miracles, Necromancy, Divination
#   Heal, one of: (1 miracle, 1 necro, 1 div)
#   Beatude
#   Blessed Mace+1
#   Cloak+0
#   Small Shield+0
#   4x Blessed Potion of Water
#   2xFood
#
#
#   Rouge
#   Endurance, Strength, Constitution
#   HP: 10 + 1-8 per level MP: 1 + 1 per level
#   LightBlade, LightThrowing, HeavyThrowing
#   Light, Medium, Cloak
#   Abjuration, Alteration
#   None
#   Dual Wielding, Lockpicking
#   LightBlade+0
#   7-16 +0 Throwing Knife
#   LightArmor+1
#   Potion of Sickness
#   Sack
#
#
#
#
#
#
#
#
########################################################################################################################

# FONT = 'arial10x10_gs_tc.png'
# FONT = 'dundalk12x12_gs_tc.png'
FONT = 'terminal12x12_gs_ro.png'

MENU_BG = 'menu_background1.png'


SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50

MAP_WIDTH = 80
MAP_HEIGHT = 43

# sizes and coordinates for the GUI
BAR_WIDTH = 20
PANEL_HEIGHT = 7
PANEL_Y = SCREEN_HEIGHT - PANEL_HEIGHT
LEVEL_SCREEN_WIDTH = 40
CHARACTER_SCREEN_WIDTH = 30

INVENTORY_WIDTH = 50

MSG_X = BAR_WIDTH + 2
MSG_WIDTH = SCREEN_WIDTH - BAR_WIDTH - 2
MSG_HEIGHT = PANEL_HEIGHT - 1

# values for standard map gen
ROOM_MAX_SIZE = 10
ROOM_MIN_SIZE = 6
MAX_ROOMS = 2
SHOW_ROOM_NUM = False

# Values for BSP map gen
DEPTH = 10
MIN_SIZE = 10
FULL_ROOMS = False

# values for FOV
FOV_ALGO = 0
FOV_LIGHT_WALLS = True
SIGHT_RANGE = 10

# makes sure stuff doesnt happen too fast
LIMIT_FPS = 20

LEVEL_UP_BASE = 200
LEVEL_UP_FACTOR = 150

# attack bonus for criticals
CRITMOD = 2

# switch between standard and BSP map gen
BSP = False

# skip player naming
QUICKSTART = True

# allows for debug controls
# F1 make player level 100
DEBUG_CONTROLS = True

DIAG_MOVEMENT = True

DTEST = True


controls_dict = {
    'Arrow Keys, Numpad': 'Move',
    'i': 'open inventory',
    'd': 'drop item',
    'g': 'pick up item',
    's': 'open skills menu',
    'f': 'assign skill hotkeys',
    '1,2,3,4,5': 'skill hotkeys',
    'c': 'show player stats',
    '<': 'go to next floor (when at stairs)',
    '?': 'open help menu',
    'ESC': 'exit to menu (game will be saved)'

}
# base wall and floor colors
color_dark_wall = libtcod.Color(40, 40, 40)
color_light_wall = libtcod.Color(160, 110, 50)
color_dark_ground = libtcod.Color(80, 80, 80)
color_light_ground = libtcod.Color(230, 180, 50)


########################################################################################################################
# Entity Management
########################################################################################################################

class Entity:
    # any entity in-game
    # stairs, player, monster, etc.
    def __init__(self, x, y, char, name, color, blocks=False, always_visible=False, locked=False,
                 telepathy_visible=False, fighter=None, ai=None, item=None, equipment=None, potion=None, ranged=None, scroll=None):
        self.x = x
        self.y = y
        self.char = char
        self.name = name
        self.color = color
        self.blocks = blocks
        self.always_visible = always_visible
        self.locked = locked
        self.telepathy_visible = telepathy_visible

        self.fighter = fighter
        if self.fighter:
            self.fighter.owner = self

        self.ai = ai
        if self.ai:
            self.ai.owner = self

        self.item = item
        if self.item:
            self.item.owner = self


        self.equipment = equipment
        if self.equipment:  # let the Equipment component know who owns it
            self.equipment.owner = self

            # there must be an Item component for the Equipment component to work properly
            self.item = Item(self.equipment.weight)
            self.item.owner = self

        self.potion = potion
        if self.potion:  # let the potion component know who owns it
            self.potion.owner = self

            # there must be an Item component for the potion component to work properly
            self.item = Item(self.potion.weight)
            self.item.owner = self

        self.ranged = ranged
        if self.ranged:  # let the potion component know who owns it
            self.ranged.owner = self

            # there must be an Item component for the potion component to work properly
            self.item = Item(self.ranged.weight)
            self.item.owner = self

        self.scroll = scroll
        if self.scroll:  # let the potion component know who owns it
            self.scroll.owner = self

            # there must be an Item component for the potion component to work properly
            self.item = Item(self.scroll.weight)
            self.item.owner = self

    def move(self, dx, dy):
        if not is_blocked(self.x + dx, self.y + dy):
            self.x += dx
            self.y += dy

    def move_towards(self, target_x, target_y):
        # vector from this entity to the target, and distance
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        # normalize it to length 1 (preserving direction), then round it and
        # convert to integer so the movement is restricted to the map grid
        if DIAG_MOVEMENT == False:
            if dx != 0 and dy != 0:
                dx = int(round(dx / distance))
            else:
                dx = int(round(dx / distance))
                dy = int(round(dy / distance))
        else:
            dx = int(round(dx / distance))
            dy = int(round(dy / distance))
        self.move(dx, dy)

    # astar pathfinding written by reddit user theMillionaire for r/rougelikedev
    # free use

    def move_astar(self, target):
        # Create FOV map with map dimentions
        fov = libtcod.map_new(MAP_WIDTH, MAP_HEIGHT)
        # Scan the current map each turn and set all the walls as unwalkable
        for y1 in range(MAP_HEIGHT):
            for x1 in range(MAP_WIDTH):
                libtcod.map_set_properties(fov, x1, y1, not map[x1][y1].block_sight, not map[x1][y1].blocked)

        # Scan all the entities to see if there are entities that must be navigated around
        # Check also that the entity isn't self or the target (so that the start and the end points are free)
        # The AI class handles the situation if self is next to the target so it will not use this A* function anyway
        for ent in entities:
            if ent.blocks and ent != self and ent != target:
                # Set the tile as a wall so it must be navigated around
                libtcod.map_set_properties(fov, ent.x, ent.y, True, False)

        # Allocate a A* path
        # The 1.41 is the normal diagonal cost of moving, it can be set as 0.0 if diagonal moves are prohibited
        if DIAG_MOVEMENT == False:
            my_path = libtcod.path_new_using_map(fov, 0.0)
        else:
            my_path = libtcod.path_new_using_map(fov, 1.41)

        # Compute the path between self's coordinates and the target's coordinates
        libtcod.path_compute(my_path, self.x, self.y, target.x, target.y)

        # Check if the path exists, and in this case, also the path is shorter than 25 tiles
        # The path size matters if you want the monster to use alternative longer paths (for example through other rooms) if for example the player is in a corridor
        # It makes sense to keep path size relatively low to keep the monsters from running around the map if there's an alternative path really far away
        if not libtcod.path_is_empty(my_path) and libtcod.path_size(my_path) < 25:
            # Find the next coordinates in the computed full path
            x, y = libtcod.path_walk(my_path, True)
            if x or y:
                # Set self's coordinates to the next path tile
                self.x = x
                self.y = y
        else:
            # Keep the old move function as a backup so that if there are no paths (for example another monster blocks a corridor)
            # it will still try to move towards the player (closer to the corridor opening)
            self.move_towards(target.x, target.y)

            # Delete the path to free memory
        libtcod.path_delete(my_path)

    def distance_to(self, other):
        # return the distance to another entity
        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt(dx ** 2 + dy ** 2)

    def draw(self):
        # if in FOV
        # only show if it's visible to the player; or it's set to "always visible" and on an explored tile
        if (libtcod.map_is_in_fov(fov_map, self.x, self.y) or (
            self.always_visible and map[self.x][self.y].explored) or self.telepathy_visible):
            libtcod.console_set_default_foreground(con, self.color)
            libtcod.console_put_char(con, self.x, self.y, self.char, libtcod.BKGND_NONE)

    def clear(self):
        # erases character after movement, avoid trail
        libtcod.console_put_char(con, self.x, self.y, ' ', libtcod.BKGND_NONE)

    def send_to_back(self):
        # make this entity be drawn first, so all others appear above it if they're in the same tile.
        global entities
        entities.remove(self)
        entities.insert(0, self)

    def distance(self, x, y):
        # return the distance to some coordinates
        return math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)

    def in_line(self, target):
        # checks to see if target is in line with caster, useful for AI w/ ranged attacks
        dx = target.x - self.x
        dy = target.y - self.y
        if abs(self.x) == abs(target.x):
            if dy > 0:
                return (0, 1)
            else:
                return (0, -1)

        elif abs(self.y) == abs(target.y):
            if dx > 0:
                return (1, 0)
            else:
                return (-1, 0)

        elif (abs(self.x) == abs(target.x) + 1 or abs(self.x) == abs(target.x) - 1) and abs(self.y) == abs(
                target.y) + 1:
            if abs(self.x) == abs(target.x) + 1:
                return (1, -1)
            else:
                return (-1, -1)

        elif (abs(self.x) == abs(target.x) + 1 or abs(self.x) == abs(target.x) - 1) and abs(self.y) == abs(
                target.y) - 1:
            if abs(self.x) == abs(target.x) + 1:
                return (1, -1)
            else:
                return (-1, -1)



        else:
            return (0, 0)


class Fighter:
    # combat-related properties

    def __init__(self, xp, hp_stat, mp_stat, constitution, strength, dexterity, wisdom, intelligence, agility, nutrition=800, growths=[], perks=[], skills=[], effects=[], race=None, job=None, gender='male', death_function=None, attack_type='attacks'):
        self.base_max_hp = hp_stat
        self.hp = hp_stat
        self.base_max_mp = mp_stat
        self.mp = mp_stat
        self.base_defense = 0
        self.base_evasion = 5
        self.base_accuracy = 100
        self.base_power = 0
        self.base_magic = 0
        self.base_crit = 0
        self.xp = xp
        self.hp_stat = hp_stat
        self.mp_stat = mp_stat
        self.constitution = constitution
        self.strength = strength
        self.dexterity = dexterity
        self.agility = agility
        self.wisdom = wisdom
        self.intelligence = intelligence
        self.agility = agility
        self.race = race
        self.job = job
        self.gender = gender
        self.death_function = death_function
        self.skills = []
        self.growths = []
        self.base_carry_weight = constitution * 2.5 + 30
        self.nutrition = nutrition
        self.effects = []

    def take_damage(self, damage):

        if damage > 0:
            self.hp -= damage

        if self.hp <= 0:
            function = self.death_function
            if function is not None:
                function(self.owner)

            if self.owner != player:  # yield experience to the player
                player.fighter.xp += self.xp

    def attack(self, target, type='attacks'):
        # attack formula
        caster = self.owner
        if hit_formula(caster, target):
            (damage, critical) = attack_formula(caster, target)

            if (critical == True):

                if damage < 0: damage = 0
                message(
                    self.owner.name.capitalize() + ' ' + type + ' ' + target.name + ' and scores a critical hit for ' + str(
                        damage) + ' damage!', libtcod.gold)

            else:
                if damage < 0: damage = 0.
                message(self.owner.name.capitalize() + ' ' + type + ' ' + target.name + ' for ' + str(damage) + ' damage.',
                        libtcod.white)
            target.fighter.take_damage(damage)
        else:
            message('You miss!')

    def heal(self, amt):
        # heal by amt up to max
        self.hp += amt
        if self.hp > self.max_hp:
            self.hp = self.max_hp

    if 'fighter properties' or True:
        @property
        def power(self):
            bonus = sum(equipment.power_bonus for equipment in get_all_equipped(self.owner))
            return self.base_power + bonus

        @property
        def defense(self):
            bonus = sum(equipment.defense_bonus for equipment in get_all_equipped(self.owner))
            return self.base_defense + bonus

        @property
        def accuracy(self):
            bonus = sum(equipment.accuracy_bonus for equipment in get_all_equipped(self.owner))
            return self.base_accuracy + bonus

        @property
        def evasion(self):
            bonus = sum(equipment.evasion_bonus for equipment in get_all_equipped(self.owner))
            return self.base_evasion + bonus

        @property
        def max_hp(self):
            bonus = sum(equipment.max_hp_bonus for equipment in get_all_equipped(self.owner))
            return self.base_max_hp + bonus

        @property
        def max_mp(self):
            bonus = sum(equipment.max_mp_bonus for equipment in get_all_equipped(self.owner))
            return self.base_max_mp + bonus

        @property
        def magic(self):
            bonus = sum(equipment.power_bonus for equipment in get_all_equipped(self.owner))
            return self.base_magic + bonus

        @property
        def crit(self):
            bonus = sum(equipment.power_bonus for equipment in get_all_equipped(self.owner))
            return self.base_crit + bonus

        @property
        def carry_weight(self):
            bonus = sum(equipment.carry_weight_bonus for equipment in get_all_equipped(self.owner))
            return self.base_carry_weight + bonus

        @property
        def attack_type(self):
            return equipment.attack_type


class Item:
    global entities
    # pick-up-able item
    def __init__(self, weight, use_function=None, consumable=True, stackable=False, amt=1):
        self.weight = weight
        self.use_function = use_function
        self.consumable = consumable
        self.stackable = stackable
        self.amt = amt


    def pick_up(self):
        # add to inv remove from map
        if len(inventory) >= 26:
            message('Your inventory is full, cannot pick up ' + self.owner.name + '.', libtcod.red)
        else:

            if player.x == self.owner.x and player.y == self.owner.y:
                if self.owner.potion or self.owner.ranged or self.owner.scroll:

                    for inv in inventory:

                        if self.owner.name == inv.name:
                            inv.item.amt += self.amt
                            message('You picked up a ' + self.owner.name + 'x' + str(self.amt) + '. You now have ' + str(
                                inv.item.amt) + '.', libtcod.green)
                            entities.remove(self.owner)
                            break
                    else:
                        if self.owner in entities:

                            inventory.append(self.owner)
                            entities.remove(self.owner)

                            message('You picked up a ' + self.owner.name + 'x' + str(self.amt) + '.', libtcod.green)


                else:
                    if self.owner in entities:
                        inventory.append(self.owner)
                        message('You picked up a ' + self.owner.name + '.', libtcod.green)

                        entities.remove(self.owner)

    def use(self):
        # special case: if the entity has the Equipment component, the "use" action is to equip/dequip
        if self.owner.equipment:
            self.owner.equipment.toggle_equip()
            return

        if self.owner.ranged:
            self.owner.ranged.toggle_ready()
            return

        if self.owner.scroll:

            if self.owner.scroll.teach is not None:

                teach_skill(self.owner.scroll.teach, player)

            else:
                self.owner.scroll.spell(player)

            if self.amt == 1:
                inventory.remove(self.owner)  # consume item if consumable
            else:
                self.amt -= 1

            return
        if self.owner.potion:
            consume_potion(self.potion.effect, self.potion.magnitude, self.potion.duration)
            if self.amt == 1:
                inventory.remove(self.owner)  # consume item if consumable
            else:
                self.amt -= 1
            return
        if self.use_function is None:
            # calls use function
            message('The ' + self.owner.name + ' cannot be used.')

    def drop(self):
        # special case: if the entity has the Equipment component, dequip it before dropping
        if self.owner.equipment:
            self.owner.equipment.dequip()

        # add to the map and remove from the player's inventory. also, place it at the player's coordinates
        entities.append(self.owner)
        inventory.remove(self.owner)
        self.owner.x = player.x
        self.owner.y = player.y
        if self.stackable and self.amt > 1:
            message('You dropped a ' + self.owner.name + 'x' + str(self.amt) + '.', libtcod.yellow)
        else:
            message('You dropped a ' + self.owner.name + '.', libtcod.yellow)
        self.owner.send_to_back()


class Potion:
    #TODO add status effects to potions
    def __init__(self, weight, effect, magnitude, duration):
        self.weight = weight
        self.item = Item(weight, stackable=True)
        self.effect = effect
        self.magnitude = magnitude
        self.duration = duration


class Scroll:

    def __init__(self, weight, spell, teach=None):
        self.weight = weight
        self.item = Item(weight, stackable=True)
        self.spell = spell
        self.teach = teach


class RangedWeapon:

    def __init__(self, weight, damage, effect, range, ready=False):
        self.weight = weight
        self.item = Item(weight, stackable=True)
        self.damage = damage
        self.effect = effect
        self.range = range
        self.ready = ready

    def toggle_ready(self):  # toggle equip/dequip status
        if self.ready:
            self.unequip_ranged()
        else:
            self.equip_ranged()

    def equip_ranged(self):
        # equip entity and show a message about it
        old_weap = None
        for ent in inventory:
            if ent.ranged and ent.ranged.ready:
                old_weap = ent.ranged
                break

        if old_weap is not None:
            old_weap.unequip_ranged()

        self.ready = True


        message('Readied ' + self.owner.name + '.', libtcod.light_green)

    def unequip_ranged(self):
        # dequip entity and show a message about it
        if not self.ready: return
        self.ready = False
        message('Put away ' + self.owner.name + '.', libtcod.light_yellow)


class Skill:
    def __init__(self, name, cast_function, cost, school, bind=None, user=None):
        self.name = name
        self.cast_function = cast_function
        self.cost = cost
        self.bind = bind

    def cast(self):
        # calls use function
        #TODO replace this if need to have enemies use skills from a skill list
        caster = player
        if self.cast_function is None:
            message('The ' + self.owner.name + ' cannot be cast.')
        if caster.fighter.mp < self.cost:
            message('You lack the required MP.')
        else:
            if self.cast_function(caster) != 'cancelled':
                caster.fighter.mp -= self.cost


class Equipment:
    # an entity that can be equipped, yielding bonuses. automatically adds the Item component.
    def __init__(self, weight, itemclass, slot, power_bonus=0, defense_bonus=0, accuracy_bonus=0, evasion_bonus=0, max_hp_bonus=0,
                 magic_bonus=0, max_mp_bonus=0, carry_weight_bonus=0, skill_level=0, attack_type='attacks'):
        self.slot = slot
        self.is_equipped = False
        # there must be an Item component for the Equipment component to work properly
        self.weight = weight
        self.item = Item(weight)
        self.item.owner = self
        self.power_bonus = power_bonus
        self.defense_bonus = defense_bonus
        self.accuracy_bonus = accuracy_bonus
        self.evasion_bonus = evasion_bonus
        self.max_hp_bonus = max_hp_bonus
        self.magic_bonus = magic_bonus
        self.max_mp_bonus = max_mp_bonus
        self.skill_level = skill_level
        self.attack_type = attack_type

    def toggle_equip(self):  # toggle equip/dequip status
        if self.is_equipped:
            self.dequip()
        else:
            self.equip()

    def equip(self):
        # equip entity and show a message about it
        for i in range(3):
            old_equipment = get_equipped_in_slot(self.slot)

            if old_equipment is not None:
                old_equipment.dequip()

        slotname = ''
        for i in range(len(self.slot)):
            slotname = slotname + str(self.slot[i]) + ', '

        slotname = slotname[:-2]

        self.is_equipped = True
        message('Equipped ' + self.owner.name + ' on ' + slotname + '.', libtcod.light_green)

    def dequip(self):
        # dequip entity and show a message about it
        slotname = ''
        for i in range(len(self.slot)):
            slotname = slotname + str(self.slot[i]) + ', '

        slotname = slotname[:-2]

        if not self.is_equipped: return
        self.is_equipped = False
        message('Dequipped ' + self.owner.name + ' from ' + slotname + '.', libtcod.light_yellow)


########################################################################################################################
# Monster AI
########################################################################################################################

class BasicMonster:
    # Moves toward player when in sight+1

    def take_turn(self):

        # monster takes its turn. if you can see it, it can see you
        monster = self.owner

        if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):

            # move towards player if far away
            if monster.distance_to(player) >= 2:
                monster.move_astar(player)

            # close enough, attack! (if the player is still alive.)
            elif player.fighter.hp > 0:
                monster.fighter.attack(player)


class MageBasicMonster:
    def take_turn(self):

        # monster takes its turn. if you can see it, it can see you
        monster = self.owner
        # teach_skill('force', monster)
        if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):

            # move towards player if far away
            if monster.distance_to(player) > 3:
                monster.move_astar(player)

            # close enough, attack! (if the player is still alive.)
            elif player.fighter.hp > 0:
                (x, y) = monster.in_line(player)
                if (x, y) != (0, 0):
                    cast_force(monster)


class RangedBasicMonster:
    def take_turn(self):

        # monster takes its turn. if you can see it, it can see you
        monster = self.owner
        (a, b) = monster.in_line(player)

        if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):

            # move towards player if far away

            if (a, b) == (0, 0) or monster.distance_to(player) > 3:
                monster.move_astar(player)

            # close enough, attack! (if the player is still alive.)
            elif player.fighter.hp > 0:
                (x, y) = monster.in_line(player)
                if (x, y) != (0, 0):
                    monster.fighter.attack(player, type='shoots')


class ConfusedMonster:
    # Ai for confused monster (moves randomly)
    def __init__(self, old_ai, num_turns):
        self.old_ai = old_ai
        self.num_turns = num_turns

    def take_turn(self):
        if self.num_turns > 0:  # still confused
            # move in random direction
            self.owner.move(libtcod.random_get_int(0, -1, 1), libtcod.random_get_int(0, -1, 1))
            self.num_turns -= 1

        else:  # restore previous ai
            self.owner.ai = self.old_ai
            message('The ' + self.owner.name + ' is no longer confused!')
            self.owner.fighter.effects.remove('confused')


class DazedMonster:
    # AI for dazed monster (can't move)
    def __init__(self, old_ai, num_turns):
        self.old_ai = old_ai
        self.num_turns = num_turns

    def take_turn(self):
        if self.num_turns > 0:  # still dazed
            # move in random direction
            self.owner.move(0, 0)
            self.num_turns -= 1

        else:  # restore previous ai
            self.owner.ai = self.old_ai
            message('The ' + self.owner.name + ' is no longer dazed!')
            self.owner.fighter.effects.remove('dazed')


########################################################################################################################
#   Map Generation
########################################################################################################################

class Tile:
    # Tile and properties
    def __init__(self, blocked, block_sight=None):
        # blocked = wall
        self.blocked = blocked
        self.explored = False

        # blocked blocks sight unless otherwise specified
        if block_sight is None:
            block_sight = blocked
        self.block_sight = block_sight


class Rect:
    # a rectangle on the map. used to characterize a room.
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h

    def center(self):
        center_x = (self.x1 + self.x2) / 2
        center_y = (self.y1 + self.y2) / 2
        return (center_x, center_y)

    def intersect(self, other):
        # returns true if this rectangle intersects with another one
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)


if BSP:
    def make_bsp():
        global map, entities, stairs, bsp_rooms, monster_set

        entities = [player]

        map = [[Tile(True) for y in range(MAP_HEIGHT)] for x in range(MAP_WIDTH)]

        # Empty global list for storing room coordinates
        bsp_rooms = []

        # New root node
        bsp = libtcod.bsp_new_with_size(0, 0, MAP_WIDTH, MAP_HEIGHT)

        # Split into nodes
        libtcod.bsp_split_recursive(bsp, 0, DEPTH, MIN_SIZE + 1, MIN_SIZE + 1, 1.5, 1.5)

        # Traverse the nodes and create rooms
        libtcod.bsp_traverse_inverted_level_order(bsp, traverse_node)

        # Random room for the stairs
        stairs_location = random.choice(bsp_rooms)
        bsp_rooms.remove(stairs_location)
        stairs = Entity(stairs_location[0], stairs_location[1], '<', 'stairs', libtcod.white, always_visible=True)
        entities.append(stairs)
        stairs.send_to_back()

        # Random room for player start
        player_room = random.choice(bsp_rooms)
        bsp_rooms.remove(player_room)
        player.x = player_room[0]
        player.y = player_room[1]

        # determines the type of monsters that appear on the floor
        monster_set = set_monster_squad()
        # Add monsters and items
        for room in bsp_rooms:
            new_room = Rect(room[0], room[1], 2, 2)

            place_entities(new_room, monster_set)

        initialize_fov()


    def traverse_node(node, dat):
        global map, bsp_rooms

        # Create rooms
        if libtcod.bsp_is_leaf(node):
            minx = node.x + 1
            maxx = node.x + node.w - 1
            miny = node.y + 1
            maxy = node.y + node.h - 1

            if maxx == MAP_WIDTH - 1:
                maxx -= 1
            if maxy == MAP_HEIGHT - 1:
                maxy -= 1

            # If it's False the rooms sizes are random, else the rooms are filled to the node's size
            if FULL_ROOMS == False:
                minx = libtcod.random_get_int(None, minx, maxx - MIN_SIZE + 1)
                miny = libtcod.random_get_int(None, miny, maxy - MIN_SIZE + 1)
                maxx = libtcod.random_get_int(None, minx + MIN_SIZE - 2, maxx)
                maxy = libtcod.random_get_int(None, miny + MIN_SIZE - 2, maxy)

            node.x = minx
            node.y = miny
            node.w = maxx - minx + 1
            node.h = maxy - miny + 1

            # Dig room
            for x in range(minx, maxx + 1):
                for y in range(miny, maxy + 1):
                    map[x][y].blocked = False
                    map[x][y].block_sight = False

            # Add center coordinates to the list of rooms
            bsp_rooms.append(((minx + maxx) / 2, (miny + maxy) / 2))

        # Create corridors
        else:
            left = libtcod.bsp_left(node)
            right = libtcod.bsp_right(node)
            node.x = min(left.x, right.x)
            node.y = min(left.y, right.y)
            node.w = max(left.x + left.w, right.x + right.w) - node.x
            node.h = max(left.y + left.h, right.y + right.h) - node.y
            if node.horizontal:
                if left.x + left.w - 1 < right.x or right.x + right.w - 1 < left.x:
                    x1 = libtcod.random_get_int(None, left.x, left.x + left.w - 1)
                    x2 = libtcod.random_get_int(None, right.x, right.x + right.w - 1)
                    y = libtcod.random_get_int(None, left.y + left.h, right.y)
                    vline_up(map, x1, y - 1)
                    hline(map, x1, y, x2)
                    vline_down(map, x2, y + 1)

                else:
                    minx = max(left.x, right.x)
                    maxx = min(left.x + left.w - 1, right.x + right.w - 1)
                    x = libtcod.random_get_int(None, minx, maxx)
                    vline_down(map, x, right.y)
                    vline_up(map, x, right.y - 1)

            else:
                if left.y + left.h - 1 < right.y or right.y + right.h - 1 < left.y:
                    y1 = libtcod.random_get_int(None, left.y, left.y + left.h - 1)
                    y2 = libtcod.random_get_int(None, right.y, right.y + right.h - 1)
                    x = libtcod.random_get_int(None, left.x + left.w, right.x)
                    hline_left(map, x - 1, y1)
                    vline(map, x, y1, y2)
                    hline_right(map, x + 1, y2)
                else:
                    miny = max(left.y, right.y)
                    maxy = min(left.y + left.h - 1, right.y + right.h - 1)
                    y = libtcod.random_get_int(None, miny, maxy)
                    hline_left(map, right.x - 1, y)
                    hline_right(map, right.x, y)

        return True


    def vline(map, x, y1, y2):
        if y1 > y2:
            y1, y2 = y2, y1

        for y in range(y1, y2 + 1):
            map[x][y].blocked = False
            map[x][y].block_sight = False


    def vline_up(map, x, y):
        while y >= 0 and map[x][y].blocked == True:
            map[x][y].blocked = False
            map[x][y].block_sight = False
            y -= 1
        create_door(x, y + 1, 'horizontal')


    def vline_down(map, x, y):
        while y < MAP_HEIGHT and map[x][y].blocked == True:
            map[x][y].blocked = False
            map[x][y].block_sight = False
            y += 1
        create_door(x, y - 1, 'horizontal')


    def hline(map, x1, y, x2):
        if x1 > x2:
            x1, x2 = x2, x1
        for x in range(x1, x2 + 1):
            map[x][y].blocked = False
            map[x][y].block_sight = False


    def hline_left(map, x, y):
        while x >= 0 and map[x][y].blocked == True:
            map[x][y].blocked = False
            map[x][y].block_sight = False
            x -= 1
        create_door(x + 1, y, 'vertical')


    def hline_right(map, x, y):
        while x < MAP_WIDTH and map[x][y].blocked == True:
            map[x][y].blocked = False
            map[x][y].block_sight = False
            x += 1
        create_door(x - 1, y, 'vertical')

else:

    def create_room(room):
        global map
        # Iterate through room, make tiles passable
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                map[x][y].blocked = False
                map[x][y].block_sight = False


    def create_h_tunnel(x1, x2, y):
        global map
        # horizontal tunnel
        for x in range(min(x1, x2), max(x1, x2) + 1):
            map[x][y].blocked = False
            map[x][y].block_sight = False


    def create_v_tunnel(y1, y2, x):
        global map
        # vertical tunnel
        for y in range(min(y1, y2), max(y1, y2) + 1):
            map[x][y].blocked = False
            map[x][y].block_sight = False


    def make_map():
        global map, entities, stairs

        # the list of entities with just the player
        entities = [player]

        # fill map w/ floor
        map = [[Tile(True)
                for y in range(MAP_HEIGHT)]
               for x in range(MAP_WIDTH)]

        rooms = []
        num_rooms = 0

        for r in range(MAX_ROOMS):
            # rand w & h
            w = libtcod.random_get_int(0, ROOM_MIN_SIZE, ROOM_MAX_SIZE)
            h = libtcod.random_get_int(0, ROOM_MIN_SIZE, ROOM_MAX_SIZE)
            # rand pos within map
            x = libtcod.random_get_int(0, 0, MAP_WIDTH - w - 1)
            y = libtcod.random_get_int(0, 0, MAP_HEIGHT - h - 1)

            new_room = Rect(x, y, w, h)

            failed = False
            for other_room in rooms:
                if new_room.intersect(other_room):
                    failed = True
                    break

            if not failed:
                # no intersect
                create_room(new_room)

                (new_x, new_y) = new_room.center()

                if SHOW_ROOM_NUM:
                    room_no = Entity(new_x, new_y, chr(65 + num_rooms), 'room number', 'label', libtcod.white)
                    entities.insert(0, room_no)  # draw early, so monsters are drawn on top

                if num_rooms == 0:
                    # first room
                    player.x = new_x
                    player.y = new_y

                else:
                    # connect to previous room

                    (prev_x, prev_y) = rooms[num_rooms - 1].center()

                    # randomly choose to do h then v tunnel or vice-versa
                    if libtcod.random_get_int(0, 0, 1) == 1:
                        create_h_tunnel(prev_x, new_x, prev_y)
                        create_v_tunnel(prev_y, new_y, new_x)
                    else:
                        create_v_tunnel(prev_y, new_y, prev_x)
                        create_h_tunnel(prev_x, new_x, new_y)
                monster_sets = {}

                monster_sets['goblins'] = 50
                monster_sets['orcs'] = 50
                monster_sets['skeletons'] = 50
                monster_sets['demons'] = 50
                set = random_choice(monster_sets)

                place_entities(new_room, set)
                rooms.append(new_room)
                num_rooms += 1

        # put stairs in last room
        stairs = Entity(new_x, new_y, '<', 'stairs', libtcod.white, always_visible=True)
        entities.append(stairs)
        stairs.send_to_back()


def initialize_fov():
    global fov_recompute, fov_map

    fov_recompute = True

    # create the FOV map, according to the generated map
    fov_map = libtcod.map_new(MAP_WIDTH, MAP_HEIGHT)
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            libtcod.map_set_properties(fov_map, x, y, not map[x][y].block_sight, not map[x][y].blocked)

    libtcod.console_clear(con)  # unexplored areas start black (which is the default background color)


########################################################################################################################
#   Entity Placement and rendering
########################################################################################################################

def place_entities(room, set):

    # data for random gen stuff

    if 'room gen data' or True:
        # choose random number of monsters
        # maximum number of monsters per room
        max_monsters = from_dungeon_level([[2, 1], [3, 4], [5, 6]])


        if set == 'goblins':
            # chance of each monster
            monster_chances = {}
            monster_chances['goblin'] = 80
            monster_chances['troll'] = from_dungeon_level([[15, 3], [30, 5], [60, 7]])
            monster_chances['goblin shaman'] = from_dungeon_level([[15, 2], [30, 4], [60, 6]])
            monster_chances['goblin crossbowman'] = from_dungeon_level([[15, 2], [30, 4], [60, 6]])
            monster_chances['ogre'] = from_dungeon_level([[15, 5], [30, 7], [60, 9]])

        elif set == 'orcs':
            monster_chances = {}
            monster_chances['orc fighter'] = 80
            monster_chances['orc warrior'] = from_dungeon_level([[15, 3], [30, 5], [60, 7]])
            monster_chances['orc mage'] = from_dungeon_level([[15, 2], [30, 4], [60, 6]])
            monster_chances['orc crossbowman'] = from_dungeon_level([[15, 2], [30, 4], [60, 6]])
            monster_chances['orc warlord'] = from_dungeon_level([[15, 5], [30, 7], [60, 9]])

        elif set == 'demons':
            monster_chances = {}
            monster_chances['imp'] = 80
            monster_chances['devil'] = from_dungeon_level([[15, 3], [30, 5], [60, 7]])
            monster_chances['lava frog'] = from_dungeon_level([[15, 2], [30, 4], [60, 6]])
            monster_chances['spitter'] = from_dungeon_level([[15, 2], [30, 4], [60, 6]])
            monster_chances['archdemon'] = from_dungeon_level([[15, 5], [30, 7], [60, 9]])

        elif set == 'skeletons':
            monster_chances = {}
            monster_chances['skeleton'] = 80
            monster_chances['skeletal warrior'] = from_dungeon_level([[15, 3], [30, 5], [60, 7]])
            monster_chances['skeleton necromancer'] = from_dungeon_level([[15, 2], [30, 4], [60, 6]])
            monster_chances['skeleton archer'] = from_dungeon_level([[15, 2], [30, 4], [60, 6]])
            monster_chances['skeleton lord'] = from_dungeon_level([[15, 5], [30, 7], [60, 9]])

        max_items = 10#from_dungeon_level([[1, 1], [2, 4]])

        # chance of each item (by default they have a chance of 0 at level 1, which then goes up)
        item_chances = {}
        item_chances['heal'] = 35  # healing potion always shows up, even if all other items have 0 chance
        item_chances['lightning'] = from_dungeon_level([[25, 4]])
        item_chances['fireburst'] = from_dungeon_level([[25, 6]])
        item_chances['confuse'] = from_dungeon_level([[10, 2]])
        item_chances['long sword'] = from_dungeon_level([[5, 4]])
        item_chances['shield'] = from_dungeon_level([[15, 8]])

    num_monsters = libtcod.random_get_int(0, 0, max_monsters)

    for i in range(num_monsters):
        # choose random spot for this monster
        x = libtcod.random_get_int(0, room.x1 + 1, room.x2 - 1)
        y = libtcod.random_get_int(0, room.y1 + 1, room.y2 - 1)

        # only place it if the tile is not blocked
        if not is_blocked(x, y):
            monster = None
            choice = random_choice(monster_chances)
            ########################################################################################################################
            #   Goblins
            ########################################################################################################################
            if set == 'goblins':
                if choice == 'goblin':
                    # create an goblin
                    fighter_component = Fighter(xp=20, hp_stat=20, mp_stat=0, constitution=2, strength=4, dexterity=0,
                                                intelligence=0, wisdom=0, agility=2, race='goblin',
                                                death_function=monster_death)
                    ai_component = BasicMonster()

                    monster = Entity(x, y, 'g', 'goblin', libtcod.desaturated_green, blocks=True,
                                     fighter=fighter_component, ai=ai_component)

                elif choice == 'troll':
                    # create a troll
                    fighter_component = Fighter(xp=40, hp_stat=40, mp_stat=0, constitution=4, strength=8, dexterity=4,
                                                intelligence=0, wisdom=0, agility=1, race='goblin',
                                                death_function=monster_death)
                    ai_component = BasicMonster()

                    monster = Entity(x, y, 't', 'troll', libtcod.desaturated_green, blocks=True,
                                     fighter=fighter_component, ai=ai_component)

                elif choice == 'goblin shaman':
                    # create a troll
                    fighter_component = Fighter(xp=30, hp_stat=20, mp_stat=30, constitution=2, strength=1, dexterity=2,
                                                intelligence=3, wisdom=3, agility=1, race='orc',
                                                death_function=monster_death)
                    ai_component = MageBasicMonster()

                    monster = Entity(x, y, 's', 'goblin shaman', libtcod.desaturated_green, blocks=True,
                                     fighter=fighter_component, ai=ai_component)

                elif choice == 'goblin rifleman':
                    # create an orc
                    fighter_component = Fighter(xp=30, hp_stat=20, mp_stat=30, constitution=2, strength=3, dexterity=2,
                                                intelligence=1,
                                                wisdom=3,
                                                agility=1, race='goblin', death_function=monster_death)
                    ai_component = RangedBasicMonster()

                    monster = Entity(x, y, 'r', 'goblin rifleman', libtcod.desaturated_green, blocks=True,
                                     fighter=fighter_component,
                                     ai=ai_component)

                elif choice == 'ogre':
                    # create an orc
                    fighter_component = Fighter(xp=60, hp_stat=80, mp_stat=0, constitution=8, strength=16, dexterity=5,
                                                intelligence=0, wisdom=0, agility=1, race='goblin',
                                                death_function=monster_death)
                    ai_component = BasicMonster()

                    monster = Entity(x, y, 'O', 'ogre', libtcod.desaturated_green, blocks=True,
                                     fighter=fighter_component, ai=ai_component)

            ########################################################################################################################
            #   Orcs
            ########################################################################################################################
            if set == 'orcs':
                if choice == 'orc fighter':
                    # create an orc
                    fighter_component = Fighter(xp=20, hp_stat=20, mp_stat=0, constitution=2, strength=4, dexterity=0,
                                                intelligence=0, wisdom=0, agility=2, race='orc',
                                                death_function=monster_death)
                    ai_component = BasicMonster()

                    monster = Entity(x, y, 'f', 'orc fighter', libtcod.darker_green, blocks=True,
                                     fighter=fighter_component, ai=ai_component)

                elif choice == 'orc warrior':
                    # create a troll
                    fighter_component = Fighter(xp=40, hp_stat=40, mp_stat=0, constitution=4, strength=8, dexterity=4,
                                                intelligence=0, wisdom=0, agility=1, race='orc',
                                                death_function=monster_death)
                    ai_component = BasicMonster()

                    monster = Entity(x, y, 'w', 'orc warrior', libtcod.darker_green, blocks=True,
                                     fighter=fighter_component, ai=ai_component)

                elif choice == 'orc mage':
                    # create an orc
                    fighter_component = Fighter(xp=30, hp_stat=20, mp_stat=30, constitution=2, strength=1, dexterity=2,
                                                intelligence=3, wisdom=3, agility=1, race='orc',
                                                death_function=monster_death)
                    ai_component = MageBasicMonster()

                    monster = Entity(x, y, 'm', 'orc mage', libtcod.darker_green, blocks=True,
                                     fighter=fighter_component, ai=ai_component)

                elif choice == 'orc crossbowman':
                    # create an orc
                    fighter_component = Fighter(xp=30, hp_stat=20, mp_stat=30, constitution=2, strength=3, dexterity=2,
                                                intelligence=1,
                                                wisdom=3,
                                                agility=1, race='orc', death_function=monster_death)
                    ai_component = RangedBasicMonster()

                    monster = Entity(x, y, 'c', 'orc crossbowman', libtcod.darker_green, blocks=True,
                                     fighter=fighter_component,
                                     ai=ai_component)

                elif choice == 'orc warlord':
                    # create an orc
                    fighter_component = Fighter(xp=60, hp_stat=80, mp_stat=0, constitution=8, strength=16, dexterity=5,
                                                intelligence=0, wisdom=0, agility=1, race='orc',
                                                death_function=monster_death)
                    ai_component = BasicMonster()

                    monster = Entity(x, y, 'W', 'orc warlord', libtcod.darker_green, blocks=True,
                                     fighter=fighter_component, ai=ai_component)

            ########################################################################################################################
            #   Demons
            ########################################################################################################################
            if set == 'demons':
                if choice == 'imp':
                    # create an orc
                    fighter_component = Fighter(xp=20, hp_stat=20, mp_stat=0, constitution=2, strength=4, dexterity=0,
                                                intelligence=0, wisdom=0,
                                                agility=2, race='demon', death_function=monster_death)
                    ai_component = BasicMonster()

                    monster = Entity(x, y, 'i', 'imp', libtcod.darker_red, blocks=True, fighter=fighter_component,
                                     ai=ai_component)

                elif choice == 'devil':
                    # create a troll
                    fighter_component = Fighter(xp=40, hp_stat=40, mp_stat=0, constitution=4, strength=8, dexterity=4,
                                                intelligence=0, wisdom=0,
                                                agility=1, race='demon', death_function=monster_death)
                    ai_component = BasicMonster()

                    monster = Entity(x, y, 'd', 'devil', libtcod.darker_red, blocks=True, fighter=fighter_component,
                                     ai=ai_component)

                elif choice == 'demon conjurer':
                    # create an orc
                    fighter_component = Fighter(xp=30, hp_stat=20, mp_stat=30, constitution=2, strength=1, dexterity=2,
                                                intelligence=3, wisdom=3,
                                                agility=1, race='demon', death_function=monster_death)
                    ai_component = MageBasicMonster()

                    monster = Entity(x, y, 'c', 'demon conjurer', libtcod.darker_red, blocks=True,
                                     fighter=fighter_component,
                                     ai=ai_component)
                elif choice == 'demon archer':
                    # create an orc
                    fighter_component = Fighter(xp=30, hp_stat=20, mp_stat=30, constitution=2, strength=3, dexterity=2,
                                                intelligence=1,
                                                wisdom=3,
                                                agility=1, race='demon', death_function=monster_death)
                    ai_component = RangedBasicMonster()

                    monster = Entity(x, y, 'a', 'demon archer', libtcod.darker_red, blocks=True,
                                     fighter=fighter_component,
                                     ai=ai_component)


                elif choice == 'archdemon':
                    # create an orc
                    fighter_component = Fighter(xp=60, hp_stat=80, mp_stat=0, constitution=8, strength=16, dexterity=5,
                                                intelligence=0, wisdom=0,
                                                agility=1, race='demon', death_function=monster_death)
                    ai_component = BasicMonster()

                    monster = Entity(x, y, 'A', 'archdemon', libtcod.darker_red, blocks=True, fighter=fighter_component,
                                     ai=ai_component)

            ########################################################################################################################
            #   Skeletons
            ########################################################################################################################
            if set == 'skeletons':
                if choice == 'skeleton':
                    # create an orc
                    fighter_component = Fighter(xp=20, hp_stat=20, mp_stat=0, constitution=2, strength=4, dexterity=0,
                                                intelligence=0, wisdom=0,
                                                agility=2, race='skeleton', death_function=monster_death)
                    ai_component = BasicMonster()

                    monster = Entity(x, y, 's', 'skeleton', libtcod.white, blocks=True, fighter=fighter_component,
                                     ai=ai_component)

                elif choice == 'skeletal warrior':
                    # create a troll
                    fighter_component = Fighter(xp=40, hp_stat=40, mp_stat=0, constitution=4, strength=8, dexterity=4,
                                                intelligence=0, wisdom=0,
                                                agility=1, race='skeleton', death_function=monster_death)
                    ai_component = BasicMonster()

                    monster = Entity(x, y, 'w', 'skeletal warrior', libtcod.white, blocks=True,
                                     fighter=fighter_component,
                                     ai=ai_component)

                elif choice == 'skeleton necromancer':
                    # create an orc
                    fighter_component = Fighter(xp=30, hp_stat=20, mp_stat=30, constitution=2, strength=1, dexterity=2,
                                                intelligence=3, wisdom=3,
                                                agility=1, race='skeleton', death_function=monster_death)
                    ai_component = MageBasicMonster()

                    monster = Entity(x, y, 'n', 'skeleton necromancer', libtcod.white, blocks=True,
                                     fighter=fighter_component,
                                     ai=ai_component)

                elif choice == 'skeleton archer':
                    # create an orc
                    fighter_component = Fighter(xp=30, hp_stat=20, mp_stat=30, constitution=2, strength=3, dexterity=2,
                                                intelligence=1,
                                                wisdom=3,
                                                agility=1, race='skeleton', death_function=monster_death)
                    ai_component = RangedBasicMonster()

                    monster = Entity(x, y, 'a', 'skeleton archer', libtcod.white, blocks=True,
                                     fighter=fighter_component,
                                     ai=ai_component)

                elif choice == 'skeleton lord':
                    # create an orc
                    fighter_component = Fighter(xp=60, hp_stat=80, mp_stat=0, constitution=8, strength=16, dexterity=5,
                                                intelligence=0, wisdom=0,
                                                agility=1, race='skeleton', death_function=monster_death)
                    ai_component = BasicMonster()

                    monster = Entity(x, y, 'S', 'skeleton lord', libtcod.white, blocks=True, fighter=fighter_component,
                                     ai=ai_component)



            if monster is None:
                i -= 1
                continue
            entities.append(monster)

    num_items = libtcod.random_get_int(0, 0, max_items)

    for i in range(num_items):
        # choose rand spot for item
        x = libtcod.random_get_int(0, room.x1 + 1, room.x2 - 1)
        y = libtcod.random_get_int(0, room.y1 + 1, room.y2 - 1)

        # place if tile  not blocked
        if not is_blocked(x, y):
            choice = random_choice(item_chances)

            if choice == 'heal':
                # create potion
                item = Entity(x, y, '!', 'healing potion', libtcod.violet, potion=potion_heal_component)

            elif choice == 'lightning':

                item = Entity(x, y, '#', 'Scroll of Lightning', libtcod.light_yellow, scroll=scroll_of_lightning)

            elif choice == 'fireburst':

                item = Entity(x, y, '#', 'Scroll of Fireburst', libtcod.light_yellow, scroll=scroll_of_fireburst)

            elif choice == 'confuse':
                item = Entity(x, y, '#', 'Croll of Sonfusion', libtcod.light_yellow, scroll=croll_of_sonfusion)

            elif choice == 'force tome':

                item = Entity(x, y, '#', 'Tome of Force', libtcod.brass, scroll=force_tome)

            elif choice == 'long sword':
                # create a sword

                item = Entity(x, y, '/', 'long sword', libtcod.black, equipment=equipment_long_sword)

            elif choice == 'shield':
                # create a shield

                item = Entity(x, y, '[', 'shield', libtcod.darker_orange, equipment=equipment_shield)


            entities.append(item)
            item.always_visible = True  # items are visible even out-of-FOV, if in an explored area
            item.send_to_back()  # items appear below other entities

            #entities.remove(item)


def create_door(x, y, orientation):
    place_door = libtcod.random_get_int(0, 0, 3)
    # TODO make some doors locked, add keys, allow breaking doors
    # lock_door = libtcod.random_get_int(0, 0, 3)

    if place_door == 0:
        if orientation == 'vertical':
            door = Entity(x, y, '|', 'door', libtcod.black, locked=False, blocks=True)
            if (map[x][y - 1].blocked == True and map[x][y + 1].blocked == True):
                entities.append(door)
        else:
            door = Entity(x, y, '_', 'door', libtcod.black, locked=False, blocks=True)
            if (map[x - 1][y].blocked == True and map[x + 1][y].blocked == True):
                entities.append(door)

                # if lock_door == 0:
                #     door.locked = True


def set_monster_squad():
    # randomly choose monster set for floor
    monster_sets = {}

    monster_sets['goblins'] = 50
    monster_sets['orcs'] = 50
    monster_sets['skeletons'] = 50
    monster_sets['demons'] = 50
    monster_sets['slimes'] = 50
    return random_choice(monster_sets)


def render_all():
    global fov_map, color_dark_wall, color_light_wall
    global color_dark_ground, color_light_ground
    global fov_recompute
    global dungeon_level, turn_count

    if fov_recompute:
        # recompute FOV if needed (the player moved or something)
        fov_recompute = False
        libtcod.map_compute_fov(fov_map, player.x, player.y, SIGHT_RANGE, FOV_LIGHT_WALLS, FOV_ALGO)

        # go through all tiles, and set their background color according to the FOV
        for y in range(MAP_HEIGHT):
            for x in range(MAP_WIDTH):
                visible = libtcod.map_is_in_fov(fov_map, x, y)
                wall = map[x][y].block_sight
                if not visible:
                    # if it's not visible right now, the player can only see it if it's explored
                    if map[x][y].explored:
                        if wall:
                            libtcod.console_set_char_background(con, x, y, color_dark_wall, libtcod.BKGND_SET)
                        else:
                            libtcod.console_set_char_background(con, x, y, color_dark_ground, libtcod.BKGND_SET)
                else:
                    # it's visible
                    if wall:
                        libtcod.console_set_char_background(con, x, y, color_light_wall, libtcod.BKGND_SET)
                    else:
                        libtcod.console_set_char_background(con, x, y, color_light_ground, libtcod.BKGND_SET)
                    # since it's visible, explore it
                    map[x][y].explored = True

                    # draw all entities in the list
    for entity in entities:
        if entity != player:
            entity.draw()
    player.draw()

        # blit the contents of "con" to the root console

    libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)

    # prepare to render the GUI panel
    libtcod.console_set_default_background(panel, libtcod.black)
    libtcod.console_clear(panel)

    # print the game messages, one line at a time
    y = 1
    for (line, color) in game_msgs:
        libtcod.console_set_default_foreground(panel, color)
        libtcod.console_print_ex(panel, MSG_X, y, libtcod.BKGND_NONE, libtcod.LEFT, line)
        y += 1

    # show the player's stats
    render_bar(1, 1, BAR_WIDTH, 'HP', player.fighter.hp, player.fighter.max_hp,
               libtcod.light_red, libtcod.darker_red, libtcod.white)

    render_bar(1, 2, BAR_WIDTH, 'Mana', player.fighter.mp, player.fighter.max_mp,
               libtcod.light_blue, libtcod.darker_blue, libtcod.white)

    render_bar(1, 3, BAR_WIDTH, 'EXP', player.fighter.xp, LEVEL_UP_BASE + player.level * LEVEL_UP_FACTOR,
               libtcod.desaturated_green, libtcod.darker_green, libtcod.white)

    render_bar(1, 4, BAR_WIDTH, 'Satiation', player.fighter.nutrition/10, 100,
               libtcod.desaturated_orange, libtcod.dark_orange, libtcod.white)



    libtcod.console_print_ex(panel, 1, 5, libtcod.BKGND_NONE, libtcod.LEFT, 'Floor ' + str(dungeon_level))
    libtcod.console_print_ex(panel, 1, 6, libtcod.BKGND_NONE, libtcod.LEFT, 'Turn ' + str(turn_count))

    # display names of entities under the mouse
    libtcod.console_set_default_foreground(panel, libtcod.light_gray)
    libtcod.console_print_ex(panel, 1, 0, libtcod.BKGND_NONE, libtcod.LEFT, get_names_under_mouse())

    # blit the contents of "panel" to the root console
    libtcod.console_blit(panel, 0, 0, SCREEN_WIDTH, PANEL_HEIGHT, 0, 0, PANEL_Y)


def random_choice(chances_dict):
    # choose one option from dictionary of chances, returning its key
    chances = chances_dict.values()
    strings = chances_dict.keys()

    return strings[random_choice_index(chances)]


def random_choice_index(chances):  # choose one option from list of chances, returning its index
    # the dice will land on some number between 1 and the sum of the chances
    dice = libtcod.random_get_int(0, 1, sum(chances))

    # go through all chances, keeping the sum so far
    running_sum = 0
    choice = 0
    for w in chances:
        running_sum += w

        # see if the dice landed in the part that corresponds to this choice
        if dice <= running_sum:
            return choice
        choice += 1


def from_dungeon_level(table):
    # returns a value that depends on level. the table specifies what value occurs after each level, default is 0.
    for (value, level) in reversed(table):
        if dungeon_level >= level:
            return value
    return 0


########################################################################################################################
#   Game Management
########################################################################################################################

def play_game():
    global key, mouse

    player_action = None

    mouse = libtcod.Mouse()
    key = libtcod.Key()

    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)
        render_all()


        libtcod.console_flush()

        check_level_up()
        update_stats(player)

        # erase all entities at their old locations, before they move
        for entity in entities:
            entity.clear()

        player_action = controls()

        if player_action == 'exit':
            save_game()
            break

        if game_state == 'alive' and player_action != 'didnt-take-turn':
            check_effects()
            for entity in entities:
                entity.clear()
                if entity.ai:
                    entity.ai.take_turn()


def new_game():
    global player, inventory, keybinds, game_msgs, game_state, dungeon_level, turn_count
    # the inventory
    inventory = []

    # create the list of game messages and their colors, starts empty


    game_msgs = []

    keybinds = {}

    character_creation()

    dungeon_level = 1
    turn_count = 0
    # generate map (at this point it's not drawn to the screen)
    if BSP:
        make_bsp()
    else:
        make_map()

    initialize_fov()

    game_state = 'alive'

    # a warm welcoming message!
    message('Welcome to the dungeon, ' + player.name + '!', libtcod.dark_yellow)
    message('You are a ' + player.fighter.gender + ' ' + player.fighter.race + ' ' + player.fighter.job + '.', libtcod.yellow)
    message('Your quest is to defeat the demon lord on floor 50.', libtcod.light_red)
    message('Good Luck!', libtcod.light_green)
    message("Press '?' for a handy list of commands.",
            libtcod.light_pink)

#TODO update the save and load functions to include EVERY variable
def save_game():
    # open a new empty shelve (possibly overwriting an old one) to write the game data
    file = shelve.open('savegame', 'n')
    file['map'] = map
    file['entities'] = entities
    file['player_index'] = entities.index(player)  # index of player in entities list
    file['inventory'] = inventory
    file['game_msgs'] = game_msgs
    file['game_state'] = game_state
    file['stairs_index'] = entities.index(stairs)
    file['dungeon_level'] = dungeon_level
    file['turn_count'] = turn_count
    file.close()


def load_game():
    # open the previously saved shelve and load the game data
    global map, entities, player, inventory, game_msgs, game_state

    file = shelve.open('savegame', 'r')
    map = file['map']
    entities = file['entities']
    player = entities[file['player_index']]  # get index of player in entities list and access it
    inventory = file['inventory']

    game_msgs = file['game_msgs']
    game_state = file['game_state']
    file.close()

    initialize_fov()


########################################################################################################################
#   Player Management
########################################################################################################################

def next_floor():
    global dungeon_level, monster_set, detect_item
    # advance to the next level
    message('You take a moment to rest, and recover your power.', libtcod.light_violet)
    player.fighter.heal(player.fighter.max_hp / 2)  # heal the player by 50%

    message('After a rare moment of peace, you descend deeper into the heart of the dungeon...', libtcod.red)

    dungeon_level += 1

    detect_item = False
    for entity in entities:
        if entity.item:
            entity.telepathy_visible = False

    detect_monster = False
    detect_monster_dur = 0
    for entity in entities:
        if entity.fighter:
            entity.telepathy_visible = False

    if BSP:
        make_bsp()
    else:
        make_map()
    initialize_fov()


def check_level_up():
    # see if the player's experience is enough to level-up
    level_up_xp = LEVEL_UP_BASE + player.level * LEVEL_UP_FACTOR
    if player.fighter.xp >= level_up_xp:
        # level up
        player.level += 1
        player.fighter.xp -= level_up_xp
        message('You reached level ' + str(player.level) + '!', libtcod.yellow)
        x = libtcod.random_get_int(0, player.fighter.growths[1], player.fighter.growths[2]) + int(player.fighter.constitution / 5.5)
        y = libtcod.random_get_int(0, player.fighter.growths[4], player.fighter.growths[5]) + int(player.fighter.wisdom / 5.5)
        player.fighter.max_hp += x
        player.fighter.max_mp += y
        player.fighter.hp += x
        player.fighter.mp += y

def get_equipped_in_slot(slotList):  # returns equipment in slot, or None if empty

    for ent in inventory:
        for i in slotList:

                if ent.equipment and ent.equipment.is_equipped and i in ent.equipment.slot:

                    return ent.equipment

    return None


def get_all_equipped(ent):  # returns a list of equipped items
    if ent == player:
        equipped_list = []
        for item in inventory:
            if item.equipment and item.equipment.is_equipped:
                equipped_list.append(item.equipment)
        return equipped_list
    else:
        return []  # other entities have no equipment


def controls():
    global key, turn_count

    if key.vk == libtcod.KEY_ENTER and key.lalt:
        # Alt+Enter: toggle fullscreen
        libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())
    if DEBUG_CONTROLS:
        if key.vk == libtcod.KEY_F1:
            #go to level 100
            player.fighter.xp += 762300


    elif key.vk == libtcod.KEY_ESCAPE:
        return 'exit'  # exit game

    if game_state == 'alive':
        # movement keys

        if key.vk == libtcod.KEY_HOME or key.vk == libtcod.KEY_KP7:
            player_move_or_attack(-1, -1)

        elif key.vk == libtcod.KEY_PAGEUP or key.vk == libtcod.KEY_KP9:
            player_move_or_attack(1, -1)

        elif key.vk == libtcod.KEY_END or key.vk == libtcod.KEY_KP1:
            player_move_or_attack(-1, 1)

        elif key.vk == libtcod.KEY_PAGEDOWN or key.vk == libtcod.KEY_KP3:
            player_move_or_attack(1, 1)

        elif key.vk == libtcod.KEY_UP or key.vk == libtcod.KEY_KP8:
            player_move_or_attack(0, -1)

        elif key.vk == libtcod.KEY_DOWN or key.vk == libtcod.KEY_KP2:
            player_move_or_attack(0, 1)

        elif key.vk == libtcod.KEY_LEFT or key.vk == libtcod.KEY_KP4:
            player_move_or_attack(-1, 0)

        elif key.vk == libtcod.KEY_RIGHT or key.vk == libtcod.KEY_KP6:
            player_move_or_attack(1, 0)

        elif key.vk == libtcod.KEY_KP5:
            pass  # do nothing ie wait for the monster to come to you



        elif key.vk == libtcod.KEY_1:
            if libtcod.KEY_1 in keybinds:
                keybinds[libtcod.KEY_1].cast()

        elif key.vk == libtcod.KEY_2:
            if libtcod.KEY_2 in keybinds:
                keybinds[libtcod.KEY_2].cast()

        elif key.vk == libtcod.KEY_3:
            if libtcod.KEY_3 in keybinds:
                keybinds[libtcod.KEY_3].cast()

        elif key.vk == libtcod.KEY_4:
            if libtcod.KEY_4 in keybinds:
                keybinds[libtcod.KEY_4].cast()

        elif key.vk == libtcod.KEY_5:
            if libtcod.KEY_5 in keybinds:
                keybinds[libtcod.KEY_5].cast()



        else:
            # test for keys
            key_char = chr(key.c)

            if key_char == 'g':
                # pick up item

                for entity in entities:

                    if entity.x == player.x and entity.y == player.y and entity.item:

                        entity.item.pick_up()
                        break
                return





            if key_char == 'i':
                # show the inventory; if an item is selected, use it
                chosen_item = inventory_menu('Press the key next to an item to use it, or any other to cancel.\n')
                if chosen_item is not None:
                    chosen_item.use()
                return

            if key_char == 's':
                # show the skill menu
                chosen_skill = skill_menu('Press the key next to an item to use it, or any other to cancel.\n')
                if chosen_skill is not None:
                    chosen_skill.cast()
                return

            if key_char == 'f':
                # show the skill menu
                fav_menu("Select skill to bind with a-z, then input key to bind with numbers 1-5 on top bar.\n")
                return


            if key_char == 'd':
                # show the inventory; if an item is selected, drop it
                chosen_item = inventory_menu('Press the key next to an item to drop it, or any other to cancel.\n')
                if chosen_item is not None:
                    chosen_item.drop()
                return

            if key_char == '<':
                # go down stairs, if the player is on them
                if stairs.x == player.x and stairs.y == player.y:
                    next_floor()

            if key_char == '?':
                # open help menu
                help_string = ""
                for cntrl, desc in controls_dict.items():
                    help_string += cntrl + ": " + desc + "\n"
                msgbox(help_string)
                libtcod.console_wait_for_keypress(True)

            if key_char == 'c':
                # show character information
                level_up_xp = LEVEL_UP_BASE + player.level * LEVEL_UP_FACTOR
                msgbox(
                    'Character Information\n\n' + player.name.capitalize() + ' the ' + player.fighter.race.capitalize() + ' ' + player.fighter.job.capitalize() + '\n\nLevel: ' + str(
                        player.level) + '\nExperience: ' + str(
                        player.fighter.xp) +
                    '\nExperience to level up: ' + str(level_up_xp) + '\n\nMaximum HP: ' + str(
                        player.fighter.max_hp) + '\nMaximum MP: ' + str(player.fighter.max_mp) +
                    '\nAttack: ' + str(player.fighter.power) + '\nDefense: ' + str(
                        player.fighter.defense) + '\nMagic: ' + str(player.fighter.magic) + '\nCritical Chance: ' + str(
                        player.fighter.agility) +
                    '\n\nConstitution: ' + str(player.fighter.constitution) +
                    '\nStrength: ' + str(player.fighter.strength) +
                    '\nEndurance: ' + str(player.fighter.dexterity) +
                    '\nIntelligence: ' + str(player.fighter.intelligence) +
                    '\nWisdom: ' + str(player.fighter.wisdom) +
                    '\nAgility: ' + str(player.fighter.agility),
                    CHARACTER_SCREEN_WIDTH)

            return 'didnt-take-turn'

        turn_count += 1
        if turn_count % 10 == 0 and player.fighter.max_hp != player.fighter.hp:
            player.fighter.hp += 1

        if turn_count % 10 == 0 and player.fighter.max_mp != player.fighter.mp:
            player.fighter.mp += 1
        if turn_count % 1 == 0:
            if player.fighter.nutrition > 0:
                player.fighter.nutrition -= 1
            else:
                player.fighter.hp -= 1


def player_move_or_attack(dx, dy):
    global fov_recompute

    # the coordinates the player is moving to/attacking
    x = player.x + dx
    y = player.y + dy

    # try to find an attackable entity there
    target = None
    for entity in entities:
        if entity.fighter and entity.x == x and entity.y == y:
            target = entity
            break
        if entity.name == 'door' and entity.x == x and entity.y == y:
            open_door(entity)
            target = entity
            break
    # attack if target found, move otherwise
    if target is not None:
        if target.name == 'door':

            pass
        else:
            player.fighter.attack(target)

    else:
        player.move(dx, dy)
        fov_recompute = True


def open_door(door):
    global entities
    if door.locked == True:
        message('The door is locked.', libtcod.red)
    else:
        entities.remove(door)


def player_death(player):
    # the game ended!
    global game_state
    message('You died!', libtcod.red)
    game_state = 'dead'

    # for added effect, transform the player into a corpse!
    player.char = '%'
    player.color = libtcod.dark_red


def update_stats(ent):
    ent.fighter.base_max_hp = ent.fighter.hp_stat
    # ent.fighter.hp = ent.fighter.hp_stat
    ent.fighter.base_max_mp = ent.fighter.mp_stat
    # ent.fighter.mp = ent.fighter.mp_stat



########################################################################################################################
#   Combat and Monster Management
########################################################################################################################


def is_blocked(x, y):
    # first test the map tile
    if map[x][y].blocked:
        return True

    # now check for any blocking entities
    for entity in entities:
        if entity.blocks and entity.x == x and entity.y == y:
            return True

    return False


def monster_death(monster):
    # transform it into a nasty corpse! it doesn't block, can't be
    # attacked and doesn't move
    message('The ' + monster.name + ' is dead! You gain ' + str(monster.fighter.xp) + ' experience points.',
            libtcod.orange)
    monster.char = '%'
    monster.color = libtcod.dark_red
    monster.blocks = False
    monster.fighter = None
    monster.ai = None
    monster.name = 'remains of ' + monster.name
    monster.send_to_back()


def closest_monster(max_range):
    # closest enemy in range
    closest_enemy = None
    closest_dist = max_range + 1  # start w/ max range + 1

    for entity in entities:
        if entity.fighter and not entity == player and libtcod.map_is_in_fov(fov_map, entity.x, entity.y):
            # calc dist btwn player and entity
            dist = player.distance_to(entity)
            if dist < closest_dist:
                closest_enemy = entity
                closest_dist = dist
    return closest_enemy


def player_target(max_range, caster):
    closest_enemy = None
    closest_dist = max_range + 1  # start w/ max range + 1

    for entity in entities:
        if entity.fighter and entity == player and libtcod.map_is_in_fov(fov_map, entity.x, entity.y):
            # calc dist btwn player and monster
            dist = caster.distance_to(entity)
            if dist < closest_dist:
                closest_enemy = entity
                closest_dist = dist
    return closest_enemy


def target_tile(max_range=None):
    global key, mouse
    while True:
        libtcod.console_flush()
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)
        render_all()

        (x, y) = (mouse.cx, mouse.cy)

        # accept the target if the player clicked in FOV, and in case a range is specified, if it's in that range
        if (mouse.lbutton_pressed and libtcod.map_is_in_fov(fov_map, x, y) and (
                max_range is None or player.distance(x, y) <= max_range)):
            return (x, y)
        if mouse.rbutton_pressed or key.vk == libtcod.KEY_ESCAPE:
            return (None, None)  # cancel if the player right-clicked or pressed Escape


def target_monster(max_range=None):
    # returns a clicked monster inside range
    while True:
        (x, y) = target_tile(max_range)
        if x is None:  # player cancelled
            return None

        # return the first clicked monster, otherwise continue looping
        for ent in entities:
            if ent.x == x and ent.y == y and ent.fighter and ent != player:
                return ent


def choose_dir(diagonal=True):
    global key, mouse
    while True:
        libtcod.console_flush()
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, key, mouse)
        render_all()

        if key.vk == libtcod.KEY_UP or key.vk == libtcod.KEY_KP8:
            return (0, -1)

        if key.vk == libtcod.KEY_DOWN or key.vk == libtcod.KEY_KP2:
            return (0, 1)

        if key.vk == libtcod.KEY_LEFT or key.vk == libtcod.KEY_KP4:
            return (-1, 0)

        if key.vk == libtcod.KEY_RIGHT or key.vk == libtcod.KEY_KP6:
            return (1, 0)
        if diagonal == True:
            if key.vk == libtcod.KEY_HOME or key.vk == libtcod.KEY_KP7:
                return (-1, -1)

            if key.vk == libtcod.KEY_PAGEUP or key.vk == libtcod.KEY_KP9:
                return (1, -1)

            if key.vk == libtcod.KEY_END or key.vk == libtcod.KEY_KP1:
                return (-1, 1)

            if key.vk == libtcod.KEY_PAGEDOWN or key.vk == libtcod.KEY_KP3:
                return (1, 1)

        if key.vk == libtcod.KEY_ESCAPE:
            return (0, 0)


def range_attack(attack_range, pierce=False, ignore_walls=False, dx=None, dy=None, getDir = False):
    if (dx == None and dy == None):
        (x, y) = choose_dir()
    else:
        (x, y) = (dx, dy)

    target_list = []

    for i in range(attack_range):
        for ent in entities:
            if ent.x == x + player.x and ent.y == y + player.y and ent.fighter and ent != player:
                target_list.append(ent)
                if not pierce:
                    break
        if map[x + player.x][y + player.y].blocked and not ignore_walls:
            break

        if x > 0:
            x += 1
        elif x < 0:
            x -= 1

        if y > 0:
            y += 1
        elif y < 0:
            y -= 1
    if getDir:
        return target_list, (x,y)
    return target_list


def check_for_collision_in_line(dist, direction):
    (x, y) = direction

    for i in range(dist):
        if map[x+player.x][y+player.y].blocked == True:
            if y < 0:
                y += 1
            elif y > 0:
                y -= 1
            if x < 0:
                x += 1
            elif x > 0:
                x -= 1
            return (x+player.x, y+player.y)
        else:
            if y < 0:
                y -= 1
            elif y > 0:
                y += 1
            if x < 0:
                x -= 1
            elif x > 0:
                x += 1


########################################################################################################################
#   Spells and Item Effects
########################################################################################################################

#Can add skills to player or monster
def teach_skill(spell, student):
    if len(student.fighter.skills) >= 26:
        message('Too many skills, cannot learn ' + self.owner.name + '.', libtcod.red)
    for skill in student.fighter.skills:
        if spell == skill.name:
            message('You already know ' + skill.name + '.', libtcod.red)
    else:
        if spell == 'fireburst':
            fireburst = Skill('fireburst', cast_function=cast_fireburst, cost=5, school='sorcery')
            student.fighter.skills.append(fireburst)

        if spell == 'force':
            force = Skill('force', cast_function=cast_force, cost=2, school='sorcery')
            student.fighter.skills.append(force)

        if spell == 'barrier':
            barrier = Skill('barrier', cast_function=cast_barrier, cost=8, school='abjuration')
            student.fighter.skills.append(barrier)

        if spell == 'heal':
            heal = Skill('heal', cast_function=cast_heal, cost=20, school='miracles')
            student.fighter.skills.append(heal)

        if spell == 'confusion':
            heal = Skill('confusion', cast_function=cast_confuse, cost=10, school='enchantment')
            student.fighter.skills.append(confuse)

        if spell == 'detect monster':
            detect_monster = Skill('detect monster', cast_function=cast_detect_monster, cost=10, school='divination')
            student.fighter.skills.append(detect_monster)

        if spell == 'shield bash':
            shield_bash = Skill('shield bash', cast_function=cast_shield_bash, cost=10, school='weapon art')
            student.fighter.skills.append(shield_bash)

        if spell == 'throw weapon':
            throw_weapon = Skill('throw weapon', cast_function=cast_throw_weapon, cost=0, school='weapon art')
            student.fighter.skills.append(throw_weapon)


def consume_potion(effect, magnitude, duration):
    if effect == 'heal':
        cast_heal(player, magnitude)
    if effect == 'food':
        cast_eat(player, magnitude)
    if effect == 'detect_monster':
        cast_detect_monster(caster, duration)


def cast_eat(caster, amt=None):
    # heals player
    if caster.fighter.nutrition == 1000:
        message("You can't eat any more.", libtcod.red)
        return 'cancelled'

    caster.fighter.nutrition += amt

    if caster.fighter.nutrition <= 200:
        message('You are still starving.', libtcod.light_violet)
    elif caster.fighter.nutrition <= 400:
        message('You are still feeling hungry.', libtcod.light_violet)
    elif caster.fighter.nutrition <= 600:
        message('You feel are still feeling peckish.', libtcod.light_violet)
    elif caster.fighter.nutrition <= 800:
        message('You feel content.', libtcod.light_violet)
    elif caster.fighter.nutrition <= 1000:
        message('You feel full.', libtcod.light_violet)
    elif caster.fighter.nutrition > 1000:
        message('You are completely full.', libtcod.light_violet)
        caster.fighter.nutrition = 1000


def cast_heal(caster, amt=None):
    # restores health by 1/3 if no amt specified
    if amt == None:
        amt = caster.fighter.hp / 3
    if caster.fighter.hp == caster.fighter.max_hp:
        message('Your health is already full.', libtcod.red)
        return 'cancelled'

    message('You are healed for ' + str(amt), libtcod.light_violet)
    caster.fighter.heal(amt)

lighting_range = 5
#example for random target attack
def cast_lightning(caster):
    # find nearest enemy and zap them
    if (caster == player):
        monster = closest_monster(lighting_range)
    else:
        monster = player_target(lightning_range, caster)
    if monster is None:  # no enemy found within maximum range
        message('No enemy is close enough to strike.', libtcod.red)
        return 'cancelled'
    (damage, critical) = mag_attack_formula(self, target)
    message('A lighting bolt strikes the ' + monster.name + ' for '
            + str(damage) + '  damage.', libtcod.light_blue)
    monster.fighter.take_damage(damage)

confuse_range = 8
#example for mouse targeted attack
def cast_confuse(caster):
    # ask the player for a target to confuse
    if caster == player:
        message('Left-click an enemy to confuse it, or right-click to cancel.', libtcod.light_cyan)
        monster = target_monster(confuse_range)
    else:
        monster = player_target(confuse_range, caster)
    if monster is None: return 'cancelled'

    # replace the monster's AI with a "confused" one; after some turns it will restore the old AI
    apply_confused(monster)

fireburst_radius = 3
#example for area attack
def cast_fireburst(caster):
    # ask player for target
    (x, y) = (caster.x, caster.y)
    if x is None: return 'cancelled'
    message('The fireburst explodes!', libtcod.orange)

    for ent in entities:
        if ent.fighter:
            if hit_formula(caster, ent):
                (damage, critical) = mag_attack_formula(caster, ent)
                if ent.distance(x, y) <= fireburst_radius and ent != player:
                    message('The ' + ent.name + ' gets burned for ' + str(damage) + ' damage.', libtcod.orange)
                    ent.fighter.take_damage(damage)
            else:
                message('You miss!')

force_base = 2
force_range = 2
#example magic attack
def cast_force(caster):
    if caster == player:
        message('Pick a direction using the numpad or arrow keys. Range: 2', libtcod.light_cyan)
        monster_list = range_attack(force_range)
    else:
        monster_list = [player]
    if monster_list is None: return 'cancelled'
    for i in range(len(monster_list)):
        target = monster_list[i]
        if hit_formula(caster,target):
            (damage, critical) = mag_attack_formula(caster, target)


            if (critical):

                message('The ' + target.name + ' is critically hit with a blast of energy for ' + str(damage) + ' damage!',libtcod.orange)
                target.fighter.take_damage(damage)
            else:

                message('The ' + target.name + ' is hit with a blast of energy for ' + str(damage) + ' damage.', libtcod.orange)
                target.fighter.take_damage(damage)

        else:
            message('You miss!')


barrier = False
barrier_dur = 15


def cast_barrier(caster):
    global barrier

    if not barrier:
        message(caster.name + " is now surrounded by a magical shield. Their defense increases by 2",
                libtcod.light_cyan)
        caster.fighter.defense += 2
        barrier = True
        barrier_dur = 15


    elif barrier:
        message("The magical shield around " + caster.name + " disappears.", libtcod.light_cyan)
        caster.fighter.defense -= 2
        barrier = False
        barrier_dur = 0


detect_monster = False
detect_monster_dur = 100


def cast_detect_monster(caster, duration = 100):
    global detect_monster
    if not detect_monster:
        message("The monsters in the dungeon become visible", libtcod.light_cyan)
        for entity in entities:
            if entity.fighter:
                entity.telepathy_visible = True

        detect_monster = True
        detect_monster_dur = duration

    else:
        message("The monsters in the dungeon are no longer visible!", libtcod.light_cyan)
        detect_monster = False
        detect_monster_dur = 0
        for entity in entities:
            if entity.fighter:
                entity.telepathy_visible = False


detect_item = False


def cast_detect_item(caster, nextfloor = False):
    global detect_item
    if not detect_item:
        message("The items in the dungeon become visible", libtcod.light_cyan)
        for entity in entities:
            if entity.item:
                entity.telepathy_visible = True

        detect_item = True

    else:
        detect_item = False
        for entity in entities:
            if entity.item:
                entity.telepathy_visible = False


def cast_shield_bash(caster):
    if caster == player:
        message('Pick a direction using the numpad or arrow keys. Range: 1', libtcod.light_cyan)
        monster_list = range_attack(1)
    else:
        monster_list = [player]
    if monster_list is None: return 'cancelled'
    for i in range(len(monster_list)):
        target = monster_list[i]

        if hit_formula(caster, target):
            (damage, critical) = attack_formula(caster, target)

            if (critical == True):

                message('You bash the ' + target.name + ' with your shield on a weak point, dealing ' + str(damage) + ' damage!', libtcod.orange)
                target.fighter.take_damage(damage)
            else:

                message('You bash the ' + target.name + ' with your shield, dealing ' + str(damage) + ' damage.', libtcod.orange)
                target.fighter.take_damage(damage)

            apply_dazed(target)
        else:
            message('You miss!', libtcod.orange)


def cast_throw_weapon(caster):

    for ent in inventory:
        if ent.ranged:
            if ent.ranged.ready == True:

                use_throwing_weapon(caster, ent.item)
                return

    message('You have no weapon readied', libtcod.red)


def use_throwing_weapon(caster, weapon):
    global entities
    if caster == player:

        message('Pick a direction using the numpad or arrow keys. Range: ' + str(weapon.owner.ranged.range),
                libtcod.light_cyan)
        (monster_list, direction) = range_attack(weapon.owner.ranged.range, getDir= True)
    else:
        monster_list = [player]
    if monster_list is None: return 'cancelled'
    target = None
    for i in range(len(monster_list)):
        target = monster_list[i]
        (damage, crit) = attack_formula_throwing(caster, target, weapon)

        if (crit):
            message(
                caster.name.capitalize() + ' throws a ' + weapon.owner.name + ' at the ' + target.name + ' for ' + str(
                    damage - target.fighter.defense) + ' damage! A critical hit!', libtcod.orange)
            target.fighter.take_damage(damage - target.fighter.defense)
        else:
            message(
                caster.name.capitalize() + ' throws a ' + weapon.owner.name + 'at the ' + target.name + ' for ' + str(
                    damage - target.fighter.defense) + ' damage!', libtcod.orange)
            target.fighter.take_damage(damage - target.fighter.defense)



    if weapon.amt == 1:
        inventory.remove(weapon.owner)  # consume item if consumable
    else:
        weapon.amt -= 1

    ranged_component = RangedWeapon(0, damage=weapon.owner.ranged.damage, effect=weapon.owner.ranged.effect, range=weapon.owner.ranged.range)
    ent = Entity(0, 0, "-", weapon.owner.name, libtcod.grey, ranged=ranged_component)
    ent.amt = 1

    entities.append(ent)
    ent.send_to_back()  # items appear below other entities
    ent.always_visible = True  # items are visible even out-of-FOV, if in an explored area
    if target is None:
        (xval, yval) = check_for_collision_in_line(weapon.owner.ranged.range, direction)
        ent.x = xval
        ent.y = yval
    else:
        ent.x = target.x
        ent.y = target.y


def apply_dazed(target, duration = 2):

    if target != player and 'dazed' not in target.fighter.effects:
        old_ai = target.ai
        target.ai = DazedMonster(old_ai, num_turns=duration)
        target.ai.owner = target  # tell the new component who owns it
        message(target.name + ' is dazed!')

        target.fighter.effects.append('dazed')

    elif 'dazed' not in target.fighter.effects:
        player.fighter.effects.append('dazed')
    else:
        message(target + ' is already dazed!')


def apply_confused(target, duration = 5):
    if target != player:
        # replace the target's AI with a "confused" one; after some turns it will restore the old AI
        old_ai = target.ai
        target.ai = ConfusedMonster(old_ai, num_turns=duration)
        target.ai.owner = target  # tell the new component who owns it
        message(target.name + ' becomes confused!')
        target.fighter.effects.append('confused')
    else:
        player.fighter.effects.append('confused')


#updates effects over many turns
def check_effects():
    global turn_count

    global barrier, barrier_dur, detect_monster, detect_monster_dur
    if barrier == True:
        barrier_dur -= 1
        if barrier_dur == 0:
            cast_barrier(player)

    if detect_monster == True:
        detect_monster_dur -= 1
        if detect_monster_dur == 0:
            cast_detect_monster(player)



########################################################################################################################
#   GUI
########################################################################################################################

def main_menu():
    img = libtcod.image_load(MENU_BG)

    while not libtcod.console_is_window_closed():
        libtcod.image_blit_2x(img, 0, 0, 0)
        # show the game's title, and some credits!
        libtcod.console_set_default_foreground(0, libtcod.light_yellow)
        libtcod.console_print_ex(0, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 4, libtcod.BKGND_NONE, libtcod.CENTER,
                                 "Dungeon Crawler")
        libtcod.console_print_ex(0, SCREEN_WIDTH / 2, SCREEN_HEIGHT - 2, libtcod.BKGND_NONE, libtcod.CENTER,
                                 'By Captaincowtj')

        choice = menu('', ['New Game', 'Continue', 'Quit'], 24)

        if choice == 0:
            new_game()
            play_game()

        elif choice == 1:  # load last game
            try:
                load_game()
            except:
                msgbox('\n No saved game to load.\n', 24)
                continue
            play_game()
        elif choice == 2:
            break

def character_creation():
    global player
    img = libtcod.image_load(MENU_BG)

    while not libtcod.console_is_window_closed():
        libtcod.console_wait_for_keypress(True)

        libtcod.console_clear(0)
        libtcod.image_blit_2x(img, 0, 0, 0)

        libtcod.console_set_default_foreground(0, libtcod.light_yellow)
        libtcod.console_print_ex(0, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 4, libtcod.BKGND_NONE, libtcod.CENTER,
                                 'Choose Player Class')
        libtcod.console_print_ex(0, SCREEN_WIDTH / 2, SCREEN_HEIGHT - 2, libtcod.BKGND_NONE, libtcod.CENTER, '')

        choice = menu('', ['Knight', 'Barbarian', 'Mage', 'Cleric', 'Rouge'], 24)
        # choosing class, sets base growths and stats
        life_base = 0
        life_growth_min = 0
        life_growth_max = 0
        mana_base = 0
        mana_growth_min = 0
        mana_growth_max = 0

        constitution = 0
        strength = 0
        dexterity = 0
        wisdom = 0
        intelligence = 0
        agility = 0

        if choice == 0:
            life_base += 14
            life_growth_min += 1
            life_growth_max += 8

            mana_base += 3
            mana_growth_min += 1
            mana_growth_max += 1


            ent = Entity(0, 0, '/', 'short sword', libtcod.dark_grey, equipment=equipment_short_sword)
            inventory.append(ent)
            equipment_short_sword.equip()
            ent.always_visible = True

            ent = Entity(0, 0, '/', 'long sword', libtcod.dark_grey, equipment=equipment_long_sword)
            inventory.append(ent)
            ent.always_visible = True

            ent = Entity(0, 0, '/', 'claymore', libtcod.dark_grey, equipment=equipment_claymore)
            inventory.append(ent)
            ent.always_visible = True


            ent = Entity(0, 0, '[', 'small shield', libtcod.darker_orange, equipment=equipment_small_shield)
            inventory.append(ent)
            equipment_small_shield.equip()
            ent.always_visible = True
            player_class = 'knight'

            ent = Entity(0, 0, '*', 'bread', libtcod.darker_orange, potion=bread_component)
            ent.item.amt = 3
            inventory.append(ent)
            ent.always_visible = True

            ent = Entity(0, 0, '*', 'jerky', libtcod.darker_orange, potion=jerky_component)
            ent.item.amt = 1
            inventory.append(ent)
            ent.always_visible = True

            stat_highs = ['strength', 'constitution', 'intelligence']

        elif choice == 1:
            life_base += 14
            life_growth_min += 1
            life_growth_max += 10

            mana_base += 1
            mana_growth_min += 1
            mana_growth_max += 1


            ent = Entity(0, 0, '/', "woodcutter's axe", libtcod.darkest_orange, equipment=equipment_woodcutter_axe)
            inventory.append(ent)
            equipment_woodcutter_axe.equip()
            ent.always_visible = True

            player_class = 'barbarian'

            ent = Entity(0, 0, '*', 'jerky', libtcod.darker_orange, potion=jerky_component)
            ent.item.amt = 2
            inventory.append(ent)
            ent.always_visible = True

            ent = Entity(0, 0, '*', 'potato', libtcod.darker_orange, potion=potato_component)
            ent.item.amt = 3
            inventory.append(ent)
            ent.always_visible = True

            stat_highs = ['strength', 'constitution', 'dexterity']

        elif choice == 2:
            life_base += 10
            life_growth_min += 1
            life_growth_max += 6

            mana_base += 6
            mana_growth_min += 1
            mana_growth_max += 2


            ent = Entity(0, 0, '/', 'cedar staff', libtcod.dark_orange, equipment=equipment_cedar_staff)
            inventory.append(ent)
            equipment_cedar_staff.equip()
            ent.always_visible = True

            player_class = 'mage'

            stat_highs = ['intelligence', 'wisdom', 'constitution']

            ent = Entity(0, 0, '*', 'bread', libtcod.darker_orange, potion=bread_component)
            ent.item.amt = 5
            inventory.append(ent)
            ent.always_visible = True

        elif choice == 3:
            life_base += 12
            life_growth_min += 1
            life_growth_max += 8

            mana_base += 6
            mana_growth_min += 1
            mana_growth_max += 2


            ent = Entity(0, 0, '/', 'mace', libtcod.darkest_grey, equipment=equipment_mace)
            inventory.append(ent)
            equipment_mace.equip()
            ent.always_visible = True

            player_class = 'cleric'

            ent = Entity(0, 0, '*', 'bread', libtcod.darker_orange, potion=bread_component)
            ent.item.amt = 3
            inventory.append(ent)
            ent.always_visible = True

            ent = Entity(0, 0, '*', 'bread', libtcod.darker_orange, item=honey_component)
            ent.item.amt = 3
            inventory.append(ent)
            ent.always_visible = True


            stat_highs = ['wisdom', 'constitution', 'strength']

        elif choice == 4:

            life_base += 10
            life_growth_min += 1
            life_growth_max += 8

            mana_base += 1
            mana_growth_min += 1
            mana_growth_max += 1


            ent = Entity(0, 0, '/', 'short sword', libtcod.dark_grey, equipment=equipment_short_sword)
            inventory.append(ent)
            equipment_short_sword.equip()
            ent.always_visible = True


            ent = Entity(0, 0, "-", 'throwing knife', libtcod.grey, ranged=throwing_knife)
            inventory.append(ent)
            ent.item.amt = 5
            ent.ranged.equip_ranged()
            ent.always_visible = True


            ent = Entity(0, 0, "-", 'heavy throwing knife', libtcod.grey, ranged=heavy_throwing_knife)
            inventory.append(ent)
            ent.item.amt = 3
            ent.always_visible = True

            player_class = 'rouge'

            ent = Entity(0, 0, '*', 'jerky', libtcod.darker_orange, potion=jerky_component)
            ent.item.amt = 2
            inventory.append(ent)
            ent.always_visible = True

            ent = Entity(0, 0, '*', 'bread', libtcod.darker_orange, potion=bread_component)
            ent.item.amt = 1
            inventory.append(ent)
            ent.always_visible = True

            stat_highs = ['agility', 'dexterity', 'strength']

        libtcod.image_blit_2x(img, 0, 0, 0)

        libtcod.console_set_default_foreground(0, libtcod.light_yellow)
        libtcod.console_print_ex(0, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 4, libtcod.BKGND_NONE, libtcod.CENTER,
                                 'Choose Player Race')
        libtcod.console_print_ex(0, SCREEN_WIDTH / 2, SCREEN_HEIGHT - 2, libtcod.BKGND_NONE, libtcod.CENTER, '')

        libtcod.console_wait_for_keypress(True)

        choice = menu('', ['Human', 'Elf', 'Dwarf', 'Orc', 'Gnome'], 24)
        # set player race, stats and growths
        if choice == 0:
            life_base += 2
            life_growth_min += 1
            life_growth_max += 2

            mana_base = 1
            mana_growth_min += 2
            mana_growth_max += 2

            player_race = 'human'

        elif choice == 1:
            life_base += 1
            life_growth_min += 1
            life_growth_max += 1

            mana_base = 2
            mana_growth_min += 3
            mana_growth_max += 3

            player_race = 'elf'

        elif choice == 2:
            life_base += 4
            life_growth_min += 1
            life_growth_max += 3

            mana_base += 0
            mana_growth_min += 0
            mana_growth_max += 0
            player_race = 'dwarf'

        elif choice == 3:
            life_base += 1
            life_growth_min += 1
            life_growth_max += 1

            mana_base += 1
            mana_growth_min += 1
            mana_growth_max += 1
            player_race = 'orc'

        elif choice == 4:
            life_base += 1
            life_growth_min += 1
            life_growth_max += 1

            mana_base += 2
            mana_growth_min += 2
            mana_growth_max += 2
            player_race = 'gnome'

        stat_list = []
        for i in range(6):
            x = dice_sum(6, 4, 1)
            stat_list.append(x)

        stat_list.sort()
        stat_list.reverse()

        for i in range(3):
            if stat_highs[0] == 'strength':
                strength = stat_list[0]

            elif stat_highs[0] == 'dexterity':
                dexterity = stat_list[0]

            elif stat_highs[0] == 'constitution':
                constitution = stat_list[0]

            elif stat_highs[0] == 'wisdom':
                wisdom = stat_list[0]

            elif stat_highs[0] == 'intelligence':
                intelligence = stat_list[0]

            elif stat_highs[0] == 'agility':
                agility = stat_list[0]

            stat_highs.pop(0)
            stat_list.pop(0)

        for i in range(3):
            if strength == 0:
                strength = stat_list.pop(libtcod.random_get_int(0, 0, len(stat_list) - 1))

            elif dexterity == 0:
                dexterity = stat_list.pop(libtcod.random_get_int(0, 0, len(stat_list) - 1))

            elif constitution == 0:
                constitution = stat_list.pop(libtcod.random_get_int(0, 0, len(stat_list) - 1))

            elif intelligence == 0:
                intelligence = stat_list.pop(libtcod.random_get_int(0, 0, len(stat_list) - 1))

            elif wisdom == 0:
                wisdom = stat_list.pop(libtcod.random_get_int(0, 0, len(stat_list) - 1))

            elif agility == 0:
                agility = stat_list.pop(libtcod.random_get_int(0, 0, len(stat_list) - 1))

        stat_growths = [life_base, life_growth_min, life_growth_max, mana_base, mana_growth_min, mana_growth_max]
        start_life = stat_growths[0] + libtcod.random_get_int(0, -2, 4)
        start_mana = stat_growths[3] + libtcod.random_get_int(0, -1, 2)

        constitution += libtcod.random_get_int(0, -2, 4)
        strength += libtcod.random_get_int(0, -2, 4)
        dexterity += libtcod.random_get_int(0, -2, 4)
        wisdom += libtcod.random_get_int(0, -2, 4)
        intelligence += libtcod.random_get_int(0, -2, 4)
        agility += libtcod.random_get_int(0, -2, 4)

        if start_life < 1:
            start_life = 1
        if start_mana < 1:
            start_mana = 1
        x = stat_growths

        fighter_component = Fighter(xp=0, hp_stat=start_life, mp_stat=start_mana, constitution=constitution,
                                    strength=strength, dexterity=dexterity, wisdom=wisdom, intelligence=intelligence,
                                    agility=agility, growths=stat_growths, race=player_race, job=player_class,
                                    death_function=player_death)
        player = Entity(0, 0, '@', 'player', libtcod.white, blocks=True, fighter=fighter_component)
        player.fighter.growths = stat_growths



        if QUICKSTART == False:
            name = input_name()

            player.name = name


            libtcod.console_clear(0)
            libtcod.image_blit_2x(img, 0, 0, 0)
            # libtcod.console_wait_for_keypress(True)

            libtcod.console_set_default_foreground(0, libtcod.light_yellow)
            libtcod.console_print_ex(0, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 4, libtcod.BKGND_NONE, libtcod.CENTER,
                                     'Choose Player Gender')
            libtcod.console_print_ex(0, SCREEN_WIDTH / 2, SCREEN_HEIGHT - 2, libtcod.BKGND_NONE, libtcod.CENTER, '')

            choice = menu('', ['Male', 'Female'], 24)

            if choice == 0:
                player.fighter.gender = 'male'

            elif choice == 1:
                player.fighter.gender = 'female'
        # add player skills
        if player_class == 'knight':
            teach_skill('shield bash', player)
            pass

        if player_class == 'mage':
            teach_skill('force', player)
            teach_skill('fireburst', player)
            teach_skill('confuse', player)
            teach_skill('detect monster', player)

        if player_class == 'cleric':
            teach_skill('heal', player)
            teach_skill('barrier', player)

        if player_class == 'rouge':
            teach_skill('throw weapon', player)
            pass

        player.level = 1
        break

def render_bar(x, y, total_width, name, value, maximum, bar_color, back_color, text_color):
    # render a bar (HP, experience, etc). first calculate the width of the bar
    bar_width = int(float(value) / maximum * total_width)

    # render the background first
    libtcod.console_set_default_background(panel, back_color)
    libtcod.console_rect(panel, x, y, total_width, 1, False, libtcod.BKGND_SCREEN)
    # now render the bar on top
    libtcod.console_set_default_background(panel, bar_color)
    if bar_width > 0:
        libtcod.console_rect(panel, x, y, bar_width, 1, False, libtcod.BKGND_SCREEN)

    # finally, some centered text with the values
    libtcod.console_set_default_foreground(panel, text_color)
    libtcod.console_print_ex(panel, x + total_width / 2, y, libtcod.BKGND_NONE, libtcod.CENTER,
                             name + ': ' + str(value) + '/' + str(maximum))

message_num = 0

def message(new_msg, color=libtcod.white):
    global message_num
    # split the message if necessary, among multiple lines
    new_msg_lines = textwrap.wrap(new_msg, MSG_WIDTH)

    for line in new_msg_lines:
        # if the buffer is full, remove the first line to make room for the new one
        if len(game_msgs) == MSG_HEIGHT - 1:
            del game_msgs[0]

        # add the new line as a tuple, with the text and the color
        if message_num % 2 == 0:
            game_msgs.append(('-' + line, color))
        else:
            game_msgs.append(('>' + line, color))
        message_num +=1


def menu(header, options, width):
    if len(options) > 26: raise ValueError('Cannot have menu with more than 26 options.')
    # calc window height
    header_height = libtcod.console_get_height_rect(con, 0, 0, width, SCREEN_HEIGHT, header)
    if header == '':
        header_height = 0
    height = len(options) + header_height

    # off-screen console for menu window
    window = libtcod.console_new(width, height)

    # print header
    libtcod.console_set_default_foreground(window, libtcod.white)
    libtcod.console_print_rect_ex(window, 0, 0, width, height, libtcod.BKGND_NONE, libtcod.LEFT, header)

    # print all options
    y = header_height
    letter_index = ord('a')
    for option_text in options:
        text = '(' + chr(letter_index) + ') ' + option_text
        libtcod.console_print_ex(window, 0, y, libtcod.BKGND_NONE, libtcod.LEFT, text)
        y += 1
        letter_index += 1

    # blit the contents of "window" to the root console
    x = SCREEN_WIDTH / 2 - width / 2
    y = SCREEN_HEIGHT / 2 - height / 2
    libtcod.console_blit(window, 0, 0, width, height, 0, x, y, 1.0, 0.7)

    # present root console to player and wait for key press
    libtcod.console_flush()
    key = libtcod.console_wait_for_keypress(True)

    if key.vk == libtcod.KEY_ENTER and key.lalt:  # (special case) Alt+Enter: toggle fullscreen
        libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

    # convert the ASCII code to an index; if it corresponds to an option, return it
    index = key.c - ord('a')
    if index >= 0 and index < len(options): return index
    return None


def inventory_menu(header):
    # display menu w/ each inventory item as choice

    if len(inventory) == 0:
        options = ['Inventory is empty.']
    else:
        options = []
        for i in inventory:
            text = i.name
            # show additional information, in case it's equipped


            if i.equipment and i.equipment.is_equipped:
                slotname = ''
                for j in range(len(i.equipment.slot)):
                    slotname = slotname + str(i.equipment.slot[j]) + ', '

                slotname = slotname[:-2]

                text = text + ' (on ' + slotname + ')'
            if i.potion or i.ranged or i.scroll:
                text = text + " x " + str(i.item.amt)
            if i.ranged:
                if i.ranged.ready == True:
                    text = text + ' (ready)'


            options.append(text)
    index = menu(header, options, INVENTORY_WIDTH)
    libtcod.console_wait_for_keypress(False)

    # if an item was chosen, return it
    if index is None or len(inventory) == 0: return None
    return inventory[index].item


def skill_menu(header):
    # display menu w/ each inventory item as choice
    if len(player.fighter.skills) == 0:
        options = ['No skills.']
    else:
        options = []
        for skill in player.fighter.skills:
            text = skill.name
            # show additional information, in case it's equipped

            options.append(text)

    index = menu(header, options, INVENTORY_WIDTH)
    libtcod.console_wait_for_keypress(False)

    # if an item was chosen, return it
    if index is None or len(player.fighter.skills) == 0: return None
    return player.fighter.skills[index]


def fav_menu(header):
    global key, keybinds

    if len(player.fighter.skills) == 0:
        msgbox("No skills to bind")
        return None
    else:

        options = []
        for skill in player.fighter.skills:
            text = skill.name
            # show additional information, in case it's equipped

            options.append(text)

    index = menu(header, options, INVENTORY_WIDTH)
    while True:

        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, key, mouse)
        render_all()

        if key.vk == libtcod.KEY_1:
            keybind = libtcod.KEY_1
            break
        elif key.vk == libtcod.KEY_2:
            keybind = libtcod.KEY_2
            break
        elif key.vk == libtcod.KEY_3:
            keybind = libtcod.KEY_3
            break
        elif key.vk == libtcod.KEY_4:
            keybind = libtcod.KEY_4
            break
        elif key.vk == libtcod.KEY_5:
            keybind = libtcod.KEY_5
            break
        else:
            keybind = None

    # if an item was chosen, return it
    if index is None or len(player.fighter.skills) == 0: return None
    player.fighter.skills[index].bind = keybind
    message(str(player.fighter.skills[index].name) + " has been bound to key " + str(player.fighter.skills[index].bind),
            libtcod.green)
    keybinds[keybind] = player.fighter.skills[index]
    return

def input_name():
    img = libtcod.image_load(MENU_BG)
    timer = 0
    command = ''
    x = SCREEN_WIDTH / 2 - 5
    y = SCREEN_HEIGHT / 2 - 1
    libtcod.console_clear(0)
    libtcod.image_blit_2x(img, 0, 0, 0)
    libtcod.console_wait_for_keypress(True)

    while True:

        libtcod.console_set_default_foreground(0, libtcod.light_yellow)
        libtcod.console_print_ex(0, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 4, libtcod.BKGND_NONE, libtcod.CENTER,
                                 'Enter your name, ' + player.fighter.race + ' ' + player.fighter.job + '.')
        libtcod.console_print_ex(0, SCREEN_WIDTH / 2, SCREEN_HEIGHT - 2, libtcod.BKGND_NONE, libtcod.CENTER, '')

        key = libtcod.console_check_for_keypress(libtcod.KEY_PRESSED)

        timer += 1
        # sets the blinking rate of the cursor
        if timer % (LIMIT_FPS // 4) == 0:
            if timer % (LIMIT_FPS // 2) == 0:
                timer = 0
                libtcod.console_set_char(0, x, y, "_")
                libtcod.console_set_char_foreground(0, x, y, libtcod.white)
            else:
                libtcod.console_set_char(0, x, y, " ")
                libtcod.console_set_char_foreground(0, x, y, libtcod.white)

        if key.vk == libtcod.KEY_BACKSPACE and x > 0:
            libtcod.console_set_char(0, x, y, " ")
            libtcod.console_set_char_foreground(0, x, y, libtcod.white)
            command = command[:-1]
            if x > SCREEN_WIDTH / 2 - 5:
                x -= 1
        elif key.vk == libtcod.KEY_ENTER:
            libtcod.console_clear(0)
            libtcod.image_blit_2x(img, 0, 0, 0)
            libtcod.console_wait_for_keypress(True)

            libtcod.console_set_default_foreground(0, libtcod.light_yellow)
            libtcod.console_print_ex(0, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 4, libtcod.BKGND_NONE, libtcod.CENTER,
                                     'Is ' + command + ' your name?')
            libtcod.console_print_ex(0, SCREEN_WIDTH / 2, SCREEN_HEIGHT - 2, libtcod.BKGND_NONE, libtcod.CENTER, '')

            choice = menu('', ['Yes', 'No'], 24)
            libtcod.console_wait_for_keypress(True)
            if choice == 0:
                break
            else:
                command = ''
                command = ''
                timer = 0
                x = SCREEN_WIDTH / 2 - 5
                y = SCREEN_HEIGHT / 2 - 1
                libtcod.console_clear(0)
                libtcod.image_blit_2x(img, 0, 0, 0)
                libtcod.console_wait_for_keypress(True)
                continue
        elif key.vk == libtcod.KEY_ESCAPE:
            command = ""
            break
        elif key.c > 0:
            letter = chr(key.c)
            libtcod.console_set_char(0, x, y, letter)  # print new character at appropriate position on screen
            libtcod.console_set_char_foreground(0, x, y, libtcod.white)  # make it white
            command += letter  # add to the string
            if x == SCREEN_WIDTH / 2 + 4:
                libtcod.console_clear(0)
                libtcod.image_blit_2x(img, 0, 0, 0)
                libtcod.console_wait_for_keypress(True)

                libtcod.console_set_default_foreground(0, libtcod.light_yellow)
                libtcod.console_print_ex(0, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 4, libtcod.BKGND_NONE, libtcod.CENTER,
                                         'Is ' + command + ' your name?')
                libtcod.console_print_ex(0, SCREEN_WIDTH / 2, SCREEN_HEIGHT - 2, libtcod.BKGND_NONE, libtcod.CENTER, '')

                choice = menu('', ['Yes', 'No'], 24)

                if choice == 0:
                    break
                else:
                    command = ''
                    timer = 0
                    x = SCREEN_WIDTH / 2 - 5
                    y = SCREEN_HEIGHT / 2 - 1
                    libtcod.console_clear(0)
                    libtcod.image_blit_2x(img, 0, 0, 0)
                    libtcod.console_wait_for_keypress(True)
                    continue
            else:
                x += 1

        libtcod.console_flush()

    return command


def msgbox(text, width=50):
    menu(text, [], width)  # use menu() as a sort of "message box"


def get_names_under_mouse():
    global mouse

    # return string with all things under mouse
    (x, y) = (mouse.cx, mouse.cy)

    # list of stuff under mouse and in fov
    names = [ent.name for ent in entities
             if ent.x == x and ent.y == y and libtcod.map_is_in_fov(fov_map, ent.x, ent.y)]

    names = ', '.join(names)  # join the names, separated by commas
    return names.capitalize()

########################################################################################################################
#   Item Declaration
########################################################################################################################

#declares components for items to help with standardization
if 'swords' or True:
    equipment_short_sword = Equipment(1, 'LightBlade', slot=['right hand'], power_bonus=2)

    equipment_long_sword = Equipment(1, 'LightBlade', slot=['right hand'], power_bonus=3)

if 'greatswords' or True:
    equipment_bastard_sword = Equipment(1, 'HeavyBlade', slot=['left hand', 'right hand'], power_bonus=4)

    equipment_claymore = Equipment(1, 'HeavyBlade', slot=['left hand', 'right hand'], power_bonus=5)

if 'axes' or True:
    equipment_woodcutter_axe = Equipment(2, 'LightAxe', slot=['right hand'], power_bonus=3)

    equipment_battle_axe = Equipment(2, 'LightAxe', slot=['right hand'], power_bonus=4)

if 'greataxes' or True:
    equipment_war_axe = Equipment(2, 'HeavyAxe', slot=['left hand', 'right hand'], power_bonus = 5)

    equipment_great_axe = Equipment(2, 'HeavyAxe', slot=['left hand', 'right hand'], power_bonus = 6)

if 'hammers' or True:
    equipment_club = Equipment(2, 'Hammer', slot=['right hand'], power_bonus=2)

    equipment_mace = Equipment(2, 'Hammer', slot=['right hand'], power_bonus=3)

    equipment_warhammer = Equipment(2, 'Hammer', slot=['right hand'], power_bonus=4)

if 'staves' or True:
    equipment_balsa_staff = Equipment(1, 'Staff', slot=['right hand'], power_bonus=-1)

    equipment_cedar_staff = Equipment(1, 'Staff', slot=['right hand'], power_bonus=2)

    equipment_birch_staff = Equipment(1, 'Staff', slot=['right hand'], power_bonus=3)

    equipment_oak_staff = Equipment(1, 'Staff', slot=['right hand'], power_bonus=4)

    equipment_beech_staff = Equipment(1, 'Staff', slot=['right hand'], power_bonus=5)

    equipment_maple_staff = Equipment(1, 'Staff', slot=['right hand'], power_bonus=6)

    equipment_mahogany_staff = Equipment(1, 'Staff', slot=['right hand'], power_bonus=7)

    equipment_ironbark_staff = Equipment(1, 'Staff', slot=['right hand'], power_bonus=8)

if 'throwing weapons' or True:
    throwing_knife = RangedWeapon(0, damage=1, effect=None, range=5)

    heavy_throwing_knife = RangedWeapon(0, damage=2, effect=None, range=4)

if 'large throwing weapons' or True:
    throwing_axe = RangedWeapon(0, damage=3, effect=None, range=3)

    heavy_throwing_axe = RangedWeapon(0, damage=4, effect=None, range=2)

if 'shields' or True:
    equipment_small_shield = Equipment(1, 'SmallShield', slot=['left hand'], defense_bonus=1)

    equipment_shield = Equipment(1, 'Shield', slot=['left hand'], defense_bonus=2)

if 'LightArmor' or True:
    equipment_cloth_tunic = Equipment(1, 'LightArmor', slot=['body'], defense_bonus=1)

    equipment_hide_tunic = Equipment(1, 'LightArmor', slot=['body'], defense_bonus=2)

    equipment_leather_armor = Equipment(1, 'LightArmor', slot=['body'], defense_bonus=3)

    equipment_boiled_leather_armor = Equipment(1, 'LightArmor', slot=['body'], defense_bonus=4)

    equipment_reinforced_leather_armor = Equipment(1, 'LightArmor', slot=['body'], defense_bonus=5)

if 'MediumArmor' or True:
    equipment_studded_leather_armor = Equipment(1, 'MediumArmor', slot=['body'], defense_bonus=3)

    equipment_light_chainmail = Equipment(1, 'MediumArmor', slot=['body'], defense_bonus=4)

    equipment_chainmail = Equipment(1, 'MediumArmor', slot=['body'], defense_bonus=5)

    equipment_heavy_chainmail = Equipment(1, 'MediumArmor', slot=['body'], defense_bonus=6)

    equipment_elven_chainmail = Equipment(1, 'MediumArmor', slot=['body'], defense_bonus=7)

if 'HeavyArmor' or True:
    equipment_iron_chestplate = Equipment(1, 'HeavyArmor', slot=['body'], defense_bonus=4)

    equipment_banded_iron_chestplate = Equipment(1, 'HeavyArmor', slot=['body'], defense_bonus=5)

    equipment_steel_chestplate = Equipment(1, 'HeavyArmor', slot=['body'], defense_bonus=6)

    equipment_steel_plate_armor = Equipment(1, 'HeavyArmor', slot=['body'], defense_bonus=7)

    equipment_orichalcum_chestplate = Equipment(1, 'HeavyArmor', slot=['body'], defense_bonus=8)

if 'Cloak' or True:
    equipment_simple_cape = Equipment(1, 'Cloak', slot=['cloak'], defense_bonus=1)
    equipment_hooded_cloak = Equipment(1, 'Cloak', slot=['cloak', 'head'], defense_bonus=2, evasion_bonus=1)

if 'scrolls' or True:

    scroll_of_lightning = Scroll(0.1, cast_lightning)

    scroll_of_fireburst = Scroll(0.1, cast_fireburst)

    croll_of_sonfusion = Scroll(0.1, cast_confuse)

if 'tomes' or True:

    force_tome = Scroll(0.3, cast_force, teach='force')

if 'potions' or True:
    potion_heal_component = Potion(0.3, 'heal', 30, 0)


    potion_large_heal_component = Potion(0.3, 'heal', 50, 0)

    potion_detect_monster_component = Potion(0.3, 'detect monster', 1, 50)

if 'food' or True:
    bread_component = Potion(0.3, 'food', 150, 0)

    jerky_component = Potion(0.3, 'food', 300, 0)

    potato_component = Potion(0.3, 'food', 50, 0)

    honey_component = Potion(0.3, 'food', 100, 0)

    lembas_bread_component = Potion(0.3, 'food', 1000, 0)

########################################################################################################################
#   Formulas
########################################################################################################################

def attack_formula(caster, target):
    dmg = libtcod.random_get_int(0,1,caster.fighter.strength) + caster.fighter.power - target.fighter.defense

    if caster.fighter.agility > libtcod.random_get_int(0,0,100):
        return (dmg*CRITMOD, True)
    return (dmg, False)

def attack_formula_throwing(caster, target, weapon):
    dmg = libtcod.random_get_int(0,1,caster.fighter.strength) + weapon.owner.ranged.damage - target.fighter.defense

    if caster.fighter.agility > libtcod.random_get_int(0,0,100):
        return (dmg*CRITMOD, True)
    return (dmg, False)

def mag_attack_formula(caster, target):
    dmg = libtcod.random_get_int(0,1,caster.fighter.intelligence) + caster.fighter.magic - target.fighter.defense

    if caster.fighter.wisdom > libtcod.random_get_int(0,0,100):
        return (dmg * CRITMOD, True)
    return (dmg, False)

def hit_formula(caster, target):

    if(caster.fighter.accuracy - target.fighter.evasion >= libtcod.random_get_int(0,1,100)):

        return True
    return False

def dice_sum(sides, times, drop):
    x = 0
    rolls = []
    for i in range(times):
        rolls.append(libtcod.random_get_int(0,1,sides))
    rolls.sort()
    for i in range(times-drop):
        y = rolls.pop(1)
        x = x + y

    return x

########################################################################################################################
#   Initialization
########################################################################################################################

#makes sure fonts are represented correctly
if "_ro" in FONT:
    libtcod.console_set_custom_font(FONT, libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_ASCII_INROW)
elif "_co" in FONT:
    libtcod.console_set_custom_font(FONT, libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_ASCII_INCOL)
else:
    libtcod.console_set_custom_font(FONT, libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'rougelike/v0.1.0', False)
libtcod.sys_set_fps(LIMIT_FPS)
con = libtcod.console_new(SCREEN_WIDTH, SCREEN_HEIGHT)

panel = libtcod.console_new(SCREEN_WIDTH, PANEL_HEIGHT)

main_menu()


