"""
Hopefully where the magic happens.
"""

import character
import json
from os import listdir

file = []

if __name__ == '__main__':

    saves = listdir('savedata')

    #checks to see if a saved character exists and if so, if the user want to load
    #that character or make a new one
    #LATER GOING TO BE GUI
    if saves == []:
        print('loading new character')

    else:
        mychar = new_or_load(saves)


    def new_or_load(slist):
        """Asks the user if they want to load a previous character or create a
        new one. If the user wants to load a previous character, it calls helper
        function loadthis which determines which character the user wants to load."""
        while(True):
            usersays = input('Enter 1 to make a new character. Enter 2 to load' +\
            'a character.')

            if usersays != '1' or usersays != '2':
                print('Invalid input')
            else:
                break

        if usersays == '1':
            print('loading new character')

        elif usersays == '2':
            loadfile = slist[loadthis(slist)]
            return character.Character(loadfile)


    def loadthis(slist):
        """Determines the character which will be loaded."""
        print('Enter the number of the character you would like to load.')

        for i in slist:
            print(str(slist.index(i)) + ')' + str(i))

        while(True):
            try:
                usersays = int(input())
            except ValueError:
                print('Please enter a valid number')

            if usersays < 0 or usersays >= len(saves):
                print('Please enter a valid number')
            else:
                break

        return usersays


    def new_route():
        """"""
        name = input('Enter character name')
        answer = input('Generate a character from the depths of the deepest,\
            darkest entropy? y/n')

        #In Progress, the below section will not do anything remotely good and is currently a mess
        while True:
            try:
                answer = str.lower(answer)


        if answer == 'y':
            return character.new_char(name, True, True)

        elif answer == 'n':
            print()

        else:
            print('Please enter a valid answer, y or n')
