import vk
from my_data import MyVKData
from config import whiteWordPart
from config import blackWordPart
import time

v=5.92
session = vk.AuthSession(app_id=MyVKData.MY_PRIL_ID, user_login=MyVKData.LOGIN, user_password=MyVKData.GET_PASSWORD, scope='wall, fields, messages')
vkapi = vk.API(session)
api = vk.API(session, v=v)
count = 200
posts = []
stop = False


while stop == False:
    newsfeed = vkapi.newsfeed.search(q='конкурс репост подарки санкт-петербург', count=count, filters='post ', v=v)

    for post in newsfeed['items']:
            id_posts = post['from_id']
            group_id = post['id']
            text = post['text']
            mass = {}
            mass['id_posts'] = id_posts
            mass['group_id'] = group_id
            mass['text'] = text
            i = 0
            i_max=len(whiteWordPart)
            while i < i_max and  whiteWordPart[i] in text:
                i1=0
                i1_max = len(blackWordPart)
                while i1 < i1_max  and blackWordPart[i1] not in text:
                    if id_posts not in posts:
                        posts.append(mass)
                    i1=i1+1
                i=i+1

    print(posts)

    # for post in posts:
    #     vkapi.wall.repost(post['id_posts'])

    time.sleep(60)

