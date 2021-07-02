import csv
import pandas as pd
import numpy as np
from os.path import join
from datetime import datetime
from threading import Timer

from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, QuickReplyButton, MessageAction, QuickReply
)
#============================================================
# Hyperparameters
DATABASE_DIR = 'database'

USERID_DATABASE_PATH = join(DATABASE_DIR,'database_users.csv')
USER_ANSWERS_DIR = join(DATABASE_DIR,'user_answers')

ALL_QUESTIONS = 'database_QA.csv'
INITIAL_QUESTION_DIR = join(DATABASE_DIR,'database_initial_questions.csv')
ALL_QUESTION_DIR = join(DATABASE_DIR, ALL_QUESTIONS)
#============================================================

#def generate_next_question(user_id):

def init_repeated_message(func, args):
    _, _,time_sec = args
    srqta_timer = Timer(
        time_sec,
        func,
        args)
    srqta_timer.start()


def send_random_question(line_bot_api, user_id, time_sec):
    print(f'\t send_random_question to {user_id}')
    init_qa = pd.read_csv(ALL_QUESTION_DIR)
    #users = pd.read_csv(USERID_DATABASE_PATH)
    
    idx = np.random.randint(len(init_qa))
    #print(init_qa.iloc[idx].values)
    
    question, answers = init_qa.iloc[idx].values[:2]
    
    #for user_id in users:
        # put question to user database
    write_userid_answers_csv(
        user_id, 
        question, answer='')

    msg = generate_quick_reply(question, answers)
    #print(msg)
    line_bot_api.push_message(
        user_id, 
        msg)
        
    #print(user_id, question, answers)

    #init_repeated_message(time_sec, line_bot_api, send_random_question_to_all)


def save_init_reply(line_bot_api, user_id, msg):
    global APP_MODE
    init_qa = pd.read_csv(INITIAL_QUESTION_DIR)
    user_an = pd.read_csv(join(USER_ANSWERS_DIR,f'{user_id}_answers.csv'))
    num_user_answers = len(user_an)
    
    answer = msg
    question = init_qa.iloc[num_user_answers][0]
    
    write_userid_answers_csv(user_id, question, answer)
    
    if num_user_answers+1 < len(init_qa):
        print('Initial questions...')
        run_initial_questions(line_bot_api, user_id)
        return
    else:
        print('\t Initial questions finish.')
        return 'default'


def run_initial_questions(line_bot_api, user_id):
    # read init questions
    init_qa = pd.read_csv(INITIAL_QUESTION_DIR)
    num_questions = len(init_qa)
    
    try:
        user_an = pd.read_csv(join(USER_ANSWERS_DIR,f'{user_id}_answers.csv'))
        num_user_answers = len(user_an)
    except:
        user_an = None
        num_user_answers = 0
    
    print(num_questions, num_user_answers)
    
    if num_user_answers == 0:
        # greetings & first question
        greeting_msg = 'Hi user! Please answer next questions.'
            
        line_bot_api.push_message(
                    user_id, 
                    TextSendMessage(text=greeting_msg))
    
    question, answers = init_qa.iloc[num_user_answers].values

    if("None" in answers):
            line_bot_api.push_message(
                user_id, 
                TextSendMessage(text=question))        
    else:  
        line_bot_api.push_message(
                    user_id, 
                    generate_quick_reply(question, answers))
        
  
def save_userid_to_csv(user_id):
    # save userID
    # TODO: must be no duplicates for ids in database_users
    now = datetime.now()
    current_time = now.strftime("%d/%m/%Y %H:%M:%S")
    #print(user_id + "\n\n\n")
    
    # open the file in the write mode
    f = open(USERID_DATABASE_PATH, 'w', newline="")

    # create the csv writer
    writer = csv.writer(f)
    # write a row to the csv file
    writer.writerow([user_id])
    # close the file
    f.close()
    
    
def create_userid_answers_csv(user_id):
    # create unique user database
    filename = join(USER_ANSWERS_DIR, f'{user_id}_answers.csv')
    print(filename)
    f = open(filename, 'w+', newline="")
    writer = csv.writer(f)
    writer.writerow(['questions', 'answers'])
    f.close()
    
    
def write_userid_answers_csv(user_id, question, answer):
    filename = join(USER_ANSWERS_DIR, f'{user_id}_answers.csv')
    
    f = open(filename, 'a', newline="")
    writer = csv.writer(f)
    writer.writerow([question, answer])
    f.close()
    
    
def generate_quick_reply(question, answers):

    # getting the answers to the question
    answers = answers.split(" / ")

    # generating buttons
    my_items = []
    for i, answer in enumerate(answers):
        my_items.append(QuickReplyButton(action=MessageAction(label=answer[:20], text=answer)))

    text_message = TextSendMessage(text=question,
                                   quick_reply=QuickReply(items=my_items))
    
    return text_message
    
    
def generate_new_user(user_id):
    save_userid_to_csv(user_id)
    create_userid_answers_csv(user_id)