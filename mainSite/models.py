from django.db import models
from django.forms import ModelForm

# Create your models here.
class Users(models.Model):
	username = models.CharField(max_length=50)
	voted = models.BooleanField(default=False)
	department = models.CharField(max_length=100)
	name = models.CharField(max_length=50)
	gender = models.CharField(max_length=1)
	course = models.CharField(max_length=30)
	hostel = models.CharField(max_length=30)
	encryptedPrivateKey = models.CharField(max_length=4096)
	'''Non empty only when user is logged in'''
	plaintextPrivatekey = models.CharField(max_length=2048)

	def __str__(self):
        	return self.username

#Create database for storing posts

class Candidates(models.Model):
	username = models.CharField(max_length=50)
	contestingPost = models.CharField(max_length=10,default='')
	details = models.CharField(max_length=10000)
	photo = models.CharField(max_length=100)
	approved = models.BooleanField(default=False)
	noOfVotes = models.IntegerField(max_length=6,default=0)
	def __unicode__(self):
        	return self.username

class Votes(models.Model):
	plainText = models.CharField(max_length=50)
	certificate = models.CharField(max_length=60)

	publicKey = models.ForeignKey("PublicKeys")
	challengeStr = models.ForeignKey("ChallengeStrings")

class ChallengeStrings(models.Model):
	challengeStr = models.CharField(max_length=2048)

class PublicKeys(models.Model):
	publicKey = models.CharField(max_length=2048)


# more fields to be added 

class Posts(models.Model):
	postName = models.CharField(max_length=50)
	postCount = models.IntegerField(max_length=3,default=0)
	voterGender = models.CharField(max_length=1)    #'M'/'F'/'a'
	voterCourse = models.CharField(max_length=2)		# 'UG'/'PG'/'a'
	eligibleGender = models.CharField(max_length=1)		#'M'/'F'/'a'
	eligibleCourse = models.CharField(max_length=2)     #'UG'/"PG"/'a'
	eligibleYear = models.CharField(max_length=2)		#minimum requirement of year


class New_Candidate(models.Model):
	name = models.CharField(max_length=50)
	post = models.CharField(max_length=4 ,default='')
	roll = models.IntegerField(max_length=10, default=0)
	department = models.CharField(max_length=100, default='')
	cpi = models.FloatField(max_length=4, default=0)
	sem = models.IntegerField(max_length=1, default=0)
	backlogs = models.CharField(max_length=50, default='')
	email = models.CharField(max_length=50, default='')
	contact = models.IntegerField(max_length=10, default=0)
	hostel = models.CharField(max_length=10,default='')
	room = models.CharField(max_length=10, default='')
	agenda = models.CharField(max_length=100000, default='')
	def __unicode__(self):
        	return self.name
