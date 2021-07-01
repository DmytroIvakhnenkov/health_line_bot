import os
import sys
import time
import csv
from datetime import datetime
from threading import Thread


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

#
# BODY
#

app = Flask(__name__)
line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

#line_bot_api.push_message('<to>', TextSendMessage(text='Hello World!'))


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
    print(event.source.user_id)
    message = event.message.text
    
    print(event)
    user = line_bot_api.get_profile(event.source.user_id)
    
    if message == 'start':
        print(message)
        # save userID
        user_id = event.source.user_id
        now = datetime.now()
        current_time = now.strftime("%d/%m/%Y %H:%M:%S")
        print(user_id + "\n\n\n")
        
        # open the file in the write mode
        f = open('reply_message/database_users.csv', 'a', newline="")

        # create the csv writer
        writer = csv.writer(f)
        # write a row to the csv file
        writer.writerow([user_id])
    
        # close the file
        f.close()
            
def generate_next_question(user_id):
    

            
class PushMesseging(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.start()
    
    def run(self):
        
    """
        while True:
            time.sleep(7)
            
            user_ids = []
            
            with open('reply_message/database_users.csv', 'r') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=',')
                for row in spamreader:
                    user_ids += [row[0]]
        
            if user_ids != []:
                print(user_ids)
                for user_id in user_ids:
                    line_bot_api.push_message(
                        user_id,
                        TextMessage(text='ur mom gay'))
            else:
                print('No user ids')
            """

if __name__ == "__main__":
    
    PushMesseging()
    
    app.run(host='0.0.0.0', port=5000, debug=True)

    