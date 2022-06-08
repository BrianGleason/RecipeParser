#!/usr/bin/python

from utils.utilities import parse_recipe, print_recipe
import sys
from termcolor import colored
import shutil
import validators

termsize = shutil.get_terminal_size().columns
url = sys.argv[1]
transform = sys.argv[2]

if not validators.url(url):
    sys.exit('Not a valid URL')

recipe = parse_recipe(url)
print_recipe(recipe, termsize, 'green', 'blue')

# TODO: Add transform calls here, add transform argument
# Currently allowed transforms: vegitarian, healthy, italian
