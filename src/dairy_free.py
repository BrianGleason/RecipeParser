from utils.utilities import parse_recipie, replace_ingredient, replace_ingredient_list, get_all_urls
import json

def make_dairy_free(recipe):
    dairy_free_data = open("lists/lactose_list.json")
    df_dict = json.load(dairy_free_data)
    dairy_free_data.close()
    cheese_file = open('lists/cheese_list.txt')
    cheeses = cheese_file.readlines()
    cheese_file.close()
    for ing in df_dict:
        replace_ingredient(recipe['Instructions'], ing, df_dict[ing])
        replace_ingredient_list(recipe['Ingredients'], ing, df_dict[ing])
    
    for cheese in cheeses:
        cheese = cheese.lower().strip() + ' cheese'
        replace_ingredient(recipe['Instructions'], cheese, 'dairy free ' + cheese)
        replace_ingredient_list(recipe['Ingredients'], cheese, 'dairy free ' + cheese)
    

if __name__ == '__main__':
    urls = get_all_urls()
    for url in urls:
        print(url)
        recipe = parse_recipie(url)
        print("Ingredients:\n")
        print(list(map(lambda i: i['name'], recipe["Ingredients"])))
        make_dairy_free(recipe)
        print(list(map(lambda i: i['name'], recipe["Ingredients"])))


