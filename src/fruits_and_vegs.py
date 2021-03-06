from utils.utilities import parse_recipe
from nltk.stem import PorterStemmer
import os

ps = PorterStemmer()

def get_food_item(url, food_file_path):
    recipe = parse_recipe(url)
    with open(os.path.dirname(__file__) + food_file_path, encoding='utf-8') as food_file:
        lines = food_file.readlines()
    outputlist = set()
    for ingredientdict in recipe["Ingredients"]:
        ingredient = ingredientdict["name"]
        for line in lines:
            stemmedingredient = ' '.join(map(ps.stem, ingredient.lower().split()))
            stemmedline = ' '.join(map(ps.stem, line.lower().split()))
            if(stemmedline in stemmedingredient):
                outputlist.add(stemmedline)
            elif(stemmedingredient in stemmedline.split(" ")):
                outputlist.add(stemmedingredient)
    return outputlist

#citation: list of fruits and vegetables from https://vegetablesfruitsgrains.com/
def getveggies(url):
    return get_food_item(url, f'/../lists/formatted_veg_list.txt')


def getfruits(url):
    return get_food_item(url, f'/../lists/formatted_fruit_list.txt')

if __name__ == '__main__':
    url = "https://www.allrecipes.com/recipe/73303/mexican-rice-iii/"
    print("Vegetables:")
    print(getveggies(url))
    print("\nFruits:")
    print(getfruits(url))

