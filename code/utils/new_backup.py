import  os,datetime,time,shutil
from settings import backup_path, backup_interval


db_sqlite = os.path.abspath(os.path.abspath(__file__)+'/../../')+'/db.sqlite3'

## This will start to back up the database
if __name__=='__main__':


    
    while True:
        # overwritten
        data_base_name = datetime.datetime.strftime(datetime.datetime.utcnow()+datetime.timedelta(hours=8),'%Y-%m-%d-%H-%M-%S')
        if len(os.listdir(backup_path))==100:
            min_file = ""
            min_time = datetime.datetime.strptime("2025-1-1-1-1-1",'%Y-%m-%d-%H-%M-%S')
            for i in os.listdir(backup_path):
                str_time = datetime.datetime.strptime(i[:i.find('_')],'%Y-%m-%d-%H-%M-%S')
                if str_time < min_time:
                    min_time = str_time
                    min_file = i
            os.remove(backup_path+'/'+min_file)
            shutil.copy(db_sqlite,backup_path+'/'+data_base_name+'_db.sqlite')
            print("%s replace %s" %(data_base_name, min_file))
        else:
            shutil.copy(db_sqlite,backup_path+'/'+data_base_name+'_db.sqlite')
            print("%s created" %(data_base_name))
            pass

        time.sleep(backup_interval)
