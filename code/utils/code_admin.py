# This code is to generate the instruction.txt, record the input, run the check method, and call if pass or not.
#
#   Date: 2022/6/9

import os,subprocess,json,sys

#jsonfile is the quiz_content, answer is the answer sets
def check_answer_code(jsonfile, answer):
    clean_output=False
    # Get the code
    code=jsonfile['code']
    blank=0
    for i in range(0,len(answer)):
        code=code.replace('__'+(str)(blank)+'__',answer[i])
    if 'wdir-code' not in os.listdir(os.getcwd()):
            os.system('mkdir '+'wdir-code')
    #code_file=open('quiz-gen/'+self.data['title']+'.txt','w')
    code_file=open('wdir-code/'+jsonfile['titile']+'.txt','w')
    code_file.write(code)
    code_file.close()
    # Get the checking method #jsonfile['check']
    check_file=open('wdir-code/'+'check.txt','w')
    check_file.write(jsonfile['check'])
    check_file.close()
    # Get the instruction
    instruction_file=open('wdir-code/'+'instruction.txt','w')
    instruction_file.write(jsonfile['instruction'])
    instruction_file.close()
    ain = open('wdir-code/instruction.txt','rb') # fixed by lj -- remove use of /bin/more
    p2=subprocess.Popen(args='jshell',shell=True,stdin=ain,stdout=subprocess.PIPE)
    output_file=open('wdir-code/data.txt.save','wb').write(p2.stdout.read()) # fixed by lj -- remove use of nano
    output_file.close()
    output_file=open('wdir-code/data.txt.save','r')
    ## Ready to check answers
    if jsonfile['main_output']!="":
        main_output=jsonfile['main_output'].lstrip('\n').rstrip('\n').split()
        content=output_file.read()
        content=content[content.find('check()'):]
        for item in main_output:
            if content.find(item)!=-1:
                content=content[content.find(item)+len(item):]
            else:
                if clean_output !=False:
                    clean_all()
                return False
        if clean_output !=False:
            clean_all()
        return True
    else:
        for line in output_file.readlines():
            if line.find('check()true')!=-1:
                if clean_output !=False:
                    clean_all()
                return True
        if clean_output !=False:
            clean_all()    
        return False


def clean_all():
    os.system('rm wdir-code/check.txt')
    os.system('rm wdir-code/data.txt.save')
    os.system('rm wdir-code/instruction.txt')
    os.system('rm wdir-code/*.txt')







