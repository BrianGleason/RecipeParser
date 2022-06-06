from utils.utilities import parse_recipie, get_all_urls
from nltk.stem import PorterStemmer
   
ps = PorterStemmer()

def get_cooking_method(url, cookingmethod_file_path):
    recipe = parse_recipie(url)
    with open(cookingmethod_file_path,"r") as cookingmethod_file:
        lines = cookingmethod_file.readlines()
    outputlist = set()
    for instruction in recipe["Instructions"]:
        lower_instruct = instruction.lower()
        stemmedinstruction = ' '.join(map(ps.stem, lower_instruct.split()))
        non_es = ['saut', 'bast', 'brais']
        for word in non_es:
            if word in stemmedinstruction:
                outputlist.add(word + 'e')
        for line in lines:
            format_line = line.lower().strip()
            if(format_line in stemmedinstruction):
                outputlist.add(format_line)

        if ("cook" in stemmedinstruction and 
            ("skillet" in stemmedinstruction or "pan" in lower_instruct)):
            outputlist.add("saute")
    return outputlist

def getprimarycookingmethod(url):
    return get_cooking_method(url, "lists/primary_cooking_methods_list.txt")

if __name__ == '__main__':
    # ps.stem('pan')
    urls = get_all_urls()
    for url in urls:
        print("\nPrimary cooking method:")
        print(url)
        print(getprimarycookingmethod(url))
