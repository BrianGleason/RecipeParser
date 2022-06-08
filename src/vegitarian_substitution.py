import os 
import json
import sys
from utils.utilities import parse_recipe, replace_ingredient, replace_ingredient_list, print_recipe

def main():
    protein_data = open(os.path.dirname(__file__) + f'../lists/formatted_proteins_list.json')
    protein_dict = json.load(protein_data)
    meats = protein_dict['meat-fish']

    args = sys.argv
    print(args)
    if len(args) != 2:
        print('must provide 1 additional arguments: allrecipes url')
        return
    url = args[1]

    recipe = parse_recipe(url)
    ingredients = recipe['Ingredients']
    instructions = recipe['Instructions']
    for ingredient in ingredients:
        if ingredient['contains']['Meat']:
            replace_ingredient(instructions, ingredient['name'], 'tofu')
            replace_ingredient_list(ingredients, ingredient['name'], 'tofu')
    print_recipe

if __name__ == '__main__':
    main()