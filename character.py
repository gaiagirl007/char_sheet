"""
This is currently a character creator. Hopefully I will be able to expand it to
include the ability to update characters and access them through a GUI. This is
currently built on the Dungeons & Dragons 5E free PDF rulebook.
"""

import random
import my_dice
import json

INVALID = ['\\', '/', ':', '*', '?', '"', '<', '>', '|']

ALL_PROF = {
    'Acrobatics': 'DEX', 'Animal Handling': 'WIS', 'Arcana': 'INT', 'Athletics': 'STR',
    'Deception': 'CHR', 'History': 'INT', 'Insight': 'WIS', 'Intimidation': 'CHR',
    'Investigation': 'INT', 'Medicine': 'WIS', 'Nature': 'INT', 'Perception': 'WIS',
    'Performance': 'CHR', 'Persuasion': 'CHR', 'Religion': 'INT', 'Sleight of Hand': 'DEX',
    'Stealth': 'DEX', 'Survival': 'WIS'
    }

PROF = [2, 2, 2, 2, 3]
STAT_POS = ['STR', 'DEX', 'CON', 'INT', 'WIS', 'CHR']

class Character(object):
    """A class called Character. Stores the overarching data that makes a character

    Instance Attributes:
        _name: the character name [str]
        _stats: the ability scores of the character [dict of int, keys in STAT_POS]
        _lvl: the level of the character [int > 0]
        _race: the race of the character [instance of Race]
        _class: the class of the character [instance of Class]
        _background: the background of the character
        _mods: the modifiers calculated from _stats [dict of int, keys in STAT_POS]
        _profs: the proficiencies a character has [dict of int, keys in ALL_PROF]
        _casting: the character's spellcasting ability [int > 1]
    """

    def __init__(self, name = None, stats = None, lvl = None, race = None,\
        char_class = None, background = None, filename = None, path = None):
        """Initializes a Character with a name, level (lvl), race, class, and
        background, OR creates a file where the character data will be saved.

        If initializing a character:
        name: non-empty str that does not contain the values in INVALID
        stats: dictionary of ints 6..20 with len 6
        lvl: int > 0
        race: object of type Race
        char_class: object of type Class (or inheriting from it)
        background: object of type Background
        filename: None

        If creating a file:
        filename: non-empty str
        """

        if filename == None:
            self._setstats(name, stats, lvl, race, char_class, background)

        else:
            self._newfile(filename)


    def __str__(self):
        """Returns a nice little summary of what makes a Character instance"""
        return "\n" + self._name + "\nLevel " + str(self._lvl) + " " +\
        str(self._race) + " " + str(self._class) + "\n" + str(self._stats) +\
        "\n" + str(self._profs) + "\nSpellcasting: " + str(self._casting) + "\n"


    def _setstats(self, name, stats, lvl, race, char_class, background):
        """Initializes the basic character info.

        name: non-empty str that does not contain the values in INVALID
        stats: dictionary of ints 6..20 with len 6
        lvl: int > 0
        race: object of type Race
        char_class: object of type Class (or inheriting from it)
        background: object of type Background
        filename: None
        """
        #check preconditions
        assert is_valid_name(name)
        assert type(stats) == dict and is_valid_stats(list(stats.values()), 20)
        assert type(lvl) == int and lvl > 0
        assert isinstance(race, Race)
        assert isinstance(char_class, Class)

        self._name = name
        self._stats = stats
        self._lvl = lvl

        self._race = race
        self._class = char_class
        self._background = background

        self._mods = {}
        for i in self._stats:
            self._mods[i] = (self._stats[i] - 10) // 2

        self._makeprofs()

        self._casting = None
        casting = self._class.getSpells()
        if casting != None:
            self._casting = 8 + self._mods[casting] + PROF[self._lvl - 1]


    def _makeprofs(self):
        """Sets proficiencies; helper function for __init__"""
        self._profs = {}
        if self._class.getProfs() != None:
            num = 2
            if self._class == rogue:
                num += 2

            class_profs = random.sample(self._class.getProfs(), num)
            #back_profs = ...
            for j in class_profs:
                self._profs[j] = self._mods[ALL_PROF[j]] + PROF[self._lvl - 1]


    def _newfile(self, filename, path):
        """Creates a new file named filename for saving character data.

        filename: non-empty str
        path: None or non-empty str
        """
        assert type(filename) == str and filename != ''
        assert path == None or (type(path) == str and path != '')

        savedata = self._dictme()

        if path == None:
            path = 'savedata'

        with open('./' + path + '/' + filename, 'w') as file:
            json.dump(savedata, file)


    def _dictme(self):
        """Helper function for _newfile. Takes the relevant attributes of an
        instance of a character and converts them to a dictionary for the purposes
        of saving with json."""
        dict = {}

        dict["name"] = self._name
        dict["stats"] = self._stats
        dict["lvl"] = self._lvl
        dict["race"] = self._race
        dict["class"] = self._class
        dict["background"] = self._background

        return dict


### Update function maybe?
    def lvlup(self):
        """Increments _lvl by 1"""
        self._lvl += 1

        #and then access the _class object to update other attributes


class Race(object):
    """A class called Race. Stores all of the things that make a race instance
    unique.

    Instance Attributes:
        _name: the name of the race
        _statbonus: the bonus(es) to ability stats specific to a race
        _darkvision: whether or not the race instance can see in the dark
    """

    def __init__(self, name, statbonus, darkvision = False):
        """Initializes Race of type name.

        name: non-empty str
        statbonus: dictionary of int
        darkvision: a bool

        ###language: list of str
        ###sub: list of str, or None
        """
        #checks preconditions
        assert type(name) == str and name != ''
        assert type(statbonus) == dict
        assert type(darkvision) == bool

        self._name = name
        self._statbonus = statbonus
        self._darkvision = darkvision


    def __str__(self):
        return self._name


    def getBonus(self):
        """Returns the dictionary of stat bonuses"""
        return self._statbonus


