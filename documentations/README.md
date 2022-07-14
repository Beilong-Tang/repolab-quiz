Update_Date: 2022/7/14

## Instructions

## Environment setup

Go to **simple/judge/deploy** folder, and do

```
./ first_time.sh
```
This will help you install the required dependencies and environments for the quiz.

## User setup

If it is the first time you clone the project, your database will be empty (the database is not in the project), including all the modules and users.

The first thing we should do is to create a super user, who is the admin of the project, and can have access to the admin page where it can modify all the data in the data base.

To create the admin, we need to go the the home directory of the project, which is 'simple-judge/code/' where you can see 'manage.py' in the directory.

**'manage.py'** is the key of the project because it is related to the server of the project, and the database of the project. 

To set up superuser, we do 

```
python3 manage.py createsuperuser
```

Then, we input some basic information of the account like username and password.

Now the superuser is created.

## APPs

Before we go deeper about the database and models. We have to know the structure of the whole project.

Make sure we are in 'simple-judge/code', and we will see the following directrories in it.

```
.
├── __pycache__
├── quiz
├── repolab
├── simple_judge
├── templates
└── utils
```

**repolab** is a project template, and we do not need to consider a lot about it.

**simple_judge** and **quiz** are two apps of the current of the project

---

**simple_judge** contains the following parts:

1. All the models (Questiondict, Question, Student)
2. The 'Sign-in, Sign-out' page

---

**quiz** contains the following parts:

1. All the Quiz pages (Basically every views about quiz)

--- 

**utils** are contain some plugins of the project.

## Models

Our models are in 'simple-judge/code/simple_judge/models.py'.

There are three models I currently use, which are 'Questiondict', 'Student', 'Question'.

All the models are python classes. All the properties in that class like CharField, IntegerField are also python classes.

- The **Student** stores the basic information of the student, which contains:
    1. user information (username, password).
    2. student_name
    3. student_id

- The **Question** stores some basic information of the question related to different student, which contains:
    1. student (Which student the question belongs to)
    2. question_title
    3. ifpassed
    4. pub_date
    5. due_date
    6. submission_times 

- The **Questiondict** stores some basic information of the question which is unique among students like the question content, which contains (Actually, we do not really need this database, we can directly import data from repolab-quiz ):
    1. question_type
    2. question_title
    3. question_content (Json File)
    4. question_id (haven't been used yet)
    5. question_level
    6. question_week 

To see the details of each property, can go to the python source file to see. 

## Database

To access the database, we can do

```
python3 manage.py shell
```

After doing so, we should enter a python terminal. 

The first thing we need to do is to import our models. 

```python
>>> from simple_judge.models import Questiondict, Student, Question
>>> from django.contrib.auth.models import User   # Since student is related to user, we should also import user if we want to create student
```

Firstly, let us try to **create a user**:

```python
>>> u1= User.objects.create_user(username='Beilong', password='Beilong_password') # This will create a user which will be directly saved
>>> s1= Student(user=u1, student_name='Beilong', student_id=0) # This will create a student
>>> s1.save() # This will save the current student.

>>> Student.objects.get(student_name='Beilong') # This is a test line.
<Student: Beilong> # Student created successfully
```

Next, let us **assign user a few questions**.
```python
>>> s = Student.objects.get(student_name='Beilong')
>>> s # test
<Student: Beilong>
>>> s.question_set.create(question_title='test1', ifpassed=False)
>>> s.save()
>>> s.question_set.all() # test line
<QuerySet [<Question: test1>]> # question is in the user Beilong 
```

---

Note that the student is only assigned with the **question title**, instead of the question content. Since the question content will be unique to all students, we will import our quizes (json files) in **Questiondict** database instead of **Question**. We only need to use the question_title as our index to search for the quiz (json files) in our Questiondict.  

---

Let us create some questions in the **Questiondict**
```python
>>> q=Questiondict(question_type='blank', question_title='test1', question_content={'description':'1+1=__2__', 'answers':2}) # Create
>>> q.save() # Save
```

We can note that the question_title is 'test1', which is the same as that in user Beilong. It is exactly what we want!

Let us try to find the question:
```python
>>> s = Student.objects.get(student_name='Beilong')
>>> q = Questiondict.objects.get(question_title=s.question_set.get(question_title='test1').question_title)
>>> q.question_content   # We have the quiz content we want!
{'description': '1+1=__2__', 'answers': 2}
>>> q.question_content.get('description')
'1+1=__2__'

# To delete object:
>>> q.delete()

```

After browsing the code above, you can have a little mind what the code is doing in view.py.

## shell.py (This step can be improved in the future!)

Before we jump to the Questiondict importing, make sure all the quizes' json files are generated!

In 'repolab-quiz/bank', do
```python
python3 generate.py
```

Let us jump to the Questiondict importing.

This will generate all the quizes (mult, blank and code.)

we go to 'simple-judge/code/shell.py' and find
```python
## Change the home_dir at here 
home_dir='/mnt/c/Users/Beilong Tang/Desktop/Main/CODE/DJANGO_new/repolab-quiz/bank'

########################################
```

This is the home_dir of my quiz. You need to **change it to yours**. 

After this is done, we do:
```
python3 shell.py blank
```

This will import all the blank questions.

After this is done, type

```
>>> exit()
```

This will exit from the python terminal.

We then do 
```
python3 shell.py mult
```

and 

```
python3 shell.py code
```

After these steps, all the quizes should be imported to the Questiondict. Go to the admin page to check out!

## Assign Week to each quiz

After importing all the quizzes into the Questiondict, we then need to assign them to different weeks.

Go to the folder 'simple-judge/code', and you will see 'shell.py' and do 
```
python3 shell.py week
```

This instruction will assgin quizzes in the Questiondict from week1 to week7. **Note** that the assignment now will only assgin weeks according to chapters instaed of sections. Further imporvment should be done on it.

## Assgine Question to Students

Now that we have the questions and its corresponding weeks, we can assign them to students.

This time, the method might be a bit **different**.

We go to 'simple-judge/code' and do

```
python3 manage.py shell
```

In the terminal python window, we do

```python 
>>> from simple_judge.models import Question, Student, Questiondict
>>> from utils.AssignQuestionWeek import question_assign_fixed_per_week as qafpw
>>> qafpw()
```

This will assign questioins to students accroding to weeks. The default setting is that for each week, we will randomly choose 10 quesitons from that week and assign them to students. (My wish is to assgin them 24 questions per week where level 1:2:3=3:2:1).

## Check in the admin page

After you finish the steps above, you can go to the admin page and check the result.





















