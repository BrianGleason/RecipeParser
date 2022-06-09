from decimal import Decimal
import os
import json
import random
import sys
from utils.utilities import replace_ingredient, replace_ingredient_list

def healthy_conversion(recipe, conversion):
    """Converts foods to healthy/unhealthy based on 2 methods.

    Valid conversions: "healthy" or "unhealthy"
    User input: "conservative (1)" or "aggressive (2)"

    Healthy/unhealthy in changes serving size by 0.75/1.25

    Per ingredient changes:
    Conservative, to healthy: converts unhealthy (condiment) ingredients to healthy ingredients
    Conservative, to unhealthy: increases the amount of unhealthy ingredients
    Aggressive, to healthy/unhealthy: finds a case of each category, and replaces that case
    with a healthy/unhealthy alternative
    """

    while True:
        try:
            method = int(input('Please select an conversion method: conservative (Enter 1) or aggressive (Enter 2): '))
            assert 0 < method < 3
        except ValueError:
            print("Please enter an integer.")
        except AssertionError:
            print("Please enter an integer 1-2")
        else:
            break

    cons_dict = json.load(open(os.path.dirname(__file__) + f'/../lists/healthy_conservative.json', encoding='utf-8'))
    aggro_dict = json.load(open(os.path.dirname(__file__) + f'/../lists/healthy_aggressive.json', encoding='utf-8'))
    aggro_categories = list(aggro_dict.keys())

    # Full recipe modifications
    if conversion == "healthy":
        recipe['Name'] = "Healthy " + recipe['Name']
        quantity_full(recipe, Decimal(0.75))
    elif conversion == "unhealthy":
        recipe['Name'] = "Unhealthy " + recipe['Name']
        quantity_full(recipe, Decimal(1.25))

    # Per ingredient modifications
    for ingredient in recipe['Ingredients']:
        if method == 1:
            if any((match := food) in ingredient['name'] for food in cons_dict.keys()):
                if conversion == "healthy":
                    ingredient['name'] = random.choice(cons_dict[match])
                    # replacement = random.choice(cons_dict[match])
                    # replace_ingredient(recipe['Instructions'], ingredient['name'], replacement)
                    # replace_ingredient_list(recipe['Ingredients'], ingredient['name'], replacement)

                elif conversion == "unhealthy": quantity_mod(ingredient, 2)

        elif method == 2:
            if any((match := category) == ingredient['type'] for category in aggro_categories):
                # Limit to one replacement per category
                aggro_categories.remove(match)

                if conversion == "healthy":
                    ingredient['name'] = random.choice(aggro_dict[match]['Healthy'])
                    # replacement = random.choice(aggro_dict[match]['Healthy'])
                    # replace_ingredient(recipe['Instructions'], ingredient['name'], replacement)
                    # replace_ingredient_list(recipe['Ingredients'], ingredient['name'], replacement)

                elif conversion == "unhealthy":
                    ingredient['name'] = random.choice(aggro_dict[match]['Unhealthy'])
                    # replacement = random.choice(aggro_dict[match]['Unhealthy'])
                    # replace_ingredient(recipe['Instructions'], ingredient['name'], replacement)
                    # replace_ingredient_list(recipe['Ingredients'], ingredient['name'], replacement)

def serving_size(recipe):
    while True:
        try:
            ratio = Decimal(input('Enter a ratio (0.5 for half, 2 for double): '))
        except ValueError:
            print("Please enter a valid decimal.")
        else:
            break

    quantity_full(recipe, ratio)
    recipe['Name'] = "Smaller/Larger " + recipe['Name']

def quantity_full(recipe, ratio):
    for ingredient in recipe['Ingredients']:
        quantity_mod(ingredient, ratio)

def quantity_mod(ingredient, ratio):
    if ingredient["quantity"]:
        ingredient["quantity"] = str(Decimal(ingredient["quantity"].strip(' "')) * ratio)
