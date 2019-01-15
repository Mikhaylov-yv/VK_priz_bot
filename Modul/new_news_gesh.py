import vk
import vk_api
import requests
from my_data import MyVKData
import websocket
import random
import json
import time

chat_id = 1
peer_id = 2000000000  + chat_id
v=5.92
session = vk.AuthSession(app_id=MyVKData.MY_PRIL_ID, user_login=MyVKData.LOGIN, user_password=MyVKData.GET_PASSWORD, scope='messages')
vkapi = vk.API(session)
api = vk.API(session, v=v)

# Список интересов
def get_rules_list():
    rules = get_my_rules()
    if rules:
        return "\n".join([str(rule['value']) for rule in rules])

# Очистить список интересов
def clear_rules_list():
    rules = get_my_rules()
    if rules:
        for rule in rules:
            del_my_rules(rule['tag'])
        return "Successful"

def get_streaming_server_key(token):
    request_url = "https://api.vk.com/method/streaming.getServerUrl?access_token={}&v=5.64".format(token)
    r = requests.get(request_url)
    data = r.json()
    return {"server":data["response"]["endpoint"],"key":data["response"]["key"]}

def listen_stream():
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://{}/stream?key={} ".format(stream["server"], stream["key"]),
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()

def on_message(ws, message):
    print(">>>> receive message:", message)
    message = eval(message)
    if message["event"]['event_type'] == 'post':
        post = 'wall' + str(message["event"]['author']['id']) + '_' + str(message["event"]['event_id']['post_id'])
        random_id = random.randint(0, 9999)
        vkapi.messages.send(peer_id=peer_id, random_id=random_id, attachment=post, v=v)
        time.sleep(1/3)

def on_error(ws, error):
    print(">>>> error thead:",error)

def on_close(ws):
    print(">>>> close thead")

def on_open(ws):
    print(">>>> open thead")


def set_my_rules(value):
    rule_params = {"rule":{"value":value,"tag":'tag_'+str(random.randint(11111, 99999))}}
    headers = {'content-type': 'application/json'}
    r = requests.post("https://{}/rules?key={}".format(stream["server"], stream["key"]), data=json.dumps(rule_params), headers=headers)
    data = r.json()

    return data['code'] == 200

def get_my_rules():
    r = requests.get("https://{}/rules?key={}".format(stream["server"], stream["key"]))
    data = r.json()
    if data['code'] != 200:
        return False

    return data['rules']

def del_my_rules(tag):
    headers = {'content-type': 'application/json'}
    rule_params = {"tag":tag}
    r = requests.delete("https://{}/rules?key={}".format(stream["server"], stream["key"]), data=json.dumps(rule_params), headers=headers)
    data = r.json()

    return data['code'] == 200

stream = get_streaming_server_key(MyVKData.TOKEN)
clear_rules_list()
set_my_rules("розыгрыш")
print(get_rules_list())
listen_stream()


