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


time.sleep(2)
#WEATHER
url = 'https://tenki.jp/forecast/3/23/4820/20203/' 
r = requests.get(url)
bsObj = BeautifulSoup(r.content,"html.parser")
today = bsObj.find(class_="today-weather")
weather = today.p.string
temp = today.div.find(class_="date-value-wrap")
temp=temp.find_all("dd")
temp_max = temp[0].span.string
today_weather="今日の天気は{}で_ス".format(weather)
today_temp="最高気温は{}どで".format(temp_max)

#降水確率(4つとも0%なら0、0以外の時間帯があるならそれを読み上げる)
rain = bsObj.find(class_="rain-probability")
today_rain=[]
for j in rain:
    if not '\n'in j:
        today_rain.append(str(j))
train=[]
for jj in today_rain:
    a=re.findall(r'\d+',jj)
    if len(a)!=0:
        train.append(int(a[0]))
    else:
        train.append(0)
train.pop(0)
today_time={0:"0時から6時、",1:"６時から12時、",2:"12時から18時、",3:"18時から24時、"}
time_W="降水確率は、"
flag=0
for i in range(len(train)):
    aa="{}:{}".format(i,train[i])
    print(aa)
    if train[i]!=0:
        time_W+=today_time[i]
        time_W+=str(train[i])+"%、"
        flag+=1
if flag == 0:
    time_W+="終日0%でス"



#DATE
now = datetime.datetime.now()
week={0:"月曜日",1:"火曜日",2:"水曜日",3:"木曜日",4:"金曜日",5:"土曜日",6:"日曜日"}
date=str(now.month)+"月"+str(now.day)+"日"+str(week[now.weekday()])


#####################################################################################
# カレンダーAPIで操作できる範囲を設定（今回は読み書き）
SCOPES = ['https://www.googleapis.com/auth/calendar']

# Google にcalendarへのアクセストークンを要求してcredsに格納します。
creds = None

# 有効なトークンをすでに持っているかチェック（２回目以降の実行時に認証を省略するため） 
if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)

# 期限切れのトークンを持っているかチェック（認証を省略するため）
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    # アクセストークンを要求
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # アクセストークン保存（２回目以降の実行時に認証を省略するため） 
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)
###### 予定を読み込む ######
service = build('calendar', 'v3', credentials=creds)
# 現在時刻を取得
now1 = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
# カレンダーから予定を取得 
events_result = service.events().list(calendarId='primary', timeMin=now1,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
events = events_result.get('items', [])

# 予定がない場合には、Not found
if not events:
    #memo
    yotei="今日の予定は特にありません"
# 予定があった場合には、出力
today_yotei=""
for event in events:
    start = event['start'].get('dateTime', event['start'].get('date'))
    print("--a--")
    print(start, event['summary'])
    #日付
    c_date=""
    c_date+=start[8]
    c_date+=start[9]

    if(c_date[0]=='0'):
        c_date=start[9]
    
    if c_date ==str(now.day):
        #時間を取得
        c_time=""
        if start[11]=="0":
            c_time=c_time+start[12]+"時"
            if start[14]!="0":
                c_time=c_time+start[14]+"分"
        else:
            c_time=c_time+start[11]+start[12]+"時"
            if start[14]!="0":
                c_time=c_time+start[14]+"分"

        today_yotei=today_yotei+c_time+"から"
        today_yotei+=event['summary']
        print(today_yotei)

if len(today_yotei)!=0:
    yotei="今日の予定は"+today_yotei+"となっていま_ス"
else:
    yotei="今日の予定は特にありません"


#####################################################################################


gr=["おはようございま_ス",date,today_weather,time_W,today_temp,yotei]
_start = f"start {BASE_DIR}\\softalk\\SofTalk.exe /X:1"
_speed = "/S:80"
_word = "/W:"

filename = 'Rewrite.mp3' #再生したいmp3ファイル
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

