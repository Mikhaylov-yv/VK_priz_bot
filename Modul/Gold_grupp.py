import vk
from my_data import MyVKData

chat_id = 79
peer_id = 2000000000  + chat_id
v=5.92
session = vk.AuthSession(app_id=MyVKData.MY_PRIL_ID, user_login=MyVKData.LOGIN, user_password=MyVKData.GET_PASSWORD, scope='messages')
vkapi = vk.API(session)
api = vk.API(session, v=v)

vkapi.groups.search(q = '',type='group, page', v=v)