class Class(object):
    """A class called Class. Used to manage the overarching functions that are
    the same for all classes.

    Instance Attributes:
        _name: the name of the character class
        _spells: if the class knows spells
        _spellstat: which stat influences the class's spells
        _profs: what proficiencies "come with" the class
    """
    def __init__(self, name, profs = None, spellstat = None, can_cast = False):
        """Initializes a Class of type name.

        name: non-empty str
        profs: None or list of str in ALL_PROF keys
        can_cast: bool
        spellstat: None or str
        """
        #checks preconditions
        assert type(name) == str and name != ''
        assert profs == None or is_valid_profs(profs)
        assert type(can_cast) == bool
        assert spellstat == None or type(spellstat) == str

        self._name = name
        self._profs = profs
        self._spells = can_cast
        self._spellstat = spellstat


    def __str__(self):
        """Returns the stringified version of a Class instance"""
        return self._name


    def getProfs(self):
        """Returns the list of proficiencies associated with a Class instance"""
        return self._profs


    def getSpells(self):
        """Returns the ability score the Class instance uses for spellcasting if
        the class can spellcast. Otherwise returns None."""
        if self._spells == True:
            return self.getStat()

        else:
            return None


    def getStat(self):
        return self._spellstat


def new_char(name = "Adventurer Doe", randomize = True, helpful_plz = False,\
    raw_stats = None, race = None, char_class = None):
    """Returns the id of a Character. If randomize is True, then my_dice generates
    stats and everything else. Otherwise, parameters are provided by the user.
    helpful_plz modifies randomize. If helpful_plz is true, the stats will be
    partially tailored to the class. If the user forgets to input parameters,
    they are randomized by default. raw_stats are assigned to strength, dexterity,
    consitution, intelligence, wisdom, and charisma in that respective order.

    name: non-empty str that does not contain the values in INVALID
    randomize: bool
    helpful_plz: bool
    raw_stats: None or a list of int 3..18 of len 6
    race: object of type Race or None
    char_class: object of type Class or None
    """
    #checks preconditions
    assert is_valid_name(name)
    assert type(randomize) == bool
    assert type(helpful_plz) == bool
    assert raw_stats == None or is_valid_stats(raw_stats)
    assert race == None or isinstance(race, Race)
    assert char_class == None or isinstance(char_class, Class)

    #creates an key-only dictionary for putting final stats in
    stats = {'STR': 0, 'DEX': 0, 'CON': 0, 'INT': 0, 'WIS': 0, 'CHR': 0}

    if randomize == True or race == None:
        race = random.sample(races, 1)[0]

    if randomize == True or char_class == None:
        char_class = random.sample(char_classes, 1)[0]

    if randomize == True or raw_stats == None:
        raw_stats = my_dice.roll_stats()

        if helpful_plz == True:
            help = max(raw_stats)
            raw_stats.remove(help)
            raw_stats.insert(STAT_POS.index(char_class.getStat()), help)

    #puts raw_stats into the dictionary
    for i in range(len(stats)):
        stats[STAT_POS[i]] = raw_stats[i]

    #applies appropriate race bonuses to stats
    race_bonus = race.getBonus()
    for j in race_bonus:
        stats[j] += race_bonus[j]

    return Character(name, stats, 1, race, char_class)


################### Helper Functions for Preconditions #########################
def is_valid_stats(stats, max = 18):
    """
    Returns a bool: True if stats is a list of length 6 only containing ints
    between 3 and max inclusive

    max: int
    """
    assert type(max) == int

    if type(stats) != list:
        return False

    if len(stats) != 6:
        return False

    for i in stats:
        if type(i) == int and 3 <= i <= max:
            return True
        else:
            return False


def is_valid_profs(profs):
    """
    Returns a bool: True if profs is a list of str that correspond to keys in
    ALL_PROF
    """
    if type(profs) != list:
        return False

    for i in profs:
        if type(i) != str or i not in ALL_PROF:
            return False

    return True


def is_valid_name(name):
    """
    Returns a bool: True if name is a non-empty str that does not contain any
    of the special ascii characters in INVALID
    """
    if type(name) != str or name != '':
        return False

    for i in INVALID:
        if i in name:
            return False

    return True


####################### End Helper Functions ###################################

#Creates 4 basic objects of class race
dwarf = Race('Dwarf', {'CON': 2}, True)
elf = Race('Elf', {'DEX': 2}, True)
halfling = Race('Halfling', {'DEX': 2})
human = Race('Human', {'STR': 1, 'DEX': 1, 'CON': 1, 'INT': 1, 'WIS': 1, 'CHR': 1})

races = [dwarf, elf, halfling, human]

#creates 4 classes (for now)
cleric = Class('Cleric', ['History', 'Insight', 'Medicine', 'Persuasion',\
    'Religion'], 'WIS', True)

fighter = Class('Fighter', ['Acrobatics', 'Animal Handling', 'Athletics',\
    'History', 'Insight', 'Intimidation', 'Perception', 'Survival'], 'STR')

rogue = Class('Rogue', ['Acrobatics', 'Athletics', 'Deception', 'Insight',\
    'Intimidation', 'Investigation', 'Perception', 'Performance', 'Persuasion',\
    'Sleight of Hand', 'Stealth'], 'DEX')

wizard = Class('Wizard', ['Arcana', 'History', 'Insight', 'Investigation',\
    'Medicine', 'Religion'], 'INT', True)

char_classes = [cleric, fighter, rogue, wizard]
