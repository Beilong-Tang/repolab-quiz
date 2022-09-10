# This file is a setting file
import os

# quiz week folder
quiz_dir='/mnt/c/Users/Beilong Tang/Desktop/Main/CODE/DJANGO_new/repolab-quiz/bank/week'

ldir = os.path.dirname(os.path.abspath(__file__))
quiz_dir='%s/../../../repolab-quiz/bank/week'% ldir

# question_due_dict
question_due_dict={"week1": ["2022-8-22  6:00"  , "2022-9-4   23:59" ], 
                   "week2": ["2022-9-4   23:59" , "2022-9-11  23:59" ], 
                   "week3": ["2022-9-11  23:59" , "2022-9-18  23:59" ], 
                   "week4": ["2022-9-18  23:59" , "2022-9-25  23:59" ], 
                   "week5": ["2022-9-25  23:59" , "2022-10-2  23:59" ], 
                   "week6": ["2022-10-2  23:59" , "2022-10-16 23:59" ], 
                   "week7": ["2022-10-16 23:59" , "2022-10-20 23:59" ]
                  }

quiz_necessary_elements = ['id','author', 'section','description','level','quiz_type'] # and id

# These are the elements the old quiz has that are not necessary for the new quiz delivery
quiz_non_necessary_elements = ['qzid', 'logx','passed','seed','from','submission']

# database name
backup_path = os.path.dirname(os.path.abspath(os.path.abspath(__file__)+'/../../..'))+'/backup'

# backup time
backup_interval = 600 # seconds

# user_raw_data
user_raw_path = os.path.dirname(os.path.abspath(__file__))+'/user_raw.txt'

# password_yaml
password_yaml = os.path.dirname(os.path.abspath(__file__))+'/password.yaml'

