import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["cooking_data"]
recipies = db["recipie_data"]
diets = db["diet_data"]

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

def food_classifier(ingredient):
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
        case 'Beverages':
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
        case 'Baking Supplies':
            diet['Contains']['Meat'] = False
            diet['Contains']['Gluten'] = True
            diet['Contains']['Lactose'] = True
    # Basic Cooking Ingredients, Canned Foods, Soup indicate nothing

    diets.insert_one(diet)

def quantity_mod(ingredients, ratio):
    for ingredient in ingredients:
        if ingredient["quantity"]: ingredient["quantity"] *= ratio

    return ingredients

def cooking_method(instruction):
    # TODO Add more cooking methods
    allowed_methods = ["marinade","preheat","bake","skillet"]
    verb_tags = ["NN","NNP"]
    verbs = [a[0] for a in nltk.pos_tag(nltk.word_tokenize(instruction)) if a[1] in verb_tags]
    methods = [a for a in verbs if a in allowed_methods]
    # TODO Group cooking methods like bake/preheat
    # TODO Primary and secondary methods
    return methods

# Testing functions
if __name__ == '__main__':
    globals()[sys.argv[1]](sys.argv[2])
