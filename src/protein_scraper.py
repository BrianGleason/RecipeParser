import json

import requests
from bs4 import BeautifulSoup

# Find meats fish
URL = 'https://www.listchallenges.com/160-types-of-meat-what-kind-of-meat-have-you-tried/list/'
proteins = {}
proteins['meat-fish'] = []
for i in range(1, 5):
    page = requests.get(URL + str(i))
    soup = BeautifulSoup(page.content, 'html.parser')
    divs = soup.find_all(class_ = "item-name")
    for div in divs:
        proteins['meat-fish'].append(div.text.strip().lower())

proteins['eggs'] = ['egg']

# Find dairy products
URL = 'https://en.wikipedia.org/wiki/List_of_dairy_products'
proteins['dairy'] = []
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')
dairies = soup.select('tbody tr td:nth-of-type(1) > a')
for dairy in dairies:
    proteins['dairy'].append(dairy.text.strip().lower())

# Find Seeds and Nuts
URL = 'https://www.adducation.info/mankind-nature-general-knowledge/edible-nuts-and-seeds/'
proteins['nuts-seeds'] = []
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')
nuts = soup.select('tbody tr td:nth-of-type(1) strong:nth-of-type(1)')
for nut in nuts:
    proteins['nuts-seeds'].append(nut.text.strip().lower())

# Find Legumes
URL = 'https://nutritionrefined.com/legumes-list/'
legume_set = set()
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')
legumes = soup.select('.entry-content h4')
for legume in legumes:
    str = legume.text.strip()
    if str == '': continue
    if '(' in str:
        legume_split = str.split('(')
        legume_name = legume_split[0].strip()
        legume_subnames = legume_split[1].strip(')')
        legume_sublist = legume_subnames.split(',')
        legume_set.add(legume_name)
        for subname in legume_sublist:
            legume_set.add(subname.strip().lower())
    else:
        legume_set.add(str)
proteins['legumes'] = list(legume_set)

with open('../lists/formatted_proteins_list.json', 'w') as f:
    json.dump(proteins, f, ensure_ascii=False)
