from flask import Flask
from flask import request
from flask import Response
import os
import requests
 
TOKEN = os.getenv('TOKEN')
app = Flask(__name__)
url = f'https://api.telegram.org/bot{TOKEN}/sendMessage?url=https://49a1-2409-4050-e31-4464-144f-cd65-7dd-c08.in.ngrok.io'
 
languages =['cpp', 'py']
# option = 1
def compile_code(code,option):
    url = "https://api.codex.jaagrav.in"
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    payload = {
        "code": code,
        "language": languages[option]
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.json())
    output = "N/A"
    if response.json()["error"] == '':
        output = response.json()["output"]
        # print(output)
    return output


def parse_message(message):
    
    # print("message-->",message)
    if not(message.get('message') is None):
        # print("ayus")
        chat_id = message['message']['chat']['id']
        txt = message['message']['text']
        usr_name = message['message']['from']['first_name']
        # return chat_id,txt,usr_name     
    elif not(message.get('callback_query') is None):
        # print("rawa")
        chat_id = message['callback_query']['message']['chat']['id']
        # print(chat_id)
        usr_name = message['callback_query']['from']['first_name']
        # print(usr_name)
        txt = message['callback_query']['data']
        # print(txt)
    return chat_id,txt,usr_name
    # inline_msg_id = message['message']['chat']['inline_message_id']
    # print("chat_id-->", chat_id)
    # print("txt-->", txt)
 
def tel_send_message(chat_id, text):
    payload = {
                'chat_id': chat_id,
                'text': text
                }
   
    r = requests.post(url,json=payload)
    # print(r)
    return r

def tel_ask_language(chat_id):
 
    payload = {
        'chat_id': chat_id,
        'text': "What is the language of your code?",
        'reply_markup': {
            "inline_keyboard": [[
                {
                    "text": "1. C++ (cpp)",
                    "callback_data": '/1'
                },
                {
                    "text": "2. Python (py)",
                    "callback_data": '/2'
                }]
            ]
        }
    }
    r = requests.post(url, json=payload)
    return r

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        print("jnjn")
        msg = request.get_json()
        try:
            chat_id,txt,usr_name = parse_message(msg)
            option=1
            if txt == "/start":
                tel_send_message(chat_id,f"Hello!! {usr_name}.\nType /lang to select in which language you want to run code.")
            elif txt == "/lang":
                tel_ask_language(chat_id)
            elif txt[1:] >='1' and txt[1:]<='6':
                option = int(txt[1:])-1
                tel_send_message(chat_id,f"{usr_name} you chose the {languages[option]} language.\n\nPlease enter your {languages[option]} code.")
            else:
                tel_send_message(chat_id,"Please wait we are fetching results!")
                ans = compile_code(txt,option)
                tel_send_message(chat_id,ans)
        except:
            print("nada")
        return Response('ok', status=200)
    else:
        return "<h1>Welcome!</h1>"
 
if __name__ == '__main__':
   app.run(debug=True)

