from django.db import models
import datetime

# Create your models here.
class Post(models.Model):
    text=models.TextField()
    author_name= models.CharField(max_length=50)
    author_netid = models.CharField(max_length=8)
    pub_date = models.DateTimeField(default=datetime.datetime.strptime('2022-7-26 6:00','%Y-%m-%d %H:%M').astimezone(datetime.timezone(datetime.timedelta(hours=0))))
    title = models.CharField(max_length=100)
    level = models.IntegerField(default=0)
    question_id = models.IntegerField(default=0)
    category = models.IntegerField(default=0)
    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField()
    author_name = models.CharField(max_length=50)
    author_netid = models.CharField(max_length=8)
    pub_date = models.DateTimeField(default=datetime.datetime.strptime('2022-7-26 6:00','%Y-%m-%d %H:%M').astimezone(datetime.timezone(datetime.timedelta(hours=0))))
    def __str__(self):
        return self.text

## reply
