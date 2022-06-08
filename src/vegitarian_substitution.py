import json
import os
import random

from utils.utilities import replace_ingredient, replace_ingredient_list


def to_vegetarian(recipe):
    ingredients = recipe['Ingredients']
    instructions = recipe['Instructions']
    for ingredient in ingredients:
        if ingredient['contains']['Meat']:
            replace_ingredient(instructions, ingredient['name'], 'tofu')
            replace_ingredient_list(ingredients, ingredient['name'], 'tofu')

def from_vegetarian(recipe):
    protein_data = open(os.path.dirname(__file__) + f'/../lists/formatted_proteins_list.json')
    protein_dict = json.load(protein_data)
    meats = protein_dict['meat-fish']
    ingredients = recipe['Ingredients']
    instructions = recipe['Instructions']
    for ingredient in ingredients:
        if ingredient['type'] == 'Natural/Organic Foods':
            meat = random.choice(meats)
            replace_ingredient(instructions, ingredient['name'], meat)
            replace_ingredient_list(ingredients, ingredient['name'], meat)
