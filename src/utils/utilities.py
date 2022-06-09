from ast import parse

import nltk
nltk.download('punkt', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)

import urllib.parse
import urllib.request

import requests
from bs4 import BeautifulSoup

_usda_key = "KCB7Ijl50I1oHVbmgjD6VGguegsxW34dKMwtfPt1"

import json
import os
import shutil
import string
import sys
import re
from pprint import pprint

from termcolor import colored


def recipe_interface(url):
    """Testing interface for recipe collection. Use the separate interface.py for a more
    robust solution with support for transforms.

    Example Call:
    `python3 src/utils/utilities.py recipe_interface https://www.allrecipes.com/recipe/228285/teriyaki-salmon/`
    """
    termsize = shutil.get_terminal_size().columns
    recipe = parse_recipe(url)
    print("Printing full recipe information:")
    pprint(recipe)
    print_recipe(recipe, termsize, 'green', 'blue')

def print_recipe(recipe, termsize, primary_color, secondary_color):
    print(colored(recipe['Name'].center(termsize),primary_color))

    print(colored('Ingredients'.center(termsize),primary_color))
    for ingredient in recipe['Ingredients']:
        statement = re.sub(' +', ' ', ingredient['quantity'] + " " + ingredient['unit']\
         + " " + ingredient['prep'] + " " + ingredient['name'])
        print(colored(statement, secondary_color))

    print(colored('Instructions'.center(termsize),primary_color))
    for i, instruction in enumerate(recipe['Instructions']):
        statement = "Step " + str(i + 1) + ": " + instruction
        print(colored(statement, secondary_color), end="\n\n")

def parse_recipe(url):
    """Crawl url and return recipe data
    """
    req = urllib.request.Request(url)
    req.add_header('Cookie', 'euConsent=true')
    soup = BeautifulSoup(urllib.request.urlopen(req).read(), 'html.parser')

    title = soup.find('title').string
    ingredient_tags = soup.findAll("li", {"class": "ingredients-item"})
    instruction_tags = soup.findAll("li", {"class": "subcontainer instructions-section-item"})
    potential_serving_size = soup.findAll("div", {"class": "recipe-adjust-servings__original-serving elementFont__fine"})[0].string
    potential_serving_sizes = [int(s) for s in potential_serving_size.split() if s.isdigit()]
    serving_size = None
    if len(potential_serving_sizes) > 0: serving_size = potential_serving_sizes[0]

    # (Additional info) Can include: Prep, Cook, Total, Servings, Yield
    cook_tags = soup.findAll("div", {"class": "recipe-meta-item-body elementFont__subtitle"})
    cook_metainfo = [(tag.contents[0].text) for tag in cook_tags]

    ingredients = []
    for tag in ingredient_tags:
        ingredient = {}

        try:
            ingredient['name'], ingredient['prep'] = tag.findChild("input")['data-ingredient'].split(",")
        except ValueError:
            ingredient['name'] = tag.findChild("input")['data-ingredient']
            ingredient['prep'] = ''

        ingredient['quantity'] = tag.findChild("input")['data-init-quantity']
        ingredient['unit'] = tag.findChild("input")['data-unit']
        ingredient['type'] = tag.findChild("input")['data-store_location']

        # Add identification passes to ingredients here
        ingredient['contains'] = {'Meat': None, 'Gluten': None, 'Lactose': None}

        # Meat Identification
        protein_data = open(os.path.dirname(__file__) + f'/../../lists/formatted_proteins_list.json', encoding='utf-8')
        protein_dict = json.load(protein_data)
        meats = protein_dict['meat-fish']
        isMeat = ingredient['name'].lower().split() in meats or ingredient['type'] == 'Meats, Fish and Seafood'
        ingredient['contains']['Meat'] = isMeat

        # Lactose Identification
        dairy = protein_dict['dairy']
        isDairy = ingredient['name'].lower().split() in dairy or ingredient['type'] == 'Dairy, Eggs and Milk'
        ingredient['contains']['Lactose'] = isDairy

        ingredient['method'] = None
        ingredients.append(ingredient)

    instructions = []
    for tag in instruction_tags:
        instructions.append(tag.find('p').getText())
    substeps = parse_substeps(instructions)

    recipe = {
        'Name': title,
        'Ingredients': ingredients,
        'Instructions': instructions,
        'Substeps': substeps,
        'ServingSize' : serving_size
    }

    return recipe

