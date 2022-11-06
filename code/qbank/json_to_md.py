import os, sys, json

if __name__ == '__main__':
    if len(sys.argv)==1:
        print(
'''
Add 'all' to generate markdown files for all the json files 'python3 json_to_md.py all'
Add 'week_' to generate markdown files for the json files in the specific week 'python3 json_to_md.py week1'
''')
    else:
        if sys.argv[1]=='all':
            root_path = os.path.dirname(os.path.abspath(__file__))
            file = os.path.join(root_path,'week1')
            print(os.listdir(file))
            pass
        elif sys.argv[1] in ['week1','week2','week3','week4','week5','week6','week7']:
            root_path = os.path.dirname(os.path.abspath(__file__))
            file = os.path.join(root_path,sys.argv[1])
            open(os.path.join(file,sys.argv[1]+'.md'),'w').write("") 
            for _quiz in list(filter(lambda x: x.endswith(".json"), os.listdir(file))):
                with open (os.path.join(file,_quiz),'r') as quiz_file:
                    content = json.load(quiz_file)
                    if content['question_type']=='blank':
                        with open (os.path.join(file,sys.argv[1]+'_blank.md'),'a') as md_file:
                            md_file.write('## '+ content['question_title']+'\n\n')
                            md_file.write(content['question_content']['description'])
            pass
        else:
            raise Exception("Please input the correct command")