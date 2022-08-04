import os,time
first_command = ['week1','week2','week3','week4','week5','week6','week7']

ldir = os.path.dirname(os.path.abspath(__file__))
home_dir='%s/../../repolab-quiz/bank'% ldir

def pull():
    a = os.path.abspath(os.getcwd())
    os.chdir(home_dir)
    print('INFO cwd =  %s' % os.getcwd())
    print('INFO cmd =  %s' % 'git pull')
    os.system('git pull')
    os.chdir(a)
    pass
def update():
    print("Uploading: may take 7 seconds")
    for i in first_command:
        cmd = 'python3 shell.py %s' % i
        print('Update %s' % i)
        os.system(cmd)
        time.sleep(1)
        pass
    pass
    
if __name__ == '__main__':
    pull()
    update()
