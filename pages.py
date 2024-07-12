from tkinter import *
from Database.word import WordList,Word
from Database.load_data import fromSaveGetListAndTarget
from Database.save import save_condition
import os
from Download import Downloader
import pygame

from moviepy.editor import AudioFileClip, concatenate_audioclips

EASY_STATUS = 0
NORMAL_STATUS = 1
HARD_STATUS = 2


import random
class Entrance_Page:
    def __init__(self,root,sub_add,sub_select):
        self.root = root
        self.AddWordSubPage = sub_add
        self.SelectStudySubPage = sub_select
        self.frame = None


        self.ButtonSwitchToStudy = None
        self.ButtonSwitchToAdd = None

    def start(self):
        self.ArrangeDesign()

        self.BindCommand()

    def ArrangeDesign(self):
        self.frame = Frame(self.root)
        self.frame.pack(padx=10, pady=10)
        self.ButtonSwitchToStudy = Button(self.frame, text="学习单词", width=20, height=2)
        self.ButtonSwitchToAdd = Button(self.frame, text="添加新单词", width=20, height=2)
        self.ButtonSwitchToStudy.pack(side=LEFT)
        self.ButtonSwitchToAdd.pack(side=LEFT)

    def BindCommand(self):
        self.ButtonSwitchToStudy.config(command = lambda :self.Switch_To_New_Page(self.SelectStudySubPage))
        self.ButtonSwitchToAdd.config(command = lambda :self.Switch_To_New_Page(self.AddWordSubPage))

    def Switch_To_New_Page(self,New_Page):
        New_Page.start()
        self.root.destroy()
class Add_page_AddWordToData:
    def __init__(self,wordData):
        self.root = None
        self.frame = None
        self.Entry_Index = None
        self.Entry_Meanings = []
        self.Button_Next = None
        self.Label_AddCnt = None
        self.AddCnt = 0
        self.word_data = wordData

    def start(self):
        self.ArrangeDesign()

        self.BindCommand()




    def ArrangeDesign(self):
        self.root = Tk()
        self.frame = Frame(self.root)
        self.frame.pack()

        self.Entry_Index = Entry(self.frame,width = 80,font = ("宋体",38))
        for i in range(9):
            self.Entry_Meanings.append(Entry(self.frame,width = 60,font = ("宋体",18)))
        self.Button_Next = Button(self.frame,text = "下一个单词",width = 20,height = 2)
        self.Label_AddCnt = Label(self.frame,text = f"已添加{self.AddCnt}个单词")
        self.root.geometry("600x600")

        self.Entry_Index.pack(pady = 6)
        for i in range(9):
            self.Entry_Meanings[i].pack(pady = 3)

        self.Button_Next.pack(pady = 30)
        self.Label_AddCnt.pack()



    def BindCommand(self):
        self.Button_Next.bind("<Button-1>",self.SaveAndClearAndRefocus)
        self.Button_Next.bind("<Return>",self.SaveAndClearAndRefocus)
        self.Entry_Index.bind("<Down>",self.focus_next_widget)
        for i in range(9):
            self.Entry_Meanings[i].bind("<Down>", self.focus_next_widget)

    def SaveAndClearAndRefocus(self,event):
        index = self.GetIndex()
        meanings = self.GetMeanings()

        if index == "":
            return

        self.word_data.new_words.append(Word(index,0,2,meanings))

        self.word_data.save_status()
        self.word_data.save_word_and_clear_stored_new_word()


        self.ClearAllEntry()

        self.Entry_Index.focus_set()

        self.refreshLabel()

    def focus_next_widget(self,event):
        event.widget.tk_focusNext().focus()
        return "break"

    def GetIndex(self):
        return self.Entry_Index.get()
    def GetMeanings(self):
        meanings = []
        for i in range(9):
            if self.Entry_Meanings[i].get() != '':
                meanings.append(self.Entry_Meanings[i].get())
        return meanings
    def ClearAllEntry(self):
        self.Entry_Index.delete(0,'end')
        for i in range(9):
            self.Entry_Meanings[i].delete(0,'end')

    def refreshLabel(self):
        self.AddCnt += 1
        self.Label_AddCnt.config(text = f"已添加{self.AddCnt}个单词")

