# This file is a setting file
import os

# quiz week folder
quiz_dir='/mnt/c/Users/Beilong Tang/Desktop/Main/CODE/DJANGO_new/repolab-quiz/bank/week'

ldir = os.path.dirname(os.path.abspath(__file__))
quiz_dir='%s/../../../repolab-quiz/bank/week'% ldir

# question_due_dict
question_due_dict={"week1": ["2023-8-21  6:00"  , "2023-9-3   23:59" ], 
                   "week2": ["2023-8-27   23:59" , "2023-9-10  23:59" ], 
                   "week3": ["2023-9-3  23:59" , "2023-9-17  23:59" ], 
                   "week4": ["2023-9-10  23:59" , "2023-9-24  23:59" ], 
                   "week5": ["2023-9-17  23:59" , "2023-10-1  23:59" ], 
                   "week6": ["2023-9-24  23:59" , "2023-10-8  23:59" ], 
                   "week7": ["2023-10-1  23:59" , "2023-10-15  23:59" ]
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

