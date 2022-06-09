from decimal import Decimal
import os
import json
import random
import sys

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

    if method == 1:
        healthy_data = open(os.path.dirname(__file__) + f'/../lists/healthy_conservative.json', encoding='utf-8')
        healthy_dict = json.load(healthy_data)

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
                if any((match := food) in ingredient['name'] for food in healthy_dict.keys()):
                    if conversion == "healthy":
                        ingredient['name'] = random.choice(healthy_dict[match])

                    elif conversion == "unhealthy": quantity_mod(ingredient['quantity'], 2)
            elif method == 2:
                sys.exit('Unsupported')

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
