# coding=UTF-8

import vk
from io import StringIO
import csv
import time
import re
import datetime
import pandas as pd
import random
from my_data import MyVKData_O
from post_history_fill import  post_history
from config import blackWordPart, whiteWordPart, whiteWordPart2, dopActions

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

def white_words_in_text(text, whiteWordPart):
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



def seve_data(all_post_data,all_group_data, csv_path):
    pd.set_option('display.max_columns', 16)
    df1 = pd.DataFrame(all_post_data)
    df2 = pd.DataFrame(all_group_data)
    df = pd.merge(df1, df2, on='group_ids')
    df = df.drop_duplicates(subset='post', keep='first')
    print(df)
    #df = df.sort_values(by='4', ascending=True)
    file_name = csv_path
    df.to_csv(file_name, sep=';', encoding='utf-8', index=False, header=True)

def app_dikt_data(data, all_data):
    data_keys = data.keys()
    for key in data_keys:
        try:
            if isinstance(all_data[key], list):
                all_data[key].extend(data[key])
            else: all_data[key] = [all_data[key], data[key]]
        except Exception as e:
            print(Exception)
            all_data = data
            return all_data
    return all_data

def app_groupp_data(group_ids,all_group_data):
    fields = ['city', 'country', 'description', 'main_section', 'members_count', 'verified']
    group_data = vkapi.groups.getById(group_ids=group_ids,fields = fields,v=v)
    # print(group_data)
    for i in range(len(group_data)):
        app_group_data = {}
        app_group_data['group_ids'] = [int(group_data[i]['id'])]
        name = str(text_clear(group_data[i]['name']))
        if name != '':
            app_group_data['name'] = [name]
        else: app_group_data['name'] = ['None']
        city = group_data[i].get('city', None)
        if city != None:
            app_group_data['city'] = [str(group_data[i]['city']['title'])]
            app_group_data['city_id'] = [str(group_data[i]['city']['id'])]
        else: app_group_data['city'] = app_group_data['city_id'] = ['None']

        country = group_data[i].get('country', None)
        if country != None:
            app_group_data['country'] = [str(group_data[i]['country']['title'])]
            app_group_data['country_id'] = [str(group_data[i]['country']['id'])]
        else:
            app_group_data['country'] = app_group_data['country_id'] = ['None']
        description = str(text_clear(group_data[i].get('description', 'None')))
        if description != '':
            app_group_data['description'] = [str(description)]
        else: app_group_data['description'] = ['None']
        app_group_data['main_section'] = [str(group_data[i].get('main_section', 'None'))]
        app_group_data['members_count'] = [str(group_data[i].get('members_count', 'None'))]
        app_group_data['verified'] = [str(group_data[i].get('verified', 'None'))]
        if all_group_data == {} or app_group_data['group_ids'][0] not in all_group_data['group_ids']:
            all_group_data = app_dikt_data(app_group_data, all_group_data)
    return all_group_data

def len_histori(all_post_data):
    histori = vkapi.messages.getHistory(count = count, peer_id = peer_id, v=v)['items']
    for i in range(len(histori)):
        try:
            group_id = histori[i]['attachments'][0]['wall']['from_id']
            post_id = histori[i]['attachments'][0]['wall']['id']
        except IndexError:
            continue
        post = 'wall' + str(group_id) + '_' + str(post_id)
        if post in all_post_data['post']:
            i1 = all_post_data['post'].index(post)
            all_post_data['approved'][i1] = int(histori[i]['important'])

    return all_post_data


def opel_fill(csv_path,pd):
    try:
        pd = pd.read_csv(csv_path, sep=';', encoding='utf-8')
        all_group_data = pd[['city','city_id','country','country_id','description','group_ids','main_section','members_count','name','verified']].to_dict('list')
        all_post_data = pd[['comments','date','group_ids','likes','post','text','approved','views']].to_dict('list')
    except Exception as e:
        print(Exception)
        all_post_data ={}
        all_group_data = {}
    return (all_post_data, all_group_data)

csv_path = 'Посты.csv'

v = 5.92
session = vk.AuthSession(app_id=MyVKData_O.MY_PRIL_ID, user_login=MyVKData_O.LOGIN,
                         user_password=MyVKData_O.GET_PASSWORD, scope='wall, fields, messages, groups')
vkapi = vk.API(session)
api = vk.API(session, v=v)
count = 200

zapros = 'бесплатно'

all_post_data= opel_fill(csv_path,pd)[0]
all_group_data= opel_fill(csv_path,pd)[1]
chat_id = 5
peer_id = 2000000000 + chat_id

if all_post_data != {}:
    all_post_data = len_histori(all_post_data)

stop = False
while stop == False:
    end_time = datetime.datetime.now()
    end_time = int(time.mktime(end_time.timetuple())) - 60*60
    newsfeed = vkapi.newsfeed.search(q='приз',end_time = end_time, count=count, filters='post ', v=v)
    newsfeed = newsfeed['items']
    message_ids = []
    # Поднять история постов
    for i in range(len(newsfeed)):
        post_data = {}
        group_id = str(newsfeed[i]['from_id'])

        if str(group_id)[0] != '-':
            continue

        post_id = newsfeed[i]['id']
        post = 'wall' + str(group_id) + '_' + str(post_id)
        if post not in post_history:
            #print('https://vk.com/id' + str(group_id) + '?w=wall' + str(group_id) + '_' + str(post_id))
            append_in_histori(post)
            text = text_clear(newsfeed[i]['text'])

            if white_words_in_text(text, whiteWordPart) and white_words_in_text(text, whiteWordPart2):
                if black_words_in_text(text):
                    continue
                if dopActions_in_text(text):
                    continue

                # В этои месте подписаться и лайк репостить
                # try:
                    # time.sleep(1 / 3)
                    # vkapi.groups.join(group_id=str(group_id)[1:], v=v)
                # except IOError as e:
                #     print(e)
                # vkapi.likes.add(type = 'post',owner_id = group_id,item_id = post_id, v=v)
                # vkapi.wall.repost(object=post, v=v)
                time.sleep(1/3)
                random_id = random.randint(0, 999999)
                message_ids.append(vkapi.messages.send(peer_id=peer_id, chat_id=chat_id, random_id=random_id, attachment=post, v=v))
                # Собираем данные
                post_data['post'] = [post]
                post_data['text'] = [text]
                post_data['date'] = [newsfeed[i]['date']]
                post_data['comments'] = [str(newsfeed[i]['comments']['count'])]
                post_data['likes'] = [str(newsfeed[i]['likes']['count'])]
                post_data['group_ids'] = [int((group_id)[1:])]
                post_data['views'] = [int(newsfeed[i]['views']['count'])]
                post_data['approved'] = ['1']
                # print(post_data['post'][0])
                # print(all_post_data['post'])
                if all_post_data == {} or post not in all_post_data['post']:
                    all_post_data = app_dikt_data(post_data, all_post_data)
                # print(all_post_data)
    try:
        vkapi.messages.markAsImportant(message_ids = message_ids,important = 1, v=v)
    except Exception as e:
        print(Exception)
    if all_post_data != {}:
        all_group_data = app_groupp_data(all_post_data['group_ids'], all_group_data)
        seve_data(all_post_data,all_group_data, csv_path)
    print('Цикл')
    time.sleep(60*20)