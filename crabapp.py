import os
import sys
import time
import csv
from datetime import datetime
from threading import Thread, Timer


from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

# custum srcs
from src.vars import *
from src.utils import *


#============================================================
# Hyperparameters
app = Flask(__name__)
line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)
# This will help to distinguish between init/default use 
#APP_MODE = 'init' # 'init', 'default', 'waiting'

USERS_MODES = {}
#============================================================

#
# BODY
#

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def message_text(event):
    global APP_MODE
    
    user_id = event.source.user_id
    message = event.message.text
    
    if user_id not in USERS_MODES.keys():
        if message == 'start':
            generate_new_user(user_id)
            run_initial_questions(line_bot_api, user_id)
            USERS_MODES[user_id] = 'init'
            
    elif USERS_MODES[user_id] == 'init':
        new_mode = save_init_reply(
            line_bot_api, 
            user_id, 
            message)
        if new_mode:
            USERS_MODES[user_id] = new_mode
    
    elif USERS_MODES[user_id] == 'waiting':
        print(message)
        
    else:
        print('ERROR!!!!')


class PushMesseging(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.start()
    
    def run(self):
        global USERS_MODES
        # TODO:
        # here we must specify conditions for further questions or notifications.
        print('PushMesseging running...')
        
        # ask random question every 30 sec, but only if previus answered
        #init_repeated_message()
        
        time_sec = 10
        
        while True:
            for user_id, mode in USERS_MODES.items():
                if mode == 'default':
                    args = [line_bot_api, user_id, time_sec]
                    init_repeated_message(
                        send_random_question, args
                    )
                    USERS_MODES[user_id] = 'waiting'
            else:
                pass
            time.sleep(1)


if __name__ == "__main__":
    PushMesseging()
    
    app.run(host='0.0.0.0', port=5000, debug=True)

    