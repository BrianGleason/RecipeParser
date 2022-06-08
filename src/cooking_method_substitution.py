# will substitute all instances of given cooking method in recipe for preferred substitute.
import sys
import os
import re
import json
from utils.utilities import parse_recipe, get_all_urls

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


def main():
    cooking_methods_tools_data = open(os.path.dirname(__file__) + f'/../lists/primary_cooking_methods_tools.json', encoding='utf-8')
    cmt_dict = json.load(cooking_methods_tools_data)

    args = sys.argv
    print(args)
    if len(args) != 4:
        print('must provide 3 additional arguments: url, cooking method to be changed, cooking method to use instead')
        return
    url = args[1]
    remove_method = args[2]
    remove_tools = []
    if remove_method in cmt_dict: remove_tools = cmt_dict[remove_method]
    add_method = args[3]
    add_tool = None
    if add_method in cmt_dict:
        add_tool = cmt_dict[add_method][0]
    else:
        print('lacking information on what kitchen tools are used with this method, results may include incorrect kitchen tools')


    recipe = parse_recipe(url)
    print(recipe)

    heating_temp = get_heating_temp_estimator(remove_method, remove_tools, recipe['Instructions'], recipe['Substeps'])
    print("HEATING TEMP", heating_temp)

    if heating_temp != None:
        pass
    for substep_list in recipe['Substeps']:
        for substep in substep_list:
            substep_lower = []
            for substep_step in substep:
                substep_lower.append(substep_step.lower())
            # if any remove tools are in substep
            if len([i for i in remove_tools if i in substep_lower]) > 0:
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
                for tool in remove_tools:
                    if tool in substep_lower and add_tool != None:
                        tool_index = substep_lower.index(tool)
                        substep[tool_index] = add_tool

            # if the remove method is in substep
            if remove_method in substep_lower:
                attempts = 0
                while "degrees" in substep_lower or attempts > 3:
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
                remove_index = substep_lower.index(remove_method)
                substep[remove_index] = add_method
    print("AFTER", recipe['Substeps'])




main()
