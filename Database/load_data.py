
import xml.etree.ElementTree as ET
def load_word(path):

    tree = ET.parse(path)
    root = tree.getroot()

    index_list = []
    meaning_list = []


    for unit in root:
        meaning = []
        for attribute in unit:
            if attribute.tag == "index":
                index_list.append(attribute.text)
            else:
                meaning.append(attribute.text)
        meaning_list.append(meaning)

    return index_list,meaning_list,root

def load_status(path):
    tree = ET.parse(path)
    root = tree.getroot()

    Okcnt_list = []
    status_list = []

    for unit in root:

        for attribute in unit:
            if attribute.tag == "Okcnt":
                Okcnt_list.append(int(attribute.text))
            elif attribute.tag == "InEasy":

                if attribute.text == "True":
                    status_list.append(1)
                else:
                    status_list.append(2)
            else:
                status_list.append(int(attribute.text))


    return Okcnt_list, status_list, root

def fromSaveGetListAndTarget(path):
    str = ""
    with open(path,"r",encoding='utf-8') as f:
        str = f.read()
    raw = str.split(",")
    id_list = []
    target = int(raw[0])
    id = 0
    time = 0
    for i in range(1,len(raw)):
        if raw[i] == '':
            continue
        if i % 2 == 1:
            id = int(raw[i])
        else:
            time = int(raw[i])
            id_list.append([id,time])
    return id_list,target
