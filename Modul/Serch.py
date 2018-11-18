import vk_api
from reg_data import MyVKData
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
        groups = []


        #for word in whiteWordPart:
            #time.sleep(1 / 3)
        finded_groups = pool.method('groups.search', {
            #'q': word
            'q':'лайк'
        })
        a = finded_groups.result['items']
        for group in finded_groups.result['items']:
            group_id = group['id']
            group_name = group['name']
            groups.append([group_id, group_name])





    print(groups)


if __name__ == '__main__':
    main()
