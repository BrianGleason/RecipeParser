import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

from bs4 import BeautifulSoup

import urllib.parse
import urllib.request

from pprint import pprint

import sys

def parse_recipie(url):

	req = urllib.request.Request(url)
	req.add_header('Cookie', 'euConsent=true')
	soup = BeautifulSoup(urllib.request.urlopen(req).read(), 'html.parser')

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

	pprint(ingredients)
	pprint(instructions)
	return ingredients, instructions

def food_diet(ingredient):
	# TODO: return all deitary restrictions category allows, healthy/non-healthy instead of keyword
	# See examples below.
	# There are useful and non-useful categories. "Soup" is not useful because soup can contain meat or gluten,
	# i.e. "beef broth" is not vegitarian

	if ingredient["type"] == "Beverages":
		return "beverage"
	elif ingredient["type"] == "Produce":
		return "vegan"
	elif ingredient["type"] == "Herbs and Spices":
		return "condiment"
	elif ingredient["type"] == "Meats, Fish and Seafood":
		return "non-vegan"
	elif ingredient["type"] == "Basic Cooking Ingredients":
		return "condiment"
	elif ingredient["type"] == "Dairy, Eggs and Milk":
		return "non-vegan"
	elif ingredient["type"] == "Baking Supplies":
		return "glutenous"
	elif ingredient["type"] == "Canned Foods":
		return None
	elif ingredient["type"] == "Soup":
		return None

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
