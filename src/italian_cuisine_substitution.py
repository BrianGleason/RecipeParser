from dataclasses import replace
import sys
import os
import re
import json
from utils.utilities import parse_recipie, get_all_urls, replace_ingredient, replace_ingredient_list
from fruits_and_vegs import getfruits, getveggies
from seasonings_and_sauces import get_herbs_spices, get_sauces

def is_subword(subword, list):
    for element in list:
        if subword in element and len(subword) > 2:
            return True
    return False

def list_not_in_word(list, word):
    for element in list:
        if element in word:
            return True
    return False

def process_name(name, name_split, type_list, replace_dict, substitute_list):
    if substitute_list == []: return
    flag = False
    if name in type_list:
        replace_dict[name] = substitute_list[0]
        flag = True
    for type in type_list:
        if type in name:
            replace_dict[type] = substitute_list[0]
            flag = True
            added = (type, substitute_list[0])
            if substitute_list == []: return
    if flag: 
        substitute_list.pop(0)
        return True
    return False


def main():
    cooking_methods_tools_data = open(os.path.dirname(__file__) + f'/../lists/primary_cooking_methods_tools.json')
    italian_cuisine_data = open(os.path.dirname(__file__) + f'/../lists/italian_cuisine_ingredients.json')
    cmt_dict = json.load(cooking_methods_tools_data)
    italian_dict = json.load(italian_cuisine_data)


    args = sys.argv
    print(args)
    if len(args) != 2:
        print('must provide 1 additional arguments: allrecipes url')
        return
    url = args[1]

    recipe = parse_recipie(url)
    ingredients = recipe['Ingredients']
    instructions = recipe['Instructions']
    vegetable_list = getveggies(url)
    seasonings_list = get_herbs_spices(recipe)
    sauces_list = get_sauces(recipe)
    substitute_vegetable_list = list(italian_dict['vegetables'].keys())
    substitute_seasoning_list = list(italian_dict['herbs and seasonings'].keys())
    substitute_sauce_list = list(italian_dict['sauces'].keys())
    for ingredient in ingredients:
        if ingredient['name'] in substitute_vegetable_list:
            substitute_vegetable_list.remove(ingredient['name'])
        if ingredient['name'] in substitute_seasoning_list:
            substitute_seasoning_list.remove(ingredient['name'])
        if ingredient['name'] in substitute_sauce_list:
            substitute_sauce_list.remove(ingredient['name'])
    if 'sauce' in substitute_sauce_list: substitute_sauce_list.remove('sauce')
    if 'sauce' in sauces_list: sauces_list.remove('sauce')
    all_italian_ingredients_list = []
    for category, val in italian_dict.items():
        for element in list(val.keys()):
            all_italian_ingredients_list.append(element)

    replace_dict = dict()

    print('BEFORE ITALIAN TRANSLATION:')
    for step in instructions:
        print(step)
    for ingredient in ingredients:
        name = ingredient['name']
        name_split = name.split(" ")

        if name not in all_italian_ingredients_list:

            if process_name(name, name_split, vegetable_list, replace_dict, substitute_vegetable_list): continue
            if process_name(name, name_split, seasonings_list, replace_dict, substitute_seasoning_list): continue
            if process_name(name, name_split, sauces_list, replace_dict, substitute_sauce_list): continue
        '''
        if is_protein(ingredient):
            pass
        if is_sauce(ingredient):
            pass
        if is_seasoning(ingredient):
            pass
        if is_grain(ingredient):
            pass
        '''

    sorted_replace_dict = {}
    for k in sorted(replace_dict, key=len, reverse=True):
        sorted_replace_dict[k] = replace_dict[k]
    for key, value in sorted_replace_dict.items():
        replace_ingredient(instructions, key, value)
        replace_ingredient_list(ingredients, key, value)
    print(sorted_replace_dict)
    print('AFTER ITALIAN TRANSLATION')
    for step in recipe['Instructions']:
        print(step)


main()