# will substitute all instances of given cooking method in recipe for preferred substitute.
import sys
import os
import re
import json
from utils.utilities import parse_recipe, get_all_urls

def untokenize(words):
    """
    This function was taken from stackoverflow
    """
    text = ' '.join(words)
    step1 = text.replace("`` ", '"').replace(" ''", '"').replace('. . .',  '...')
    step2 = step1.replace(" ( ", " (").replace(" ) ", ") ")
    step3 = re.sub(r' ([.,:;?!%]+)([ \'"`])', r"\1\2", step2)
    step4 = re.sub(r' ([.,:;?!%]+)$', r"\1", step3)
    step5 = step4.replace(" '", "'").replace(" n't", "n't").replace(
         "can not", "cannot")
    step6 = step5.replace(" ` ", " '")
    return step6.strip()

def compose_substeps_into_instructions(recipe):
    substep_matrix = recipe['Substeps']
    new_instructions = []
    for step in substep_matrix:
        new_step = ""
        for substep in step:
            substep_string = untokenize(substep)
            if len(substep_string) > 0 and substep_string[-1] != ".":
                substep_string = substep_string + "."
            if new_step == "":
                new_step = new_step + substep_string
            else:
                new_step = new_step + " " + substep_string

        new_instructions.append(new_step)

    recipe['Instructions'] = new_instructions

def fahrenheit_estimate(num):
    if num >= 400:
        return "high"
    elif num >= 300:
        return "medium"
    else:
        return "low"

def celsius_estimate(num):
    pass

def get_heating_temp_estimator(remove_method, remove_tools, step_list, substep_matrix):
    remove_method = remove_method.lower()
    for index in range(len(step_list)):
        step = step_list[index]
        step_np = re.sub(r'[^\w\s]', '', step)

        substep_list = substep_matrix[index]
        step_split_npl = step_np.lower().split(" ")
        if remove_method in step_split_npl or len([i for i in remove_tools if i in step_split_npl]) > 0:
            if "degrees" in step_split_npl:
                deg_index = step_split_npl.index("degrees")
                if deg_index > 0 and step_split_npl[deg_index - 1].isnumeric():
                    # if farenheit
                    if deg_index + 1 < len(step_split_npl) and (step_split_npl[deg_index + 1] == "fahrenheit" or step_split_npl[deg_index + 1] == "f"):
                        return fahrenheit_estimate(int(step_split_npl[deg_index - 1]))
                    # if celcius
                    if deg_index + 1 < len(step_split_npl) and (step_split_npl[deg_index + 1] == "celsius" or step_split_npl[deg_index + 1] == "c"):
                        return celsius_estimate(int(step_split_npl[deg_index - 1]))

            if "high" in step_split_npl and "medium" in step_split_npl: return "medium high"
            if "medium" in step_split_npl and "low" in step_split_npl: return "medium low"
            if "high" in step_split_npl: return "high"
            if "medium" in step_split_npl: return "medium"
            if "low" in step_split_npl: return "low"

def handle_heat(substep_lower, substep, heating_temp):
    attempts = 0
    while "degrees" in substep_lower and attempts < 3:
        attempts += 1
        # deal with heating
        deg_index = substep_lower.index("degrees")
        if deg_index > 0 and substep_lower[deg_index - 1].isnumeric():
            # if farenheit
            if deg_index + 1 < len(substep_lower) and ("fahrenheit" in substep_lower[deg_index + 1] or substep_lower[deg_index + 1] == "f"):
                del substep[deg_index + 1]
                substep[deg_index] = heating_temp
                del substep[deg_index - 1]
            # if celcius
            if deg_index + 1 < len(substep_lower) and ("celsius" in substep_lower[deg_index + 1] or substep_lower[deg_index + 1] == "c"):
                del substep[deg_index + 1]
                substep[deg_index] = heating_temp
                del substep[deg_index - 1]

        if "(" in substep: substep.remove("(")
        if ")" in substep: substep.remove(")")

def substitute_cooking_method(recipe, add_method, remove_method):

    cooking_methods_tools_data = open(os.path.dirname(__file__) + f'/../lists/primary_cooking_methods_tools.json', encoding='utf-8')
    cmt_dict = json.load(cooking_methods_tools_data)

    remove_tools = []
    remove_covers = []
    remove_places = []
    remove_containers = []
    if remove_method in cmt_dict: 
        remove_tools = cmt_dict[remove_method]['appliance']
        remove_covers = cmt_dict[remove_method]['cover']
        remove_places = cmt_dict[remove_method]['place']
        remove_containers = cmt_dict[remove_method]['container']
    add_tool = None
    add_cover = None
    add_place = None
    add_container = None
    if add_method in cmt_dict:
        add_tool = cmt_dict[add_method]['appliance'][0]
        add_cover = cmt_dict[add_method]['cover'][0]
        add_place = cmt_dict[add_method]['place'][0]
        add_container = cmt_dict[add_method]['container'][0]
    else:
        print('lacking information on what kitchen tools are used with this method, results may include incorrect kitchen tools')

    heating_temp = get_heating_temp_estimator(remove_method, remove_tools, recipe['Instructions'], recipe['Substeps'])

    if heating_temp != None:
        pass
    for substep_list in recipe['Substeps']:
        for substep in substep_list:
            substep_lower = []
            for substep_step in substep:
                substep_lower.append(substep_step.lower())
            # if any remove tools are in substep
            tool_or_method_flag = False
            if len([i for i in remove_tools if i in substep_lower]) > 0:
                tool_or_method_flag = True
                for tool in remove_tools:
                    if tool in substep_lower and add_tool != None:
                        tool_index = substep_lower.index(tool)
                        substep[tool_index] = add_tool
                handle_heat(substep_lower, substep, heating_temp)

            # if the remove method is in substep
            if remove_method in substep_lower:
                tool_or_method_flag = True
                substep_lower, substep, heating_temp
                remove_index = substep_lower.index(remove_method)
                substep[remove_index] = add_method
            
            # if tool or method present, look for replacement places and covers/doors
            if tool_or_method_flag:
                if len([i for i in remove_places if i in substep_lower]) > 0:
                    for place in remove_places:
                        if place in substep_lower and add_place != None:
                            place_index = substep_lower.index(place)
                            substep[place_index] = add_place
                if len([i for i in remove_covers if i in substep_lower]) > 0:
                    for cover in remove_covers:
                        if cover in substep_lower and add_cover != None:
                            cover_index = substep_lower.index(cover)
                            substep[cover_index] = add_cover
                if len([i for i in remove_containers if i in substep_lower]) > 0:
                    for container in remove_containers:
                        if container in substep_lower and add_container != None:
                            container_index = substep_lower.index(container)
                            substep[container_index] = add_container
                    
    compose_substeps_into_instructions(recipe)
    #print("AFTER", recipe['Instructions'])


def main():
    args = sys.argv
    print(args)
    if len(args) != 4:
        print('must provide 3 additional arguments: url, cooking method to be changed, cooking method to use instead')
        return
    url = args[1]
    remove_method = args[2]
    add_method = args[3]
    recipe = parse_recipe(url)

    substitute_cooking_method(recipe, add_method, remove_method)

main()
