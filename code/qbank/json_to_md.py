import os, sys, json, re

# if __name__ == '__main__':
#     if len(sys.argv)==1:
#         print(
# '''
# Add 'all' to generate markdown files for all the json files 'python3 json_to_md.py all'
# Add 'week_' to generate markdown files for the json files in the specific week 'python3 json_to_md.py week1'
# ''')
#     else:
#         if sys.argv[1]=='all':
#             root_path = os.path.dirname(os.path.abspath(__file__))
#             file = os.path.join(root_path,'week1')
#             print(os.listdir(file))
#             pass
#         elif sys.argv[1] in ['week1','week2','week3','week4','week5','week6','week7']:
#             root_path = os.path.dirname(os.path.abspath(__file__))
#             file = os.path.join(root_path,sys.argv[1])
#             open(os.path.join(file,sys.argv[1]+'.md'),'w').write("") 
#             for _quiz in list(filter(lambda x: x.endswith(".json"), os.listdir(file))):
#                 with open (os.path.join(file,_quiz),'r') as quiz_file:
#                     content = json.load(quiz_file)
#                     if content['question_type']=='blank':
#                         with open (os.path.join(file,sys.argv[1]+'_blank.md'),'a') as md_file:
#                             md_file.write('## '+ content['question_title']+'\n\n')
#                             md_file.write(content['question_content']['description'])
#             pass
#         else:
#             raise Exception("Please input the correct command")

root_path = os.path.dirname(os.path.abspath(__file__)) # qbank

md_path = os.path.join(os.path.dirname(os.path.dirname(root_path))
                        ,'repolab-quiz','bank')


class Json_File():

    def __init__(self) ->None:
        self.content = None # json content
        pass

    def get_content(self) ->dict:
        return self.content

    def load(self,filepath) -> None:
        self.content = self._find_content(filepath)

    def _find_content(self,filepath) -> dict:
        json_dict = json.load(open(filepath,'r'))
        return json_dict

    def markdown_update(self) -> None:
        section = self.get_content()['question_content']['section']
        quiz_type = self.get_content()['question_type']
        title = self.get_content()['question_title']

        self.md_update(section,quiz_type,title)
    
        print("finished")

    def md_update(self,section,quiz_type,title) -> None:
        # md_array = None
        chap_num:str = str(section[0])
        quiz_content = self.modify_quiz_content(quiz_type,self.get_content())
        if quiz_type =='blank':
            # chap_num:str = str(section[0])
            md_file_path = os.path.join(md_path,'princeton-book','chap0'+chap_num,'sec-'+section,'sec-'+section+'.para.qz.md')
            with open(md_file_path,'r') as f:
                md_array = f.read().split("##")

        elif quiz_type == 'mult':
            md_file_path = os.path.join(md_path,'mult','chap0'+chap_num,'sec-'+section,'sec-'+section+'.mult.md')
            with open(md_file_path, 'r') as f:
                md_array = ('\n'+f.read()).split("\n## ")

        elif quiz_type =='code':
             md_file_path = os.path.join(md_path,'code','chap0'+chap_num,'sec-'+section,'sec-'+section+'.code.md')
             with open(md_file_path,'r') as f:
                md_array=('\n'+f.read()).split("\n## ")

        add = True
        for index,i in enumerate(md_array):
            if i.lstrip().startswith(title):
                md_array[index] = quiz_content 
                add = False
                break
        if add:
            if md_array[-1].endswith('\n\n')!=True:
                md_array[-1]+='\n\n'
            md_array.append(quiz_content)

        # print(("##").join(md_array))
        if quiz_type =='blank':
            md_content = (("##").join(md_array)).lstrip("\n")
        elif quiz_type=='mult' or quiz_type=='code':
            md_content = (("\n## ").join(md_array)).lstrip("\n")
        
        open(md_file_path,'w').write(md_content)
    
    def blank_quiz_content_convert(self,content:str, title:str, answer:list, level:int, author:str) -> str:
        original_title = content[:content.find("\n")]
        title_level_author = title+"\n"+":jq_level="+str(level)+":\n"+":author="+author+":"
        content = content.replace(original_title,title_level_author)
        for index, _answer in enumerate(answer):
            content=content.replace("_____("+str(index)+")\\___","__"+_answer+"__")
        return ' '+content+'\n\n---\n\n'

    def mult_quiz_content_convert(self,content:str,title:str,choices:list,author:str,level:int,answers:list) ->str:
        original_title = content[:content.find("\n")]
        title_level_author = title+"\n"+":jq_level="+str(level)+":\n"+":author="+author+":"
        Quote = False
        if content.find("Excerpt From Computer Science")!=-1:
            Quote = True
        content = content.replace( original_title,title_level_author)
        content = (content[:content.find("**Choices:**")]
                  +"### Choices:"
                  +'\n\n'
                  +"\n\n".join(choices)
                  +"\n\n### Answers:\n\n"
                  +self.mult_answers_convert(answers)
                  +'\n\n')
        if Quote:
            content=(content
                    +"### Quote:\n\n*Excerpt From Computer Science Sedgewick, Robert,Wayne, Kevin. This material may be protected by copyright.*\n\n"
                    )
        return content+"---\n"

    def mult_answers_convert(self,answers:list) -> str:
        answer_str=""
        for index, _answer  in enumerate(answers):
            if _answer == 'True':
                answer_str += chr(index+97) + " "
        return answer_str.rstrip()

    def code_quiz_content_convert(self,content:str,title:str,level:int,author:str,check:str,main_output:str,answers:str) -> str :
        original_title = content[:content.find('\n')]
        title_level_author = title+"\n"+":jq_level="+str(level)+":\n"+":author="+author+":"
        content = content.replace( original_title,title_level_author)
        content +=("\n### Check:\n"
                  + check
                  + (("\n\n### Main:\n\n"+main_output) if main_output !=None else '')
                  +"\n\n### Answer:\n\n"
                  +("\n\n").join(answers))
        return content+"\n\n---\n"


    
    def modify_quiz_content(self, quiz_type:str,content:dict) -> str:
        
        if quiz_type=='blank':
            return self.blank_quiz_content_convert(content['question_content']['description'],
                                                   content['question_title'],
                                                   content['question_content']['answers'],
                                                   content['question_level'],
                                                   content['question_content']['author'])
        
        elif quiz_type=='mult':
            return self.mult_quiz_content_convert(content['question_content']['description'],
                                                  content['question_title'],
                                                  content['question_content']['choices'],
                                                  content['question_content']['author'],
                                                  content['question_level'],
                                                  content['question_content']['answers'])
        
        elif quiz_type=='code':
            return self.code_quiz_content_convert(content['question_content']['description'],
                                                  content['question_title'],
                                                  content['question_level'],
                                                  content['question_content']['author'],
                                                  content['question_content']['check'],
                                                  content['question_content']['main_output'],
                                                  content['question_content']['answers'])

if __name__=='__main__':
    js = Json_File()
    # file = os.path.join(root_path,'week1','101.json')
    # js.load(file)
    # js.markdown_update()

    if sys.argv[1] in ['week1','week2','week3','week4','week5','week6','week7']:
        file_root = os.path.join(root_path,sys.argv[1])
        json_files = list(filter(lambda x: x.endswith(".json"),os.listdir(file_root)))
        print(json_files)
        for file in json_files:
            json_file_path = os.path.join(file_root,file)
            js.load(json_file_path)
            js.markdown_update()