def query_fooddata(ingredient):
    """Query USDA FoodData Central with ingredient name, returns relevant dietary information
    Note: long queries usually result in inaccurate results.
    """
    response = requests.post(
        r'https://api.nal.usda.gov/fdc/v1/search',
        params = {'api_key': _usda_key},
        json = {'generalSearchInput': ingredient["name"]}
    )

    # Save only top query
    food_data = response.json()['foods'][0]

    diet = {
        'Category': food_data.get('foodCategory', ''),
        'Score': food_data.get('score', ''),
        'Serving': food_data.get('servingSize', ''),
        'Unit': food_data.get('servingSizeUnit', '')
    }

    return diet

def replace_all(recipe, target, substitute):
    replace = re.compile(re.escape(target), re.IGNORECASE)
    for i, instruction in enumerate(recipe['Instructions']):
        recipe['Instructions'][i] = replace.sub(substitute, recipe['Instructions'][i])
    for i, ingredient in enumerate(recipe['Ingredients']):
        recipe['Ingredients'][i]['name'] = replace.sub(substitute, recipe['Ingredients'][i]['name'])

def replace_ingredient(instructions, target, substitute):
    for i, instruction in enumerate(instructions):
        lowered = instruction.lower()
        if target in lowered:
            instructions[i] = lowered.replace(target, substitute)

def replace_ingredient_list(ingredients, target, substitute, changedkey=None):
    for i, ingredient in enumerate(ingredients):
        lowered = ingredient['name'].lower()
        if target in lowered:
            if changedkey is not None:
                ingredients[i][changedkey] = True
            ingredients[i]['name'] = lowered.replace(target, substitute)

def instruction_subject(instructions, allowed_targets, word_tags):
    """ Word identification used for finding cooking methods and tools.
    """
    # TODO Primary and secondary targets, groups
    targets = []
    for instruction in instructions:
        verbs = [a[0] for a in nltk.pos_tag(nltk.word_tokenize(instruction)) if a[1] in word_tags]
        targets.append([a for a in verbs if a in allowed_targets])
    return targets

def parse_substeps(instructions):
    substep_matrix = []
    for step in instructions:
        substep_list = []
        text = nltk.word_tokenize(step)
        pos_tagged = nltk.pos_tag(text)
        substep_list.append(find_substep(0, pos_tagged))
        for index in range(1, len(pos_tagged)):
            if (pos_tagged[index][0] == ".") and index + 1 < len(pos_tagged):
                substep_list.append(find_substep(index + 1, pos_tagged))
        substep_matrix.append(substep_list)
    return substep_matrix

def find_substep(index, pos_tagged):
    substring = [pos_tagged[index][0]]
    index += 1
    while index + 1 < len(pos_tagged) and pos_tagged[index][0] != ".":
        substring.append(pos_tagged[index][0])
        index += 1
    substring.append(".")
    return substring

def get_all_urls():
    urllist =  ["https://www.allrecipes.com/recipe/24074/alysias-basic-meat-lasagna/",
                "https://www.allrecipes.com/recipe/244716/shirataki-meatless-meat-pad-thai/",
                "https://www.allrecipes.com/recipe/16167/beef-bourguignon-i/",
                "https://www.allrecipes.com/recipe/228285/teriyaki-salmon/",
                "https://www.allrecipes.com/recipe/229293/korean-saewoo-bokkeumbap-shrimp-fried-rice/",
                "https://www.allrecipes.com/recipe/7757/tiramisu-cheesecake/",
                "https://www.allrecipes.com/recipe/73303/mexican-rice-iii/"]
    return urllist


def no_punctuation(s):
    return s.translate(str.maketrans('', '', string.punctuation))

if __name__ == '__main__':
    globals()[sys.argv[1]](sys.argv[2])
