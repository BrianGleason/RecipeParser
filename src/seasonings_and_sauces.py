from nltk.stem import PorterStemmer
import os
import json
   
ps = PorterStemmer()

def get_food_item(recipe, food_file_path, key):
    with open(os.path.dirname(__file__) + food_file_path) as food_file:
        data = json.load(food_file)
        lines = data[key]
    outputlist = set()
    for ingredientdict in recipe["Ingredients"]:
        ingredient = ingredientdict["name"]
        for line in lines:
            if line in ingredient:
                outputlist.add(line)
            if ingredient in line:
                outputlist.add(ingredient)
    return outputlist

#citation: list of fruits and vegetables from https://vegetablesfruitsgrains.com/
def get_sauces(recipe):
    return get_food_item(recipe, f'/../lists/sauces.json', "sauces")


def get_herbs_spices(url):
    return get_food_item(url, f'/../lists/herbs_spices.json', "herbs and spices")