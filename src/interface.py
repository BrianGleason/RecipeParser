#!/usr/bin/env python3

from utils.utilities import parse_recipe, print_recipe
import sys
from termcolor import colored
import shutil
import validators
from vegitarian_substitution import to_vegetarian, from_vegetarian

termsize = shutil.get_terminal_size().columns
print(colored("Enter an All Recipes URL:", 'green'))
while True:
    try:
        url = input('URL: ')
        assert validators.url(url)
    except:
        print("Please enter a valid All Recipes URL.")
    else:
        break

recipe = parse_recipe(url)
print_recipe(recipe, termsize, 'green', 'red')

print(colored("What transformation do you want to perform? Avalable options:".center(termsize),'green'))
print("To vegitarian (Enter 1)")
print("To non-vegitarian (Enter 2)")
print("To healthy (Enter 3)")
print("To unhealthy (Enter 4)")
print("To Italian (Enter 5)")

while True:
    try:
        transform = int(input('Your choice (1,2,3,4,5): '))
        assert 0 < transform < 6
    except ValueError:
        print("Please enter an integer.")
    except AssertionError:
        print("Please enter an integer 1-5")
    else:
        break

if transform == 1:
    predicate = "Vegitarian"
    to_vegetarian(recipe)
elif transform == 2:
    predicate = "Non-vegitarian"
    from_vegetarian(recipe)
elif transform == 3:
    predicate = "Healthy"
    # TODO: Transforrm to healthy
elif transform == 4:
    predicate = "Unhealthy"
    # TODO: Transform to unhealthy
elif transform == 5:
    predicate = "Italian"
    # TODO: Transform to Italian

recipe['Name'] = predicate + " " + recipe['Name']
print_recipe(recipe, termsize, 'green', 'blue')
