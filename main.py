from tkinter import *

from Database.word import WordList
from pages import *

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    words = WordList("data/words.xml","data/status.xml")
    words.read()

    root = Tk()

    root.geometry("400x100")

    study_pg = Study_Page(words)

    select_pg = Select_Page(study_pg)
    add_pg = Add_page_AddWordToData(words)

    entrance_pg = Entrance_Page(root,add_pg,select_pg)
    entrance_pg.start()

    words_onlyIndex = words.GetIndexList()
    audio_pg = Audio_Download_Page(words_onlyIndex,"audios")

    audio_pg.start()
    # print(words.GetIdOf("comprise"))
    root.mainloop()



