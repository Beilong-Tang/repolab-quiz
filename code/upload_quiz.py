import os
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
    for i in first_command:
        cmd = 'python3 shell.py %s' % i
        print('Update %s' % i)
        os.system(cmd)
        pass
    pass
    
if __name__ == '__main__':
    pull()
    update()
