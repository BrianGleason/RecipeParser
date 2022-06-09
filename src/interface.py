#!/usr/bin/env python3

import sys
from termcolor import colored
import shutil
import validators

from utils.utilities import parse_recipe, print_recipe
from healthy import serving_size, healthy_conversion
from vegitarian_substitution import to_vegetarian, from_vegetarian
from italian_cuisine_substitution import italian_cuisine_substitution
from cooking_method_substitution import method_interface

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
print("To Italian (Enter 3)")
print("To healthy (Enter 4)")
print("To unhealthy (Enter 5)")
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
    italian_cuisine_substitution(recipe, url)
elif transform == 4:
    healthy_conversion(recipe, "healthy", termsize)
elif transform == 5:
    healthy_conversion(recipe, "unhealthy", termsize)
elif transform == 6:
    serving_size(recipe, termsize)
elif transform == 7:
    method_interface(recipe, termsize)
elif transform == 8:
    # TODO: Transform to lactose free
    sys.exit('Unsupported')

print_recipe(recipe, termsize, 'green', 'blue')
