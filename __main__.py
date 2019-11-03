"""
Hopefully where the magic happens.
"""

import character
import json
from os import listdir, getcwd

def new_or_load(slist):
    """Asks the user if they want to load a previous character or create a
    new one. If the user wants to load a previous character, it calls helper
    function loadthis which determines which character the user wants to load.

    slist: list of str"""
    assert is_string_list(slist)

    nlist = []
    for file in slist:
        end = file.find('.json')
        nlist.append(file[:end])

    while(True):
        usersays = input('Enter 1 to make a new character. Enter 2 to load' +\
        'a character.')

        if usersays != '1' or usersays != '2':
            print('Invalid input')
        else:
            break

    if usersays == '1':
        print('loading new character')
        return new_route()

    elif usersays == '2':
        lprompt = 'Enter the number of the character you would like to load.'
        loadfile = slist[pick_number(lprompt, nlist)]
        return character.Character(filename = loadfile)


def new_route():
    """Walks the user through the creation of a new character."""

    print('Enter character name: ')
    while True:
        name = input()
        if character.is_valid_name(name):
            break
        else:
            print("Please enter a name that does not contain " + str(character.INVALID))

    print('Generate a character from the depths of the deepest, darkest entropy? y/n')
    while True:
        answer = str.lower(input())
        if answer in ['y', 'yes']:
            print('Summoning the daemons of entropy...')
            return character.new_char(name, True, True)
        elif answer in ['n', 'no']:
            print('Manual input it is...')
            break
        else:
            print('Please enter a valid answer')

    #select stats
    stats = choose_stats()
    #select a race
    race = select_from_options('race', character.races)
    #select a character class
    chclass = select_from_options('character class', character.char_classes)
    #select a background
    background = select_from_options('background', character.backgrounds)

    print('Constructing to order...')
    return character.new_char(name, False, False, stats, character.races[race],\
        character.char_classes[chclass])


def choose_stats():
    """Walks the user through entering their ability scores. Returns a list of stats"""

    print('Enter your basic stats, without any bonuses')
    stats = []
    for i in character.STAT_POS:
        print(i + ': ')
        while True:
            try:
                num = int(input())
            except ValueError:
                print('Please enter a valid integer between 3 and 18')

            if num <= 18 and num >= 3:
                break
            else:
                print('Please enter a valid integer between 3 and 18')

        stats.append(num)

    return stats


############################### Helper functions ###############################
def select_from_options(name, from_class):
    """Guides the user through selecting an option from a list of instances.
    Prompts the user to select a <insert name> from the list of numbers. Returns
    the selected option.

    name: str
    from_class: dict in [character.char_classes, character.races, character.backgrounds]
    """
    assert type(name) == str
    assert from_class in [character.char_classes, character.races, character.backgrounds]

    prompt = 'Enter the number of the ' + name + ' you want to select'
    list = []
    for i in from_class:
        list.append(i)

    return list[pick_number(prompt, list)]


def pick_number(prompt, list):
    """Prompts the user with prompt, then prints a list of options which the
    user must pick a number from. If the user enters an invalid response,
    the function will inform them and and wait until they enter a valid
    response. Returns the index of the user's response.

    prompt: str
    list: list of str"""
    assert type(prompt) == str
    assert is_string_list(list)

    print(prompt)

    for i in list:
        print(str(list.index(i)) + ') ' + i)

    while(True):
        try:
            usersays = int(input())
        except ValueError:
            print('Please enter a valid number')

        if usersays < 0 or usersays >= len(list):
            print('Please enter a valid number')
        else:
            break

    return usersays


def is_string_list(val):
    """Determines whether a given value is a list of strings

    val: any"""
    if type(val) != list:
        return False

    for i in val:
        if type(i) != str:
            return False

    return True


##################################### Main #####################################

if __name__ == '__main__':

    saves = listdir('char_sheet/savedata')

    #checks to see if a saved character exists and if so, if the user want to load
    #that character or make a new one
    #LATER GOING TO BE GUI
    if saves == []:
        print('loading new character')
        mychar = new_route()

    else:
        mychar = new_or_load(saves)

    print(str(mychar))
