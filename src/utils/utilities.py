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

    return recipie

def quantity_mod(ingredients, ratio):
    for ingredient in ingredients:
        if ingredient["quantity"]: ingredient["quantity"] *= ratio

    return ingredients

def replace_ingredient(instructions, target, substitute):
    for i, instruction in enumerate(instructions):
        if target in instruction:
            instructions[i] = instruction.replace(target, substitute)

def instruction_subject(instructions, allowed_targets, word_tags):
    """ Word identification used for finding cooking methods and tools.
    """
    # TODO Primary and secondary targets, groups
    targets = []
    for instruction in instructions:
        verbs = [a[0] for a in nltk.pos_tag(nltk.word_tokenize(instruction)) if a[1] in word_tags]
        targets.append([a for a in verbs if a in allowed_targets])
    return targets

def populate_diets():
    """Manually populate array with hardcoded values. Subject to change.
    Hopefully all the arbitary choices can stay here.

    Usually populating comes in a separate step, but becuase the arbitary nature
    of choosing certain values (like healthy scores) I've manually added code here.

    There are useful and non-useful categories. "Soup" is not useful because soup can
     contain meat or gluten, i.e. "beef broth" is not vegitarian.
    Baking Supplies, Ethnic Foods, Canned Foods, Soup indicate nothing about diet

    This means there are "Category" types and "Specifier" types.
    Specifiers should have either a T/F in each contains key-value.
    """

    nutrition = []
    nutrition.append({
        'Name': 'Herbs and Spices',
        'Type': 'Category',
        'Contains': {'Meat': False, 'Gluten': False, 'Lactose': False},
        'Healthy' : 3
    })
    nutrition.append({
        'Name': 'Produce',
        'Type': 'Category',
        'Contains': {'Meat': False, 'Gluten': False, 'Lactose': False},
        'Healthy': 3
    })
    nutrition.append({
        'Name': 'Beverages',
        'Type': 'Category',
        'Contains': {'Meat': False, 'Gluten': False, 'Lactose': None},
        'Healthy': 2
    })
    nutrition.append({
        'Name': 'Natural/Organic Foods',
        'Type': 'Category',
        'Contains': {'Meat': False, 'Gluten': False, 'Lactose': None},
        'Healthy': 3
    })
    nutrition.append({
        'Name': 'Basic Cooking Ingredients',
        'Type': 'Category',
        'Contains': {'Meat': False, 'Gluten': False, 'Lactose': None},
        'Healthy': 2
    })
    nutrition.append({
        'Name': 'Meats, Fish and Seafood',
        'Type': 'Category',
        'Contains': {'Meat': True, 'Gluten': False, 'Lactose': False},
        'Healthy': 1
    })
    nutrition.append({
        'Name': 'Dairy, Eggs and Milk',
        'Type': 'Category',
        'Contains': {'Meat': False, 'Gluten': False, 'Lactose': True},
        'Healthy': 1
    })

    return nutrition

def get_all_urls():
    urllist =  ["https://www.allrecipes.com/recipe/24074/alysias-basic-meat-lasagna/",
                "https://www.allrecipes.com/recipe/244716/shirataki-meatless-meat-pad-thai/",
                "https://www.allrecipes.com/recipe/16167/beef-bourguignon-i/",
                "https://www.allrecipes.com/recipe/228285/teriyaki-salmon/",
                "https://www.allrecipes.com/recipe/229293/korean-saewoo-bokkeumbap-shrimp-fried-rice/",
                "https://www.allrecipes.com/recipe/7757/tiramisu-cheesecake/",
                "https://www.allrecipes.com/recipe/73303/mexican-rice-iii/"]
    return urllist
# Testing functions
if __name__ == '__main__':
    globals()[sys.argv[1]](sys.argv[2])
