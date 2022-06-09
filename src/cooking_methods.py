from utils.utilities import parse_recipe, get_all_urls, no_punctuation
import json


def get_cooking_method(url, cookingmethod_file_path):
    cooking_methods_tools_data = open(cookingmethod_file_path, encoding='utf-8')
    cmt_dict = json.load(cooking_methods_tools_data)
    recipe = parse_recipe(url)
    lines = set(cmt_dict)
    outputlist = []
    times = []
    time_priority = {
        'second' : 0,
        'seconds' : 0,
        'minute' : 1,
        'minutes' : 1,
        'hour' : 2,
        'hours' : 2
        }
    for instruction in recipe["Instructions"]:
        instruction = no_punctuation(instruction)
        lower_instruct = instruction.lower()
        splitinstruct = lower_instruct.split()
        saute = "skillet" in splitinstruct or "pan" in splitinstruct

        for i, word in enumerate(splitinstruct):
            to_append = None
            if word in lines:
                to_append = word
            elif word == "cook" and saute:
                to_append = "saute"

            found_timeword = False
            if to_append is not None:
                j = i + 1
                while j < len(splitinstruct):
                    if splitinstruct[j] in time_priority:
                        unit = time_priority[splitinstruct[j]]
                        j -= 1
                        while j >= 0:
                            time = splitinstruct[j]
                            if '-' in time:
                                time = time.rsplit('-', 1)[1]
                            try:
                                x = int(time)
                                times.append((unit, x))
                                found_timeword = True
                                break
                            except ValueError:
                                j -= 1

                        break
                    j += 1

            if found_timeword:
                outputlist.append(to_append)
    best_ind = 0
    for i in range(len(times)):
        if times[i] > times[best_ind]:
            best_ind = i
    return outputlist[best_ind]

def getprimarycookingmethod(url):
    return get_cooking_method(url, "lists/primary_cooking_methods_tools.json")

if __name__ == '__main__':
    urls = get_all_urls()
    for url in urls:
        print("\nPrimary cooking method:")
        print(url)
        print(getprimarycookingmethod(url))
