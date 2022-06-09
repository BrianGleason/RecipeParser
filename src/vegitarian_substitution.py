import json
import os
import random

import nltk
from collections import Counter

from utils.utilities import replace_all


def to_vegetarian(recipe):
    subs = open(os.path.dirname(__file__) + f'/../lists/vegetarian_subs.json', encoding='utf-8')
    subs_dict = json.load(subs)
    ingredients = recipe['Ingredients']
    for ingredient in ingredients:
        if ingredient['contains']['Meat']:
            replace = _get_sub(ingredient['name'], subs_dict)
            replace_all(recipe, ingredient['name'], replace)


def _get_sub(name, subs_dict):
    # check for exact match sub, if not then partial sub, if not then assign tofu sub
    l_name = name.lower()
    tokens = nltk.word_tokenize(l_name)
    text = nltk.Text(tokens)
    tags = dict(nltk.pos_tag(text))
    counts = Counter(tag for word, tag in tags.items())
    if l_name in subs_dict:
        return subs_dict[l_name]
    sl_name = l_name.split()
    changed_name = l_name
    for meat in subs_dict.keys():
        for token in sl_name:
            if token in meat:
                tag = tags[token]
                if tag in ['NN', 'NNS'] and counts['NN'] + counts['NNS'] > 1:
                    changed_name = changed_name.replace(token, '')
                elif tag in ['JJ', 'JJR', 'JJS']:
                    changed_name = changed_name.replace(token, 'vegetarian')
                else:
                    changed_name = changed_name.replace(token, subs_dict[meat])
    return "tofu" if changed_name == l_name else changed_name

def from_vegetarian(recipe):
    ingredients = recipe['Ingredients']
    for ingredient in ingredients:
        if ingredient['contains']['Meat']: return

    protein_data = open(os.path.dirname(__file__) + f'/../lists/formatted_proteins_list.json', encoding='utf-8')
    protein_dict = json.load(protein_data)

    vegetable_data = open(os.path.dirname(__file__) + f'/../lists/formatted_veg_list.txt', encoding='utf-8')
    vegetable_list = vegetable_data.read().splitlines()
    vegetable_list = [vegetable.lower() for vegetable in vegetable_list]

    fruit_data = open(os.path.dirname(__file__) + f'/../lists/formatted_fruit_list.txt', encoding='utf-8')
    fruit_list = fruit_data.read().splitlines()
    fruit_list = [fruit.lower() for fruit in fruit_list]

    meats = protein_dict['meat-fish']
    ingredients = recipe['Ingredients']
    for ingredient in ingredients:
        if ingredient['type'] == 'Natural/Organic Foods' or ingredient['name'] in fruit_list or ingredient['name'] in vegetable_list:
            meat = random.choice(meats)
            replace_all(recipe, ingredient['name'], meat)
            return
    for ingredient in ingredients:
        if ingredient['name'] in fruit_list or ingredient['name'] in vegetable_list:
            meat = random.choice(meats)
            replace_all(recipe, ingredient['name'], meat)
            return

    replace_all(recipe, random.choice(ingredients)['name'], random.choice(meats))