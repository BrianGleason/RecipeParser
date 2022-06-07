# will substitute all instances of given cooking method in recipe for preferred substitute.
import sys
import os
from utils.utilities import parse_recipie, get_all_urls



def get_heating_temp_estimator(remove_method, step_list):
    for step in step_list:
        step_split = step.split(" ")
        step_split_lower = step.lower().split(" ")

def main():
    args = sys.argv
    print(args)
    if len(args) != 4:
        print('must provide 3 additional arguments: url, cooking method to be changed, cooking method to use instead')
        return
    url = args[1]
    remove_method = args[2]
    add_method = args[3]

    recipe = parse_recipie(url)
    print(recipe)

    heating_temp = get_heating_temp_estimator(remove_method, recipe['Instructions'])

    if heating_temp != None:
        pass

main()