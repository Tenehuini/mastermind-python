import argparse
from curses.ascii import isdigit
import os
import signal
import sys

from random import randint


CLEAR_SCREEN = "clear"

LETTERS = ['A', 'B', 'C', 'D', 'E', 'F']
NUMBERS = [1, 2, 3, 4, 5, 6]

USE_LETTERS = False


parser = argparse.ArgumentParser(description="Optional arguments")
parser.add_argument('--letters', type=bool, help='Optional argument to use letters instead of numbers')
parser.add_argument('--duplicates', type=bool, help='Optional argument to use duplicate numbers (or letters) on the code to break')


def new_game(use_letters=False, allow_duplicates=False):
    tries = 0

    code = generate_code(use_letters, allow_duplicates)
    
    guess = []

    while guess != code:
        tries += 1
        print(f"Guess the hidden code using: {LETTERS if use_letters else NUMBERS}")
        guess = get_guess(use_letters)
        correctness = get_correctness(code, guess)
        print_correctness(correctness)
        if correctness[0] == 4:
            break

    print(f"Congratulations, you found the hidden code in {tries} tries")


def print_correctness(correctness):
    print(f"Correct color and correct position -> {correctness[0]}")
    print(f"Correct color incorrect position -> {correctness[1]}")


def get_correctness(code, guess):
    guess = guess.split()
    copy_code = code.copy()
    correct_position = 0
    incorrect_position = 0

    for index, c in enumerate(copy_code):
        if guess[index] == str(c):
            correct_position += 1
        elif str(c) in guess:
            incorrect_position += 1

    return (correct_position, incorrect_position)


def is_valid_guess(use_letters, guess):
    guesses = guess.split()

    if len(guesses) != 4:
        return False

    for g in guesses:
        if len(g) > 1:
            return False
    
    if use_letters:
        return all(list(map(str.isalpha, guesses)))
    else:
        return all(list(map(str.isdigit, guesses)))


def get_guess(use_letters):
    guess = []

    while True:
        guess = input(f"Enter your guess, separated by spaces: ")
        if is_valid_guess(use_letters, guess):
            break

    return guess


def generate_code(use_letters, allow_duplicates):
    return generate_random_code(LETTERS if use_letters else NUMBERS, allow_duplicates)


def generate_random_code(values, allow_duplicates):
    list_of_values = values.copy()
    code = []

    if not allow_duplicates:
        code.append(list_of_values.pop(randint(0, len(list_of_values) - 1)))
        code.append(list_of_values.pop(randint(0, len(list_of_values) - 1)))
        code.append(list_of_values.pop(randint(0, len(list_of_values) - 1)))
        code.append(list_of_values.pop(randint(0, len(list_of_values) - 1)))
    else:
        code.append(list_of_values[randint(0, len(list_of_values) - 1)])
        code.append(list_of_values[randint(0, len(list_of_values) - 1)])
        code.append(list_of_values[randint(0, len(list_of_values) - 1)])
        code.append(list_of_values[randint(0, len(list_of_values) - 1)])

    return code


def print_rules():
    """Prints the rules"""
    pass


def signal_handler(signal, frame):
    """Signal handler for CTRL+C to clear the screen and exit"""
    os.system(CLEAR_SCREEN)
    sys.exit(0)


def not_valid_initial_choice(choice):
    """Checks that the initial choice is new game (G) or read the rules (R)"""
    if choice.upper() == "G" or choice.upper() == "R":
        return False
    return True


def main(use_letters, allow_duplicates):
    signal.signal(signal.SIGINT, signal_handler)

    choice = input("New Game (G) or Read the Rules (R): ")
    while not_valid_initial_choice(choice):
        input()
    if choice.upper() == "G":
        new_game(use_letters, allow_duplicates)
    else:
        print_rules()


if __name__ == "__main__":
    args = parser.parse_args()
    main(args.letters, args.duplicates)
