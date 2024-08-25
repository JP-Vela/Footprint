
from transformers import pipeline

qa_model = pipeline("question-answering")

def find_name_with_qa(text):
    result = qa_model(question="what is the user's name?", context=text)
    return result['answer']





from json_parser import read_json_as_dict
from bs4 import BeautifulSoup

config = read_json_as_dict("config.json")
bio_words = config["bio_words"]
name_words = config["name_words"]

#Put the ids and classes into a dictionary with the id and class
# being the key and the value being the content (ChatGPT generated)
def extract_ids_and_classes(html_content):
    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Initialize dictionaries to store ids and classes
    ids_dict = {}
    classes_dict = {}
    
    lookedat = []

    # Iterate over all elements with an id attribute and collect the ids and their contents
    for element in soup.find_all(True, id=True):
        id_value = element.get('id')
        if id_value not in ids_dict:
            lookedat.append(element)
            ids_dict[id_value] = element.text.strip()
    
    # Iterate over all elements with a class attribute and collect the classes and their contents
    for element in soup.find_all(True, class_=True):
        classes = element.get('class')
        for cls in classes:
            if cls not in classes_dict and element not in lookedat:
                classes_dict[cls] = element.text.strip()

    ids_dict.update(classes_dict)
    return ids_dict


def extract(text):
    total = {
        "bio":"",
        "name":""
        }

    #page_outputs\\test2.html
    #with open(filepath, "r", encoding="utf-8") as f:
        #text = f.read()
    ids = extract_ids_and_classes(text)

    bioadded = False
    nameadded = False
    
    # print("Looking through ids: ")
    for id in ids.keys():
        for word in bio_words:
            if word in id and ids[id] not in total["bio"]:
                total["bio"] += ids[id]+", "
                bioadded = True
            

        for word in name_words:
            if word in id and ids[id] not in total["name"]:
                total["name"] += ids[id]+", "
                nameadded = True
    if bioadded:
        total["bio"] = total["bio"].replace("  ", " ")[:-2]
    if nameadded:
        total["name"] = total["name"].replace("  ", " ")[:-2]

    try:
        total["name guess"] = find_name_with_qa(str(total["bio"])+" "+str(total["name"]))
    except:
        total["name guess"] = ""
        
    return total
    # print(total["bio"])
    # print(total["name"])