class Select_Page:
    def __init__(self,study_root):
        self.root = None
        self.frameOnTheHead = None
        self.frameBelow = None
        self.Button_Normal = None
        self.Button_Easy = None
        self.Button_Hard = None
        self.Button_Load = None

        self.study_root = study_root

    def start(self):
        self.ArrangeDesign()

        self.BindCommand()

    def ArrangeDesign(self):
        self.root = Tk()
        self.frameOnTheHead = Frame(self.root)
        self.frameBelow = Frame(self.root)
        self.Button_Normal = Button(self.frameBelow, text="复习认识单词")
        self.Button_Easy = Button(self.frameBelow, text="复习熟悉单词")
        self.Button_Hard = Button(self.frameBelow, text="复习生词")
        self.Button_Load = Button(self.frameOnTheHead, text="载入先前进度")

        self.root.geometry("400x400")
        self.frameOnTheHead.pack()
        self.frameBelow.pack()
        self.Button_Easy.pack(side=LEFT, pady=60, padx=10)
        self.Button_Normal.pack(side=LEFT, pady=60, padx=10)
        self.Button_Hard.pack(side=LEFT, pady=60, padx=10)
        self.Button_Load.pack(side=LEFT, padx=0)

    def BindCommand(self):
        self.Button_Normal.config(command = lambda :self.Switch_To_Study_Page(self.study_root,"Normal"))
        self.Button_Easy.config(command = lambda :self.Switch_To_Study_Page(self.study_root,"Easy"))
        self.Button_Hard.config(command = lambda :self.Switch_To_Study_Page(self.study_root,"Hard"))
        self.Button_Load.config(command = lambda :self.Switch_To_Study_Page(self.study_root,"Load"))

    def Switch_To_Study_Page(self,New_Page,type):
        New_Page.start(type)
        self.root.destroy()

