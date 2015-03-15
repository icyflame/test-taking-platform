from django.db import models

# Create your models here.
class Question(models.Model):
	qtext = models.CharField(max_length=200)
	correctans = models.CharField(max_length=200)

class User(models.Model):
	name = models.CharField(max_length=200)
	password = models.CharField(max_length=200)
	username = models.CharField(max_length=30)

class Test(models.Model):
	tname = models.CharField(max_length=200)

class TestToAnswer(models.Model):
	qid = models.ForeignKey(Question)
	tid = models.ForeignKey(Test)
