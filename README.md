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









