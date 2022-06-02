from bs4 import BeautifulSoup

import urllib.parse
import urllib.request

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
		
		ingredient['quantity'] = tag.findChild("input")['data-init-quantity']
		ingredient['unit'] = tag.findChild("input")['data-unit']
		ingredient['type'] = tag.findChild("input")['data-store_location']
		ingredients.append(ingredient)

	instructions = []
	for tag in instruction_tags:
		instructions.append(tag.find('p').getText())
	
	print(ingredients)
	print(instructions)
	return ingredients, instructions

# Testing functions
if __name__ == '__main__':
	globals()[sys.argv[1]](sys.argv[2])
