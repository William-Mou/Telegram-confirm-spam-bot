import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
import os
import time
import json
telBot = telepot.Bot(os.environ.get('SLACK_BOT_TOKEN'))

# chat_id:[add_member]
enter_queue = {}
last_time = 0

def print_msg(msg):
    print(json.dumps(msg, indent=10))

def enter_push(chat_id, user_id):
    global last_time
    last_time = time.time()
    if chat_id in enter_queue:
        enter_queue[chat_id].append(user_id)
    else:
        enter_queue[chat_id] = [user_id]
    
def sendWarningMsg():
    print(enter_queue)
    for chat in enter_queue:
        if len(enter_queue[chat]) != 0:
            telBot.sendMessage(chat,"@admin Here is a unconfirmed list! \n" + str(['@'+str(i) for i in enter_queue[chat]]))

def on_chat(msg):
    print_msg(msg)
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    content_type, chat_type, chat_id = map(str,telepot.glance(msg))
    print(content_type, chat_type, chat_id )
    if "new_chat_participant" in msg:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
                   [InlineKeyboardButton(text='Press me', callback_data=str(chat_id))],
               ])
        telBot.sendMessage(chat_id, 'Hello~your welcome SITCON!\nPlease press the button let us know you are not spam~', reply_markup=keyboard)
        enter_push(str(chat_id), str(msg["from"]["id"]))
    if msg['text'] == '/skip':
        global enter_queue
        enter_queue = {}
def on_callback_query(msg):
    query_id, from_id, query_data = map(str,telepot.glance(msg, flavor='callback_query'))
    print('Callback Query:', query_id, from_id, query_data)

    telBot.answerCallbackQuery(query_id, text='Got it')
    print(enter_queue[query_data],from_id)
    enter_queue[query_data].remove(from_id)

MessageLoop(telBot, {
    'chat': on_chat,
    'callback_query': on_callback_query,
}).run_as_thread()

while(True):
    time.sleep(1)
    #print(time.time() - last_time)
    #print((time.time() - last_time)%6)
    if time.time() - last_time >= 15 and time.time() - last_time <= 30:
        sendWarningMsg()
    if time.time() - last_time >= 15 and (int(time.time()) - int(last_time))%3600 == 0:
        sendWarningMsg()
