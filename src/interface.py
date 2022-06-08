#!/usr/bin/env python

from utils.utilities import parse_recipe, print_recipe
import sys
from termcolor import colored
import shutil
import validators

termsize = shutil.get_terminal_size().columns
url = sys.argv[1]
if not validators.url(url):
    sys.exit('Not a valid URL')

recipe = parse_recipe(url)
print_recipe(recipe, termsize, 'green', 'blue')

print(colored("What transformation do you want to perform? Avalable options:".center(termsize),'green'))
print(colored("To vegitarian (Enter 1)",'blue'))
print(colored("To non-vegitarian (Enter 2)",'red'))
print(colored("To healthy (Enter 3)",'blue'))
print(colored("To unhealthy (Enter 4)",'red'))
print(colored("To Italian (Enter 5)",'blue'))

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

# TODO: Add transform calls here, based on user input
