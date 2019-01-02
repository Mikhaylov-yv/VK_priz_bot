import vk_api
from my_data import MyVKData
from config import whiteWordPart
import time
def main():
    vk_session = vk_api.VkApi(MyVKData.LOGIN, MyVKData.GET_PASSWORD)
    try:
        vk_session.auth()
        print('Ok')
    except vk_api.AuthError as errror_msg:
        print(errror_msg)
        return


    with vk_api.VkRequestsPool(vk_session) as pool:
        posts = []


        #for word in whiteWordPart:
            #time.sleep(1 / 3)
        finded_groups = pool.method('groups.search', {
            #'q': word
            'q':'лайк'
        })

        for post in newsfeed.items:
            id_posts = post['id_posts']
            group_id = post['group_id']
            mass = {}
            mass['id_posts'] = id_posts
            mass['group_id'] = group_id
            posts.append(mass)


for post in posts:
    vkapi.wall.repost(post['id_posts'])


    print(groups)


if __name__ == '__main__':
    main()
