import csv
from datetime import datetime

USERID_DATABASE_PATH = 'database/database_users.csv'


#def generate_next_question(user_id):

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