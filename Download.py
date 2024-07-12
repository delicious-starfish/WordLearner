from config import *
import concurrent.futures as cf
from tqdm import tqdm
import time
import requests

class Downloader:
    def __init__(self,quryString_list,id_list):
        self.quryString_list = quryString_list
        self.audio_names = id_list
        self.audios = []

    def download(self):

        self.DownloadMultiThread()


    def save(self,path):
        with tqdm(total = len(self.quryString_list),desc = "正在保存") as pbar:
            for i in range(len(self.audio_names)):
                pbar.update()
                with open(path + '/' + str(self.audio_names[i]) + '.mp3', "wb") as f:
                    f.write(self.audios[i])

    def DownloadMultiThread(self):
        with cf.ThreadPoolExecutor(max_workers=DOWNLOAD_CONFIG["THREAD_NUM"]) as executor:
            with tqdm(total=len(self.quryString_list), desc="正在下载音频") as pbar:
                for AUDIO in executor.map(DownSingleAudio, self.quryString_list):
                    pbar.update()
                    self.audios.append(AUDIO)



def DownSingleAudio(quryString):
    url = "https://fanyi.baidu.com/gettts"
    payload = ""
    response = None
    flag = False
    headers = NETWORK_CONFIG["HEADER"]
    time.sleep(DOWNLOAD_CONFIG["DOWNLOAD_DELAY"])
    for i in range(0, DOWNLOAD_CONFIG["RETRY"]):
        try:
            response = requests.get(url, headers=headers, data=payload,params= quryString)
            flag = True
            break
        except Exception as e:
            print("fail to download, it is the ", i, " attempt")
            time.sleep(DOWNLOAD_CONFIG["DOWNLOAD_DELAY"])
    if not flag:
        return None
    return response.content