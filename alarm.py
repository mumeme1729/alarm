import os
from pathlib import Path
import subprocess
import datetime
import requests
from bs4 import BeautifulSoup
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request 
from mutagen.mp3 import MP3 as mp3
import pygame
import time
import re


BASE_DIR = Path(__file__).resolve().parent

class Alarm:
    def __init__(self):
        self.BASE_DIR = Path(__file__).resolve().parent
        self.now = datetime.datetime.now()
        self.date=""
        self.today_weather=""
        self.time_W=""
        self.today_temp=""
        self.plans=""

        time.sleep(2)
        self.set_weather()
        self.set_google_calendar_schedule()


    def set_weather(self):
        #　tenki.jpさんのURL 以下長野県上田市のURL
        url = 'https://tenki.jp/forecast/3/23/4820/20203/' 
        r = requests.get(url)
        bsObj = BeautifulSoup(r.content,"html.parser")
        today = bsObj.find(class_="today-weather")
        weather = today.p.string
        temp = today.div.find(class_="date-value-wrap")
        temp=temp.find_all("dd")
        temp_max = temp[0].span.string #最高気温

        #降水確率(4つとも0%なら0、0以外の時間帯があるならそれを読み上げる)
        rain_probability = bsObj.find(class_="rain-probability")
        today_rain=[]
        for rain in rain_probability:
            if not '\n'in rain:
                today_rain.append(str(rain))
        check_rain=[]
        for rain in today_rain:
            a=re.findall(r'\d+',rain)
            if len(a)!=0:
                check_rain.append(int(a[0]))
            else:
                check_rain.append(0)
        check_rain.pop(0)
        today_time={0:"0時から6時、",1:"６時から12時、",2:"12時から18時、",3:"18時から24時、"}
        self.time_W="降水確率は、"
        flag=0
        for i in range(len(check_rain)):
            rain_time="{}:{}".format(i,check_rain[i])
            print(rain_time)
            if check_rain[i]!=0:
                self.time_W+=today_time[i]
                self.time_W+=str(check_rain[i])+"%、"
                flag+=1
        if flag == 0:
            self.time_W+="終日0%でス"

        
        week={0:"月曜日",1:"火曜日",2:"水曜日",3:"木曜日",4:"金曜日",5:"土曜日",6:"日曜日"}

        self.date=str(self.now.month)+"月"+str(self.now.day)+"日"+str(week[self.now.weekday()])
        self.today_weather="今日の天気は{}で_ス".format(weather)
        self.today_temp="最高気温は{}どで".format(temp_max)


    def set_google_calendar_schedule(self):
        SCOPES = ['https://www.googleapis.com/auth/calendar']
        #calendarへのアクセストークンを要求し、credsに格納
        creds = None
        # 有効なトークンをすでに持っているかチェック（２回目以降の実行時に認証を省略するため） 
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)

        # 期限切れのトークンを持っているかチェック
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            # アクセストークンを要求
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # アクセストークン保存 
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        # 予定を読み込む 
        service = build('calendar', 'v3', credentials=creds)
        # 現在時刻を取得
        utc_time = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        # カレンダーから予定を取得 
        events_result = service.events().list(calendarId='primary', timeMin=utc_time,
                                                maxResults=10, singleEvents=True,
                                                orderBy='startTime').execute()
        events = events_result.get('items', [])

        # 予定がない場合には、Not found
        if not events:
            #memo
            self.plans="今日の予定は特にありません"
        # 予定があった場合には、出力
        todays_plan=""
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            #予定の開始時刻を取得
            calendar_date=""
            calendar_date+=start[8]
            calendar_date+=start[9]

            if(calendar_date[0]=='0'):
                calendar_date=start[9]
            
            if calendar_date ==str(self.now.day):
                #時間を取得
                calendar_time=""
                if start[11]=="0":
                    calendar_time=calendar_time+start[12]+"時"
                    if start[14]!="0":
                        calendar_time=calendar_time+start[14]+"分"
                else:
                    calendar_time=calendar_time+start[11]+start[12]+"時"
                    if start[14]!="0":
                        calendar_time=calendar_time+start[14]+"分"

                todays_plan=todays_plan+calendar_time+"から"
                todays_plan+=event['summary']
                

        if len(todays_plan)!=0:
            self.plans="今日の予定は"+todays_plan+"となっていま_ス"
        else:
            self.plans="今日の予定は特にありません"  

    def start_softolk(self):
        gr=["おはようございま_ス",self.date,self.today_weather,self.time_W,self.today_temp,self.plans]
        _start = f"start {BASE_DIR}\\softalk\\SofTalk.exe /X:1"
        _speed = "/S:80"
        _word = "/W:"

        filename = 'Rewrite.mp3' #BGMとして再生したいmp3ファイル
        if filename!='':
            pygame.mixer.init()
            pygame.mixer.music.load(filename) #音源を読み込み
            mp3_length = mp3(filename).info.length #音源の長さ取得
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play(1)   
            pygame.mixer.music.fadeout(80000)
            time.sleep(1)
            for i in gr:
                _command = [_start, _speed, _word+i,]
                print(_command)
                subprocess.run(' '.join(_command), shell=True)
                time.sleep(3.0)

            time.sleep(80 -0.25) #再生開始後、音源の長さだけ待つ(0.25待つのは誤差解消)
            pygame.mixer.music.stop()
        else:
            time.sleep(1)
            for i in gr:
                _command = [_start, _speed, _word+i,]
                print(_command)
                subprocess.run(' '.join(_command), shell=True)
                time.sleep(3.0)

    


alarm=Alarm()
alarm.start_softolk()