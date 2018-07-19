from django.db import models

# Create your models here.

class User(models.Model):
    wxId = models.CharField(max_length=128)
    name = models.CharField(max_length=64,blank=True,null=True)
    createTime = models.DateTimeField(auto_now_add=True)
    photoUrl = models.CharField(max_length=256)
    time = models.DateTimeField(auto_now=True)

    def __str__(self):  # __unicode__ on Python 2
        return self.wxId

class Thought(models.Model):
    userId = models.ForeignKey(User)
    auther = models.CharField(max_length=64,blank=True,null=True)
    createTime = models.DateTimeField(auto_now_add=True)
    content = models.TextField(max_length=8192)
    discussNum = models.IntegerField(default=0)
    supportNum = models.IntegerField(default=0)
    duration = models.FloatField() #距离时长
    selfW = models.FloatField(default=0) #自定义权重
    weight = models.FloatField(default=0)   #排名权重

    def __str__(self):  # __unicode__ on Python 2
        return self.content

class DiscussOne(models.Model):
    thoughtId = models.ForeignKey(Thought)
    userId = models.ForeignKey(User)
    auther = models.CharField(max_length=64, blank=True, null=True)
    content = models.TextField(max_length=1024)
    createTime = models.DateTimeField(auto_now_add=True)
    discussNum = models.IntegerField(default=0)
    supportNum = models.IntegerField(default=0)

    def __str__(self):  # __unicode__ on Python 2
        return self.content

class DiscussTwo(models.Model):
    userId = models.ForeignKey(User)
    auther = models.CharField(max_length=64, blank=True, null=True)
    discussoneId = models.ForeignKey(DiscussOne)
    createTime = models.DateTimeField(auto_now_add=True)
    content = models.TextField(max_length=1024)

    def __str__(self):  # __unicode__ on Python 2
        return self.content

class SupportThought(models.Model):
    userId = models.ForeignKey(User)
    thoughtId = models.ForeignKey(Thought)
    createTime = models.DateTimeField(auto_now_add=True)

    def __str__(self):  # __unicode__ on Python 2
        return self.userId

class SupportDisone(models.Model):
    userId = models.ForeignKey(User)
    discussoneId = models.ForeignKey(DiscussOne)
    createTime = models.DateTimeField(auto_now_add=True)

    def __str__(self):  # __unicode__ on Python 2
        return self.userId

#开发者列表
class Developer(models.Model):
    name = models.CharField(max_length=40)
    key = models.CharField(max_length=64)
    secret = models.CharField(max_length=64)

    def __str__(self):  # __unicode__ on Python 2
        return self.name

#权重表
class WeightFactor(models.Model):
    name = models.CharField(max_length=32)
    time = models.FloatField(default=1)
    sup = models.FloatField(default=1)
    dis = models.FloatField(default=1)

    def __str__(self):  # __unicode__ on Python 2
        return self.name