class Study_Page:
    def __init__(self,word_data):
        self.path = os.getcwd()
        self.root = None
        self.word_data = word_data
        self.type = None

        self.frame_above = None
        self.frame_below = None
        self.frame_lowest = None

        self.label_index = None
        self.label_meaning_list = []
        self.label_remain = None
        self.label_group_remain = None
        self.label_all_word_num = None

        self.button_know = None
        self.button_show = None
        self.button_not_know = None
        self.button_save = None
        self.button_audio = None
        self.button_addToAudioMakeList = None
        self.button_generateAudio = None

        self.front_list = []
        self.wait_front_list = []
        self.audio_list = []

        self.position = 0


    def start(self,type):
        pygame.init()
        pygame.mixer.init()
        self.ArrangeDesign()

        self.type = type

        self.loadTargetedWord()
        self.showWordNum()

        self.refreshGroupLabel()

        self.refreshIndexAndRemainLabel()

        self.BindCommand()

    def ArrangeDesign(self):
        self.root = Tk()


        self.frame_above = Frame(self.root)
        self.frame_below = Frame(self.root)
        self.frame_lowest = Frame(self.root)
        self.button_show = Button(self.frame_below, text="展示释义", width=10, height=2)
        self.button_know = Button(self.frame_below, text="认识", width=10, height=2)
        self.button_not_know = Button(self.frame_below, text="不认识", width=10, height=2)
        self.button_save = Button(self.frame_below, text="保存", width=10, height=2)
        self.button_audio = Button(self.frame_below, text="发音", width=10, height=2)
        self.button_addToAudioMakeList = Button(self.frame_lowest, text="加入诵读", width=10, height=2)
        self.button_generateAudio = Button(self.frame_lowest, text="生成音频", width=10, height=2)
        self.label_remain = Label(self.frame_below, text="",font=("宋体", 20))

        self.label_group_remain = Label(self.frame_lowest, text="111111111", font=("宋体", 20))
        self.label_all_word_num = Label(self.frame_lowest,font = ("宋体",20),text = "")
        for i in range(9):
            self.label_meaning_list.append(Label(self.frame_above, text="", font=("宋体", 20)))
        self.label_index = Label(self.frame_above, text="",
                                 font=("Arial", 34))

        self.root.geometry("900x800")

        self.frame_above.pack()
        self.label_index.pack(pady=10)
        for i in range(9): self.label_meaning_list[i].pack(pady=10)

        self.frame_below.pack()
        self.button_know.pack(padx=40, side=LEFT)
        self.button_show.pack(padx=40, side=LEFT)
        self.button_not_know.pack(padx=40, side=LEFT)
        self.label_remain.pack(padx=40, side=LEFT)
        self.button_save.pack()
        self.button_audio.pack()

        self.frame_lowest.pack(padx=(300, 0))
        self.label_group_remain.pack(side=LEFT)
        self.label_all_word_num.pack(side = BOTTOM)
        self.button_addToAudioMakeList.pack()
        self.button_generateAudio.pack()

    def loadTargetedWord(self): # 0熟悉,1认识,2生词
        target = -1
        if self.type == 'Easy': target = EASY_STATUS
        elif self.type == 'Normal': target = NORMAL_STATUS
        elif self.type == 'Hard': target = HARD_STATUS

        if target != -1:
            # 找到目标词汇的编号
            for i in range(len(self.word_data)):

                if self.word_data.words[i].status == target:
                    self.front_list.append([i,-1])

            # 开始打乱顺序
            random.shuffle(self.front_list)

        else:
            self.front_list,target = fromSaveGetListAndTarget("data/save.txt")
            self.setType(target)

        if len(self.front_list) > 50:
            self.wait_front_list = self.front_list[50:]
            self.front_list = self.front_list[:50]

    def setType(self,target):
        if target == EASY_STATUS:
            self.type = "Easy"
        elif target == NORMAL_STATUS:
            self.type = "Normal"
        elif target == HARD_STATUS:
            self.type = "Hard"
    def showWordNum(self):
        self.label_all_word_num.config(text = f"共{len(self.front_list) + len(self.wait_front_list)}个单词")
    def BindCommand(self):
        self.button_save.config(command = lambda :self.savePresentCondition())
        self.button_show.config(command = lambda :self.show_meaning())
        self.button_know.config(command = lambda :self.goto_next_known())
        self.button_not_know.config(command = lambda : self.goto_next_unknown())
        self.button_audio.config(command = lambda: self.playSound())
        self.button_addToAudioMakeList.config(command = lambda:self.addToAudioGenerationList())
        self.button_generateAudio.config(command = lambda :self.generateAudio())

    def show_meaning(self):
        if self.position >= len(self.front_list):
            return

        id = self.front_list[self.position][0]
        word = self.word_data.words[id]

        for i in range(min(9,len(word.meanings))):
            self.label_meaning_list[i].config(text = word.meanings[i])

    def goto_next_unknown(self):
        # 避免超数组错误
        if self.position >= len(self.front_list):
            return

        # 更新单词状态为不会
        id = self.front_list[self.position][0]
        self.word_data.words[id].status = 2
        self.word_data.words[id].Okcnt = 0
        if self.type == "Hard":
            self.wait_front_list.append([id,2])
        # 只有复习生词的时候会回滚

        for i in range(9):
            self.label_meaning_list[i].config(text = "")
        self.position += 1

        # 在复习完一组之后装载新的一组
        if self.position >= len(self.front_list):
            if len(self.wait_front_list) > 0:
                self.word_data.save_status()
                self.reloadFrontList()
                self.refreshGroupLabel()
            else:
                self.showEnd()

        self.refreshIndexAndRemainLabel()


    def goto_next_known(self):
        if self.position >= len(self.front_list):
            return
        id = self.front_list[self.position][0]

        # 调整单词状态，并且调整复习的状态
        if self.front_list[self.position][1] > 0:
            self.wait_front_list.append((id,self.front_list[self.position][1] - 1))
        elif self.front_list[self.position][1] == -1:
            # 初次见面便答对，连对次数加一
            self.word_data.words[id].Okcnt += 1
            if self.word_data.words[id].Okcnt >= 3:
                self.word_data.words[id].Okcnt = 0
                self.word_data.words[id].status = max(0,self.word_data.words[id].status - 1)
                # 归入下一档， 最低为零

        for i in range(9):
            self.label_meaning_list[i].config(text = "")
        self.position += 1

        # 复习完本组，重新装载或者直接结束
        if self.position >= len(self.front_list):
            if len(self.wait_front_list) > 0:
                self.word_data.save_status()
                self.reloadFrontList()
                self.refreshGroupLabel()
            else:
                self.showEnd()

        self.refreshIndexAndRemainLabel()

    def playSound(self):
        filename = str(self.front_list[self.position][0]) + '.mp3'
        track = pygame.mixer.music.load(f"audios/{filename}")
        pygame.mixer.music.play(loops=1)
        # 播放音频文件


    def addToAudioGenerationList(self):
        self.audio_list.append(self.front_list[self.position][0])

    def generateAudio(self):
        audio_clips = []
        for id in self.audio_list:
            filename = str(id) + '.mp3'
            clip1 = AudioFileClip(f"{self.path}/audios/{filename}")
            audio_clips.append(clip1)
        concatenated_clip = concatenate_audioclips(audio_clips)
        concatenated_clip.write_audiofile('concatenated_audio.mp3')
    def reloadFrontList(self):
        self.position = 0
        self.front_list = []
        for i in range(min(50,len(self.wait_front_list))):
            self.front_list.append(self.wait_front_list[i])
        if len(self.wait_front_list) > 50:
            self.wait_front_list = self.wait_front_list[50:]
        else:
            self.wait_front_list = []
        random.shuffle(self.front_list)



    def showEnd(self):
        self.label_index.config(text="你已经复习完所有单词", font=("宋体", 34))

    def refreshGroupLabel(self):
        groupNum = (len(self.front_list) + len(self.wait_front_list)) / 50
        if groupNum > int(groupNum):
            groupNum = int(groupNum) + 1
        else:
            groupNum = int(groupNum)
        self.label_group_remain.config(text = f"剩余{groupNum}组")
    def refreshIndexAndRemainLabel(self):
        id = self.front_list[self.position][0]
        self.label_index.config(text=self.word_data.words[id].index)
        self.label_remain.config(text=f"本组剩余{len(self.front_list) - self.position - 1}个单词")



    def savePresentCondition(self):
        save_condition(self.front_list[self.position:],self.wait_front_list,"data/save.txt",self.type)
        self.word_data.save_status()


