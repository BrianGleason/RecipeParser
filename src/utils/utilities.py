import pymongo
client = pymongo.MongoClient('localhost:27017')
db = client["cooking_data"]
recipies = db["recipie_data"] # Contains recipies
nutrition = db["nutrition_data"] # Contains food deitary information
methods = db["method_methods"] # Contains methods and tools used in method

import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

from bs4 import BeautifulSoup

import urllib.parse
import urllib.request

from pprint import pprint

import sys

def parse_recipie(url):
    """Crawl url and insert recipie data into database collection.
    """
    req = urllib.request.Request(url)
    req.add_header('Cookie', 'euConsent=true')
    soup = BeautifulSoup(urllib.request.urlopen(req).read(), 'html.parser')

    title = soup.find('title').string
    ingredient_tags = soup.findAll("li", {"class": "ingredients-item"})
    instruction_tags = soup.findAll("li", {"class": "subcontainer instructions-section-item"})

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
        ingredients.append(ingredient)

    instructions = []
    for tag in instruction_tags:
        instructions.append(tag.find('p').getText())

    recipie = {
        'Name': title,
        'Ingredients': ingredients,
        'Instructions': instructions
    }
    pprint(recipie)

    # TODO: Duplicate detection
    recipies.insert_one(recipie)

def quantity_mod(ingredients, ratio):
    for ingredient in ingredients:
        if ingredient["quantity"]: ingredient["quantity"] *= ratio

    return ingredients

def replace_ingredient(instructions, target, substitute):
    for i, instruction in enumerate(instructions):
        if target in instruction:
            instructions[i] = instruction.replace(target, substitute)

# TODO Change to cooking method / tools allowed_targets to database
def instruction_subject(instructions, allowed_targets, word_tags):
    """ Word identification used for finding cooking methods and tools.
    """
    # TODO Primary and secondary targets, groups
    targets = []
    for instruction in instructions:
        verbs = [a[0] for a in nltk.pos_tag(nltk.word_tokenize(instruction)) if a[1] in word_tags]
        targets.append([a for a in verbs if a in allowed_targets])
    return targets

# TODO Change to database lookup
def ingredient_classifier(ingredient):
    # Hopefully all the hardcoded garbage can go in this function.
    # There are useful and non-useful categories. "Soup" is not useful because soup can contain meat or gluten,
    # i.e. "beef broth" is not vegitarian

    diet = {
        'Name': ingredient['name'],
        'Contains' : {'Meat': None, 'Gluten': None, 'Lactose': None},
        'Healthy' : 2
    }

    match ingredient['type']:
        case 'Herbs and Spices' | 'Produce':
            diet['Contains']['Meat'] = False
            diet['Contains']['Gluten'] = False
            diet['Contains']['Lactose'] = False
            diet['Healthy'] = 3
        case 'Beverages' | 'Natural/Organic Foods' | 'Basic Cooking Ingredients':
            diet['Contains']['Meat'] = False
            diet['Contains']['Gluten'] = False
        case 'Meats, Fish and Seafood':
            diet['Contains']['Meat'] = True
            diet['Contains']['Gluten'] = False
            diet['Contains']['Lactose'] = False
            diet['Healthy'] = 1
        case 'Dairy, Eggs and Milk':
            diet['Contains']['Meat'] = False
            diet['Contains']['Gluten'] = False
            diet['Contains']['Lactose'] = True
            diet['Healthy'] = 1
    # Note: Baking Supplies, Ethnic Foods, Canned Foods, Soup indicate nothing about diet

    nutrition.insert_one(diet)

# Testing functions
if __name__ == '__main__':
    globals()[sys.argv[1]](sys.argv[2])
