#twitch parser
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import odbc
import datetime

connect=odbc.odbc('uniNotice')
db=connect.cursor()
url = 'https://www.twitch.tv/zilioner'

driver=webdriver.Chrome('chromedriver.exe') 
driver.get(url)
time.sleep(3.0)
last_chat_id=0
while(True):
    print('start')
    
    soup = BeautifulSoup(driver.page_source,'html.parser')
    chats_wrapper = soup.find('ul','chat-lines')
    chats = chats_wrapper.find_all('li')
    now_last_chat_id=int(chats[-1]['id'][5:])
    if(last_chat_id>=now_last_chat_id):
        print('no new comment')
        print(last_chat_id,now_last_chat_id)
    else:
        new_chat_num=int((now_last_chat_id-last_chat_id)/4)
        print('new comment',new_chat_num)
        print(last_chat_id,now_last_chat_id)
        if(last_chat_id==0):
            chats=chats
        else:
            chats=chats[-new_chat_num:]
        for chat in chats:
            if(chat.find('div','system-msg')):
                print(chat.find('div','system-msg').string)
            else:
                print("chat id : ",chat['id'])
                print("time : ",chat.find('span','timestamp float-left').string)
                print("badge : ",chat.find('span','badges float-left').string)
                print("from : ",chat.find('span','from').string)
                if(chat.find('span','intl-login')):
                    print("user id : ",chat.find('span','intl-login').string)
                else:
                    print("user id : user_id_none")
                message=""
                if(chat.find('span','message').string):
                    message=chat.find('span','message').string.strip()
                if(chat.find('span','balloon-wrapper')):
                    emojis=chat.find_all('span','balloon-wrapper')
                    for emoji in emojis:
                        print(emoji.find('div').string)
                        message+=emoji.find('div').string
                print("message : ",message)
            print("parse time : ",datetime.datetime.now())
            last_chat_id=int(chat['id'][5:])
            print()

    print('fin')
    time.sleep(1.0)     
    