
import  os,datetime,time,shutil
from settings import backup_path, backup_interval

db_sqlite = os.path.abspath(os.path.abspath(__file__)+'/../../')+'/db.sqlite3'

s = 1

# improt shutil,os

# shutil.copy("file.txt","file_copy.txt")

# # or

# shutil.copy("file.txt",os.path.join(os.getcwd(),"copy"))


def back_up_database():
    data_base_name = datetime.datetime.strftime(datetime.datetime.utcnow()+datetime.timedelta(hours=8),'%Y-%m-%d-%H-%M-%S')


    if len(os.listdir(backup_path))!=100:  # This part can be modified !!!!!!!!!!!
        shutil.copy(db_sqlite,backup_path+'/'+data_base_name+'_db.sqlite')

    else:
        min_file = ""
        min_time = datetime.datetime.strptime("2025-1-1-1-1-1",'%Y-%m-%d-%H-%M-%S')
        for i in os.listdir(backup_path):
            str_time = datetime.datetime.strptime(i[:i.find('_')],'%Y-%m-%d-%H-%M-%S')
            if str_time < min_time:
                min_time = str_time
                min_file = i
        
        os.remove(backup_path+'/'+min_file)
        shutil.copy(db_sqlite,backup_path+'/'+data_base_name+'_db.sqlite')

    time.sleep(backup_interval)
    back_up_database()
    pass

if __name__=='__main__':
    back_up_database()