class Audio_Download_Page:
    def __init__(self,word_index_list,audio_path):
        self.word_index_list = word_index_list
        self.audio_path = audio_path
        self.root = None
        self.Text = None
        self.Button = None

    def start(self):
        self.Arrange_Design_Except_Button()

        numOfWords = len(self.word_index_list)
        numOfAudio = len(self.GetAudioNames())

        if numOfAudio == numOfWords:
            self.SetLabelAs("均具备音频，无须下载")

        elif numOfAudio < numOfWords:
            self.SetLabelAs(f"需下载{numOfWords - numOfAudio}份音频，是否下载?")
            self.Arrange_Download_Button()

        else:
            self.SetLabelAs(f"出现问题")

    def Arrange_Design_Except_Button(self):
        self.root = Tk()
        self.root.geometry("700x200")
        self.root.title("音频下载窗口")

        self.Text = Label(self.root,text = "",font = ("宋体",34))
        self.Text.pack()

    def Arrange_Download_Button(self):
        self.Button = Button(self.root,text = "下载",command = lambda :self.Download_Audio(),width = 10,height = 2)

        self.Button.pack()

    def Download_Audio(self):
        quryString_list,audio_name_list = self.Prepare_Download_Infos()

        download_task = Downloader(quryString_list,audio_name_list)

        download_task.download()
        download_task.save(self.audio_path)

    def GetAudioNames(self):
        audios = os.listdir(self.audio_path)
        return audios

    def SetLabelAs(self,show):
        self.Text.config(text = show)

    def Prepare_Download_Infos(self):
        qurystring_list = []
        id_list = []
        idOfWords_haveAudio = self.extractSortedIds(self.GetAudioNames())

        cnt = 0
        for i in range(len(self.word_index_list)):
            if len(idOfWords_haveAudio) == 0:
                qurystring_list.append({"lan":"uk","text":self.word_index_list[i],"spd":"3","source":"wise"})
                id_list.append(i)

            elif idOfWords_haveAudio[cnt] == i:
                if cnt < len(idOfWords_haveAudio) - 1:
                    cnt += 1
                i += 1
            else:
                qurystring_list.append({"lan":"uk","text":self.word_index_list[i],"spd":"3","source":"wise"})
                id_list.append(i)
        return qurystring_list,id_list

    def extractSortedIds(self,name_list):
        id_list = []
        for name in name_list:
            id = int(name[:-4])
            id_list.append(id)
        id_list.sort()
        return id_list


        

