"""
Hopefully where the magic happens.
"""

import character
import json
from os import listdir

file = []

if __name__ == '__main__':

    saves = listdir(savedata)

    #checks to see if a saved character exists and if so, if the user want to load
    #that character or make a new one
    #LATER GOING TO BE GUI
    if saves == []:
        print('loading new character route')

    else:
        mychar = new_or_load()


    def new_or_load():
        """"""
        while(True):
            usersays = input('Enter 1 to make a new character. Enter 2 to load' +\
            'a character.')

            if usersays != '1' or usersays != '2':
                print('Invalid input')
            else:
                break

        if usersays == '1':
            print('loading new character route')

        elif usersays == '2':
            loadfile = saves[loadthis()]

            return character.load_char(loadfile)


    def loadthis():
        """"""
        while(True):
            print('Enter the number of the character you would like to load.')

            for i in saves:
                print(str(saves.index(i)) + ')' + str(i))

            usersays = input()

            if int(usersays) >= len(saves):
                print('Please enter a valid number')
            else:
                break

        return int(usersays)


    def new_route():
        """"""
        name = input('Enter character name')
        answer = input('Create random character? y/n')

        if answer == 'y':
            return character.new_char(name)

        elif answer == 'n':
            print()

        else:
            print('Please enter a valid answer, y or n')