class quiz_file:

    def __init__ (self, quiz_templete):
        self.quiz_templete_name=quiz_templete

        self.create_quiz_working()

        self.load_data()

    def create_quiz_working(self):

        ### This is to create the 'wdir-quiz' file
        if 'wdir-quiz' not in os.listdir(quiz_templete_dir):
            os.system('mkdir '+'quiz-gen/wdir-quiz')

        if  self.quiz_templete_name not in os.listdir(quiz_working_dir):
            file_templete= open(quiz_templete_dir+'/'+self.quiz_templete_name,'r')
            data = json.load(file_templete)
            working_quiz=open(quiz_working_dir+'/'+self.quiz_templete_name,'w')
            json.dump(data,working_quiz,indent=2)
            pass
        pass

    def load_data(self):
        self.data = json.load(open(quiz_working_dir+'/'+self.quiz_templete_name,'r'))
        pass

    def save_data(self):
        json.dump(self.data,open(quiz_working_dir+'/'+self.quiz_templete_name,'w'),indent=2)
        pass


    # This is to concentrate the input and generate the corrsponding code file to run in jshell
    def input(self,debugging=False):
        errormsg='---------------------------\nWrong Answer, please try again.\nPress Enter to try again'
        answer=""
        code=self.data['code']
        blank = 0
        answer_set=[]
        ifskip=False
        print(self.data['description'])

        ## Loop for answer check:
        while True:
            while self.data['code'].find('__'+(str)(blank)+'__')!=-1:
                answer=input('__'+(str)(blank)+'__'+" : ")
                ifskip=True if answer=='s' else False
                if ifskip :
                    break
                answer_set.append(answer)
                code=code.replace('__'+(str)(blank)+'__',answer)
                blank=blank+1
            if ifskip:
                break
            self.update_logx(answer_set)
            print('\nYour Code:\n\n'+code)
            if(self.check(code,debugging)==True):
                break
            #print(errormsg)
            input(errormsg)
            print(self.data['description'])
            code=self.data['code']
            blank=0
        if not ifskip:
            input("---------------------------\nCongratulation, you passed!\nPress Enter to continue")
            self.data['passed']='True'
            self.save_data()

    def check(self,code,debugging):
        code_file=open('quiz-gen/'+self.data['title']+'.txt','w')
        code_file.write(code)
        code_file.close()
        return self.create_and_check(debugging)
        pass
    
    def create_and_check(self,debugging=False):
        print("\nChecking...\n")
        # create instruction file
        self.create_instruction_file()
        self.create_check_file()
        #p1=subprocess.Popen(['/bin/more','quiz-gen/'+'instruction.txt'],stdout=subprocess.PIPE)
        ain = open('quiz-gen/instruction.txt','rb') # fixed by lj -- remove use of /bin/more
        #p2=subprocess.Popen(args='jshell',shell=True,stdin=p1.stdout,stdout=subprocess.PIPE)
        p2=subprocess.Popen(args='jshell',shell=True,stdin=ain,stdout=subprocess.PIPE)
        #p3=subprocess.run(args=['rm','quiz-gen/data.txt.save'])
        #p4=subprocess.run(['nano','quiz-gen/data.txt'],stdin=p2.stdout)
        open('quiz-gen/data.txt.save','wb').write(p2.stdout.read()) # fixed by lj -- remove use of nano
        if True or p4.returncode>=0 :
            ifpass=self.check_code()
            # This is to rm the file to make it look more simple
            if debugging==False:
                os.system('rm quiz-gen/check.txt')
                os.system('rm quiz-gen/data.txt.save')
                os.system('rm quiz-gen/instruction.txt')
                os.system('rm quiz-gen/*.txt')
        return ifpass
        pass

    def check_code(self):
        output_file=open('quiz-gen/data.txt.save','r')
        if self.data['main_output']==None:
            for line in output_file.readlines():
                if line.find('check()true')!=-1:
                    return True
                    ##
            return False
        else:
            ### Improvement here
            content=output_file.read()
            content=content[content.find('check()'):]
            main_output=self.data['main_output'].split()
            return self.check_answer(content,main_output)

    def check_answer(self,content,answer):
        for item in answer:
            if content.find(item)!=-1:
                content=content[content.find(item)+len(item):]
            else:
                return False
        return True

    def create_instruction_file(self):
        instruction_file=open('quiz-gen/instruction.txt','w')
        instruction_file.write(self.data['instruction'])
        instruction_file.close()

    def create_check_file(self):
        check_file=open('quiz-gen/check.txt','w')
        check_file.write(self.data['check'])
        check_file.close()
        pass


    def update_logx(self, answer_set):
        self.data['logx'].append(answer_set)
        self.save_data()
        pass



        #if self.filename not in os.listdir(os.getcwd()+'/quiz-gen/wdir-quiz'):
        #    self.data=json.load(self.file)
        #else: 
        #    if answer=="":
        #        self.data=json.load(open('quiz-gen'+'/'+'wdir-quiz'+'/'+self.filename,'r'))
        #        pass
        #    else:
        #        self.data=json.load(open('quiz-gen'+'/'+'wdir-quiz'+'/'+self.filename,'r'))
        #        self.data["logx"].append(answer)
        #self.file = open('quiz-gen'+'/'+'wdir-quiz'+'/'+self.filename,'w')
        #json.dump (self.data, self.file, indent=2)  


if __name__=='__main__':

    quiz_templete_dir=os.getcwd()+'/quiz-gen'
    quiz_working_dir=os.getcwd()+'/quiz-gen/wdir-quiz'
    try:
        quiz_all=[item for item in os.listdir(quiz_templete_dir) if item.find('.json')!=-1]
    except:
        assert False,'Please make gen before make test'
    ## Initialize the wdir-quiz
    quizes=[quiz_file(item) for item in quiz_all]
    for quiz in list(filter(lambda i:i.data['passed']=='False',quizes)):
        if len(sys.argv)>1:
            if sys.argv[1]=='debug':
                quiz.input(debugging=True)
        else:
            quiz.input()




        #quiz.update("")
        #pass_quiz=json.load(open('quiz-gen/'+item,'r'))
        #if pass_quiz['passed']=='True':
        #    continue
        #quiz.input(True)

    #assert(len(filename)!=0),"Please generate the quiz first (make gen) before test (make test)"
    #filename=filename[0]
    #quiz= quiz_file(filename)

