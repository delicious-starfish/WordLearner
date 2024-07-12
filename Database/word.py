from Database.load_data import load_word,load_status
import xml.etree.ElementTree as ET
class Word:
    def __init__(self,index,Okcnt,status,meanings):
        self.index = index
        self.Okcnt = Okcnt
        self.status = status
        self.meanings = meanings


class WordList:
    def __init__(self,wordPath,statusPath):
        self.words = []
        self.word_path = wordPath
        self.status_path = statusPath
        self.word_root = None
        self.status_root = None
        self.new_words = []

    def __len__(self):
        return len(self.words)
    def read(self):
        index_list,meaning_list,self.word_root = load_word(self.word_path)
        Okcnt_list,status_list,self.status_root = load_status(self.status_path)

        for i in range(len(index_list)):
            self.words.append(Word(index_list[i],Okcnt_list[i],status_list[i],meaning_list[i]))


    def save_word_and_clear_stored_new_word(self):
        # TODO: 保存时缺少word
        for word in self.new_words:
            word_block = ET.SubElement(self.word_root,'word')
            word_block.tail = '\n'
            index = ET.SubElement(word_block,'index')
            index.text = word.index
            index.tail = '\n'

            for meaning in word.meanings:
                meanings = ET.SubElement(word_block,'meaning')
                meanings.text = meaning
                meanings.tail = '\n'

        tree = ET.ElementTree(self.word_root)
        tree.write(self.word_path, encoding='utf-8', xml_declaration=True)

        self.words.extend(self.new_words)
        self.new_words = []

    def save_status(self):
        for i,unit in enumerate(self.status_root):
            for attrib in unit:
                if attrib.tag == 'Okcnt':
                    attrib.text = str(self.words[i].Okcnt)
                elif attrib.tag == 'InEasy':
                    attrib.tag = 'status'
                    attrib.text = str(self.words[i].status)

                else:
                    attrib.text = str(self.words[i].status)

        for word in self.new_words:
            word_block = ET.SubElement(self.status_root, 'word')
            word_block.tail = '\n'

            Okcnt = ET.SubElement(word_block, 'Okcnt')
            Okcnt.text = str(word.Okcnt)
            Okcnt.tail = '\n'

            status = ET.SubElement(word_block, 'status')
            status.text = str(word.status)
            status.tail = '\n'

        tree = ET.ElementTree(self.status_root)
        tree.write(self.status_path, encoding='utf-8', xml_declaration=True)

    def GetIndexList(self):
        index_list = []
        for word in self.words:
            index_list.append(word.index)
        return index_list
    def GetIdOf(self,word_index):
        id_list = []
        for i,word in enumerate(self.words):
            if word.index == word_index:
                id_list.append(i)
        return id_list