import sys
import os
import re
import json
from utils.utilities import parse_recipie, get_all_urls
from fruits_and_vegs import getfruits, getveggies


def main():
    cooking_methods_tools_data = open(os.path.dirname(__file__) + f'/../lists/primary_cooking_methods_tools.json')
    italian_cuisine_data = open(os.path.dirname(__file__) + f'/../lists/italian_cuisine_ingredients.json')
    cmt_dict = json.load(cooking_methods_tools_data)

    args = sys.argv
    print(args)
    if len(args) != 2:
        print('must provide 1 additional arguments: allrecipes url')
        return
    url = args[1]

    recipe = parse_recipie(url)
    print(recipe)
    ingredients = recipe['Ingredients']
    vegetable_list = getveggies(url)
    fruit_list = getfruits(url)
    print(vegetable_list)
    print(fruit_list)
    for ingredient in ingredients:
        if ingredient in vegetable_list:
            pass
        if ingredient in fruit_list:
            pass
        if is_protein(ingredient):
            pass
        if is_sauce(ingredient):
            pass
        if is_seasoning(ingredient):
            pass
        if is_grain(ingredient):
            pass

    for step in recipe['Instructions']:
        print(step)


main()