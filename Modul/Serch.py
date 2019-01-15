# coding=UTF-8

import vk
from io import StringIO
import csv
import time
import re
import datetime
from my_data import MyVKData_O
from post_history_fill import  post_history
from config import blackWordPart, whiteWordPart, dopActions

def text_clear(text):
    reg = re.compile('[^а-яА-я ]')
    text = reg.sub(' ', str(text))
    text = re.sub(" +", " ", text)
    text = text.lower()
    return text

def data_rekonf(date_int):
    date = datetime.datetime.fromtimestamp(date_int)
    date_str = date.strftime('%d-%m-%Y %H:%M:%S')
    return date_str

def black_words_in_text(text):
    for word in blackWordPart:
        if word in text:
            return True
    return False

def white_words_in_text(text):
    for word in whiteWordPart:
        if word in text:
            return True
    return False

def dopActions_in_text(text):
    for word in dopActions:
        if word in text:
            return True
    return False

def append_in_histori(post):
    post_history.append(post)
    file = open('post_history_fill.py', 'w')
    file.write('post_history = ' + str(post_history))
    file.close()



v = 5.92
session = vk.AuthSession(app_id=MyVKData_O.MY_PRIL_ID, user_login=MyVKData_O.LOGIN,
                         user_password=MyVKData_O.GET_PASSWORD, scope='wall, fields, messages, groups')
vkapi = vk.API(session)
api = vk.API(session, v=v)
count = 25

zapros = 'конкурс репост подарки'

stop = False
while stop == False:
    newsfeed = vkapi.newsfeed.search(q='приз', count=count, filters='post ', v=v)
    newsfeed = newsfeed['items']
    # Поднять история постов
    for i in range(len(newsfeed)):
        group_id = newsfeed[i]['from_id']

        if str(group_id)[0] != '-':
            continue

        post_id = newsfeed[i]['id']
        post = 'wall' + str(group_id) + '_' + str(post_id)
        if post not in post_history:
            print('https://vk.com/id' + str(group_id) + '?w=wall' + str(group_id) + '_' + str(post_id))
            append_in_histori(post)
            text = text_clear(newsfeed[i]['text'])

            if white_words_in_text(text):
                if black_words_in_text(text):
                    continue
                if dopActions_in_text(text):
                    continue
                try:
                    time.sleep(1 / 3)
                    vkapi.groups.join(group_id=str(group_id)[1:], v=v)
                except IOError as e:
                    print(e)
                vkapi.likes.add(type = 'post',owner_id = group_id,item_id = post_id, v=v)
                vkapi.wall.repost(object=post, v=v)
                time.sleep(1/3)
                vkapi.messages.send(user_id='255960', attachment=post, v=5.0)
                # В этои месте подписаться и репостить

    time.sleep(60*60)