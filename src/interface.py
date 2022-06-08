#!/usr/bin/env python3

from utils.utilities import parse_recipe, print_recipe
from quantity import quantity_mod
import sys
from termcolor import colored
import shutil
import validators
from vegitarian_substitution import to_vegetarian, from_vegetarian
from italian_cuisine_substitution import italian_cuisine_substitution

termsize = shutil.get_terminal_size().columns
print(colored("Enter an All Recipes URL:".center(termsize), 'green'))
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
print("Change serving amount (Enter 6)")
print("Change cooking method (Enter 7)")
print("To lactose-free (Enter 8)")

while True:
    try:
        transform = int(input('Your choice (1-8): '))
        assert 0 < transform < 9

    except ValueError:
        print("Please enter an integer.")
    except AssertionError:
        print("Please enter an integer 1-8")
    else:
        break

if transform == 1:
    to_vegetarian(recipe)
elif transform == 2:
    from_vegetarian(recipe)
elif transform == 3:
    # TODO: Transforrm to healthy
    sys.exit('Unsupported')
elif transform == 4:
    # TODO: Transform to unhealthy
    sys.exit('Unsupported')
elif transform == 5:
    italian_cuisine_substitution(recipe, url)
elif transform == 6:
    quantity_mod(recipe)
elif transform == 7:
    # TODO: Change cooking method
    sys.exit('Unsupported')
elif transform == 8:
    # TODO: Transform to lactose free
    sys.exit('Unsupported')

print_recipe(recipe, termsize, 'green', 'blue')
