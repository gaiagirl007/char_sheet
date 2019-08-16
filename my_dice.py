"""This 'rolls' dice."""

import random

def roll(num, max):
    """Generates a random number between 1 and max, num times.
    Adds and returns the results

    num: int > 0
    max: int > 1"""
    assert type(num) == int and num > 0
    assert type(max) == int and max > 1

    total = 0
    for i in range(num):
        total += random.randint(1, max)

    return total


def roll_dice(num_dice, max_value):
    """Prints the results of 'roll' function

    num_dice: int > 0
    max_value: int > 1"""
    assert type(num_dice) == int and num_dice > 0
    assert type(max_value) == int and max_value > 1

    print(num_dice, "d", max_value, " = ", roll(num_dice, max_value))


def roll_stats():
    """Uses the 'roll' function to roll 1d6 4 times, dropping the lowest
    value. Prints the sum of the remaining 3. Completes 6 times."""
    stats = []

    for i in range(6):

        single = []
        for j in range(4):
            single.append(roll(1, 6))

        single.sort()

        best_total = 0
        for k in range(1, 4):
            best_total += single[k]

        stats.append(best_total)

    return stats


def character():
    print(str(roll_stats()))
