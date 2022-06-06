from utils.utilities import parse_recipie
from nltk.stem import PorterStemmer
   
ps = PorterStemmer()

def get_food_item(url, food_file_path):
    recipe = parse_recipie(url)
    with open(food_file_path,"r") as food_file:
        lines = food_file.readlines()
    outputlist = set()
    for ingredientdict in recipe["Ingredients"]:
        ingredient = ingredientdict["name"]
        for line in lines:
            stemmedingredient = ' '.join(map(ps.stem, ingredient.lower().split()))
            stemmedline = ' '.join(map(ps.stem, line.lower().split()))
            if(stemmedline in stemmedingredient):
                outputlist.add(stemmedline)
    return outputlist

#citation: list of fruits and vegetables from https://vegetablesfruitsgrains.com/
def getveggies(url):
    return get_food_item(url, "lists/formatted_veg_list.txt")


def getfruits(url):
    return get_food_item(url, "lists/formatted_fruit_list.txt")

if __name__ == '__main__':
    url = "https://www.allrecipes.com/recipe/73303/mexican-rice-iii/"
    print("Vegetables:")
    print(getveggies(url))
    print("\nFruits:")
    print(getfruits(url))

