import csv
import pandas as pd
from os.path import join
from datetime import datetime

from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)


DATABASE_DIR = 'database'

USERID_DATABASE_PATH = join(DATABASE_DIR,'database_users.csv')
USER_ANSWERS_DIR = join(DATABASE_DIR,'user_answers')
INITIAL_QUESTION_DIR = join(DATABASE_DIR,'database_initial_questions.csv')

#def generate_next_question(user_id):

#def generate_quick_reply(user_id, question, answers_list):


def save_init_reply(line_bot_api, user_id, msg):
    init_qa = pd.read_csv(INITIAL_QUESTION_DIR)
    user_an = pd.read_csv(join(USER_ANSWERS_DIR,f'{user_id}_answers.csv'))
    num_user_answers = len(user_an)
    
    answer = msg
    question = init_qa.iloc[num_user_answers][0]
    
    write_userid_answers_csv(user_id, question, answer)
    
    if num_user_answers+1 < len(init_qa):
        run_initial_questions(line_bot_api, user_id)

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
    
    line_bot_api.push_message(
                user_id, 
                TextSendMessage(text=question))
    
    
    '''
    massage = ''
    for i in range(num_questions):
        if entry_id == i:
            question, answers = init_qa.iloc[i].values
            answers = answers.replace(' ', '')
            print(question)
            
            if answers == 'None':
                line_bot_api.push_message(
                    user_id, 
                    TextSendMessage(text=question))
            else:
                # quick_reply
            
            return
         '''   
    '''
    for i in range(len(init_qa)):
        question, answers = init_qa.iloc[i].values
        answers = answers.replace(' ', '')
        
        print(question)
        if answers != 'None':
            answers_list = answers.split('/')
            print(answers_list)
            
        line_bot_api.push_message(
            user_id, 
            TextSendMessage(text=question))
'''
    


def save_userid_to_csv(user_id):
    # save userID
    
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