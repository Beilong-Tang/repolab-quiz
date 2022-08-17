## Introduction

This project is called simple-judge. This website is to be used as CS201 quiz website.

### Two main functions :

1. Quiz function
2. Quiz Chat Room Function

---

---

## Models

The model can be thought of as the template of the database. We can use the model interface to interact with the database. 

Basically we have 5 models which are **Student, Question, Questiondict, Post, Comment. **

- Student focuses on the user authentication, and everything that is unique to student like name, net id etc.

- Question focuses on the status (pass or fail) of each question in Student.

- Questiondict focuses on the Quiz description, blanks, answers that are common to all users.

- Post focuses on the forum post.

- Comment focuses on the Comment of forum post.

A quiz can be considered as **Question + Questiondict**. For simplicity, Question is the status, while Questiondict is the description, and we use **question_id** as a bridge to connect them. By doing so, we can satisfy that every student is looking at the same quiz content but with the different pass status. To record the passing data, we only need to focus on Question. 



---

---

### Student

**Location** : simple-judge/models

Do not be tricked by its name, this model can be considered as **all users**, including TAs and Prof.

The detailed filed of the model can be found in the python source code like its type, default value etc. 

This model contains the following fields:

---

#### User

This is connected to django's  default user field. We mainly use the field to do the user authentication like login, logout, change password etc. 

**Note: The username equals to the student's netid instead of student's name**

To find the student with user, we can do 

```python
s = Student.objects.get(student_netid = request.user.username)
```

---

#### Student_name 

---

#### Student_netid

This is student's netid, which is the user's username.

---

#### question_due_dict

This dict looks sth. like

```python
question_due_dict={ 'week1':['2022-7-22 6:00','2022-7-30 9:00'],
                    'week2':['2022-7-29 11:51','2022-8-29 23:59'],
                    'week3':['2022-7-28 6:00','2022-8-29 23:59'],
                    'week4':['2022-7-28 6:00','2022-8-29 23:59'],
                    'week5':['2022-7-28 6:00','2022-8-29 23:59'],
                    'week6':['2022-8-30 6:00','2022-9-2 23:59'],
                    'week7':['2022-8-30 6:00','2022-9-2 23:59'],
                  }
```

It is basically a dictionary that contains the name of the Quiz, the start_time and the due_time. The start_time is the first element of the dictionary's value, and the due_time is the second.  

In default, each student has the same question_due_dict which corresponds to the real open and due time for each quiz. If a student would like a due postpone, we can change the question_due_dict.

```python
# s is the student 
s = Student.objects.get(student_netid='bt132')
s.question_due_dict['week1'][1]='2022-8-30 9:00'
# save the result
s.save()
```

---

#### offline_time, online_time

These two fields are used to check if the student is online or not. Whenever a student sends a request to the server (going to the other page, forum post ,submit the quiz), the offline_time and online_time will be refreshed. The online_time is the time when the student sends the request, and the offline_time is the online_time adding a delta of time. This delta of time can be 10 minutes, 20 minutes or 30 minutes. This means that if the student does not send any request to the server in the delta of time, then he/she is considered to be logged out. This method is from the Internet, and we cannot 100% record the online status so far. 

---

#### level

This integer field is used to distinguish between student, TA and professor. (I will implement this function once professor gives me the list of the student)

**0 -> student**

**1 -> TA (Beilong, Yike, Yantao)**

**2 -> Prof. Long**

|       User        | Do the quiz | Go to quiz admin page (only quiz) | Go to admin page |
| :---------------: | :---------: | :-------------------------------: | :--------------: |
| Student (level=0) |      ✓      |                 x                 |        x         |
|   TA (level=1)    |      ✓      |                 ✓                 |        ✓         |
|  Prof (level=2)   |      ✓      |                 ✓                 |        ✓         |

Basically, TA and prof have the same authority. 

---

#### forum_seen, comment_seen , forum_star

These fields are not that important. 

Forum_seen will show the user the forum post that they haven't seen. 

Comment_seen will show the user the comment post they haven't seen.

Forum_star is the list of post that students favorite.

---

#### messages

This field is related to one of the new pages that is called **message**.

**messages** will record the new message in the forum and show them in the message page. 

For example, you might see 'Alice replied to You in Week1 Problem1 How to code in java ... ' in your message page. 

