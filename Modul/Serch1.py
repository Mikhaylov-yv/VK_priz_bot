import vk
from my_data import MyVKData
from config import whiteWordPart
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
        for whiteWord in whiteWordPart:
            if whiteWord  in post['text']:
                id_posts = post['from_id']
                group_id = post['id']
                text = post['text']
                mass = {}
                mass['id_posts'] = id_posts
                mass['group_id'] = group_id
                mass['text'] = text
                posts.append(mass)
    print(posts)
    # for post in posts:
    #     vkapi.wall.repost(post['id_posts'])

    time.sleep(60)

