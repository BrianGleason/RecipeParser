from ast import parse
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

from bs4 import BeautifulSoup

import urllib.parse
import urllib.request

import requests
_usda_key = "KCB7Ijl50I1oHVbmgjD6VGguegsxW34dKMwtfPt1"

from pprint import pprint

import sys
import string

def parse_recipie(url):
    """Crawl url and return recipie data
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

        # TODO: Add identification passes to ingredients here
        ingredient['contains'] = {'Meat': None, 'Gluten': None, 'Lactose': None}
        ingredient['method'] = None

        ingredients.append(ingredient)

    instructions = []
    for tag in instruction_tags:
        instructions.append(tag.find('p').getText())

    recipie = {
        'Name': title,
        'Ingredients': ingredients,
        'Instructions': instructions
    }
    recipie['Substeps'] = parse_substeps(recipie['Instructions'])
    # pprint(recipie)

    return recipie

def query_fooddata(ingredient):
    """Query USDA FoodData Central with ingredient name.
    """
    response = requests.post(
        r'https://api.nal.usda.gov/fdc/v1/search',
        params = {'api_key': _usda_key},
        json = {'generalSearchInput': ingredient["name"]}
    )
    return response.json()

def quantity_mod(ingredients, ratio):
    for ingredient in ingredients:
        if ingredient["quantity"]: ingredient["quantity"] *= ratio

    return ingredients

def replace_ingredient(instructions, target, substitute):
    for i, instruction in enumerate(instructions):
        lowered = instruction.lower()
        if target in lowered:
            instructions[i] = lowered.replace(target, substitute)

def replace_ingredient_list(ingredients, target, substitute):
    for i, ingredient in enumerate(ingredients):
        lowered = ingredient['name'].lower()
        if target in lowered:
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

# Example Call:
# `python3 src/utils/utilities.py parse_recipie https://www.allrecipes.com/recipe/228285/teriyaki-salmon/`
if __name__ == '__main__':
    globals()[sys.argv[1]](sys.argv[2])