This **message** record process will happen if:

1. You are the poster, and someone commented or replied to your post.
2. You commented to a post, and someone commented or replied to that post after you.

---

---

### Question

**Location:** simple-judge/models

One of the features is that this model has a one-to-one tie to student. This model contains the field that specifies the status of the quiz (pass or fail) , and everyone's status might be different, so it has to be connected to a specific student. 

Here are the fields of Question:

---

#### student

This actually cannot be called a field. This is called a **ForeignKey**. For simplicity, this is just the **Student** Model. It specifies which student the question belongs to.

---

#### question_title

This is the title of the quiz.

---

#### question_id

For each quiz, it has a unique question_id. If we want to search for the content of the quiz like description, we will need to use the id. 

---

#### ifpassed (boolean)

This field can be tricky.  

If **ifpassed** is True, it means that student have passed the quiz. **However**, if **ifpassed** is False, it does not mean anything. This field has to be viewed withe **submission_times** in order to get the status of the quiz.



---

#### submission_times (int)

**This part below can be ignored!**

> _The default value is 5, meaning that student has 5 times to **fail**. If student's answer failed, the submission_times would minus one. If the student's answer is correct, it will **not** minus one. If student's answer failed, and submission_times is 1, the student will failed._

We don't need to understand the principle behind it, since it is a bit complicated. We only need to know how to judge the status of the quiz (pass or fail)

 The passing Status can be judged combing **ifpassed** and **submission_times**:

| ifpassed | submission_times |     Status     |
| :------: | :--------------: | :------------: |
|   True   |        +         |      pass      |
|   True   |        0         | Never happened |
|  False   |        +         |    ongoing     |
|  False   |        0         |      fail      |

We only need to keep this form in mind to tell if a quiz is passed, failed or ongoing.

---

#### logx (textfield)

This string field records the history of a student's submission. 



> Even if a student has passed or failed the test, he/she can still do the test and the history will be recorded. 

Each submission is combined with the previous submission history into a string. 



> The part below can be ignored.

For example:

```
d#d#d#d@2022-08-12 09:06:39$d#d#d#d@2022-08-12 09:06:41$d#d#d#d@2022-08-12 09:06:43$d#d#d#d@2022-08-12 09:06:45$d#d#d#d@2022-08-12 09:06:46$
```

This is an example of a logx. Each submission is separated by **$**. In each submission, each blank/choice is separated by **#**, and each submission time is followed by a **@**.



---

---

### Questiondict

**Location:** simple-judge/models

This model contains the basic content of each quiz.

Here the fields of Questiondict:

---

#### question_type 

The type a question contains mult, blank, and code.

---

#### 	question_title 

This is the title of the question, which is determined by the question json file name in repolab-quiz/bank/week.

---

#### question_content (jsonfield)

For simplicity, this field is equals the quiz json file, including author, answer etc.

---

#### question_id

This id is unique to each quiz. We use it to distinguish between each quiz.

---

#### question_week

This field is not that important. It specifies the week the question belongs to. 

---

#### question_level

This shows the level of the question.

---

---

### Post

**Location:** forum/models

This model focuses on the information of a student's post.

**Note that this Post is only used for the CS201 Quiz Post instead of the whole cs201 forum post website. Ed still needs to be used for assignment etc.!**

Here are the fields of the **Post**:

---

#### text

The text of the post.

---

#### author_name

The author of the post, it should be the same as the student_name.

---

#### author_netid

The author's netid of the post, it should be the same as student_netid

---

#### pub_date

This is the publication date of the post. Note that the pub_date's time zone is CST (UTC+8) instead of UTC.

---

#### title

The title of the post

---

#### level (int)

For now , this int field should only have two values, 0 and 1.

If the value is 0, it means that your post as well as your author_name is shown to everyone.

If the value is 1, it means that your name will be hidden (anonymous).

---





[image]('/static/forum/images/Bob_92_2022-08-13-21-22-56_0_.png')







## Instruction

Below are some instructions of the website. Make sure you are in our project main directory _(simple-judge/code)_.

### How to Create user

```
python3 shell.py create_user bt132 Beilong_Tang 0
```

This will create a user whose name is 'Beilong Tang', and his netid is 'bt132'. His level is 0.

> You should have a '_' between the first name and last name of the student name.





