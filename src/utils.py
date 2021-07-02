import csv
import pandas as pd
from os.path import join
from datetime import datetime

DATABASE_DIR = 'database'

USERID_DATABASE_PATH = join(DATABASE_DIR,'database_users.csv')
USER_ANSWERS_DIR = join(DATABASE_DIR,'user_answers')
INITIAL_QUESTION_DIR = join(DATABASE_DIR,'database_initial_questions.csv')

#def generate_next_question(user_id):

def run_initial_questions(user_id):
    # read init questions
    init_qa = pd.read_csv(INITIAL_QUESTION_DIR)
    
    for i in range(len(init_qa)):
        question, answers = init_qa.iloc[i].values
        answers = answers.replace(' ', '')
        
        print(question)
        if answers != 'None':
            answers_list = answers.split('/')
            print(answers_list)


def save_userid_to_csv(user_id):
    # save userID
    
    now = datetime.now()
    current_time = now.strftime("%d/%m/%Y %H:%M:%S")
    #print(user_id + "\n\n\n")
    
    # open the file in the write mode
    f = open(USERID_DATABASE_PATH, 'a', newline="")

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
    f.close()