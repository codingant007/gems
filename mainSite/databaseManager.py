import os
import sys
import json
from django.contrib.auth.models import User
from .models import Users, Candidates,Votes, PublicKeys, ChallengeStrings ,Posts
from django.db.models import Q
#from Crypto.PublicKey import RSA
import cryptography

def registerUsers(userList):
	"""Registers a new set of users as specified in userList.

	Should be called with a large number of users for good security (prefferably all that will ever be in the system.)

	userList -- list of dictionaries each depicting a user with the keys:
		'username', 'department', 'name', 'course'

	returns a list of passwords corresponding to each user
	"""

	noUsers = len(userList)
	passwords = [cryptography.generatePrintableRandomString() for i in range(noUsers)]

	publicKeys = []
	for i in range(noUsers):
		challengeStr = cryptography.generateRandomString(128)
		newChallengeStr = ChallengeStrings(challengeStr=challengeStr)
		newChallengeStr.save()

		newPublicKey = addUser(userList[i]['username'], userList[i]['department'], userList[i]['name'], userList[i]['course'], passwords[i])

		publicKeys += [newPublicKey]
		user = User.objects.create_user(username = userList[i]['username'], password = passwords[i])
		user.save()

	cryptography.permuteList(publicKeys)
	for i in range(len(publicKeys)):
		newPublicKey = PublicKeys(publicKey=publicKeys[i])
		newPublicKey.save()

	return passwords

def addUser(username, department, name, course, password, voted=False):
	'''Registers new user with the system including signature key generation and registration'''
	#generate private key
	#key = RSA.generate(2048)
	encryptedPrivateKey = cryptography.symmetricEncrypt(key.exportKey(), password)
	p1 = Users(username=username, voted=voted, department=department, name=name, course=course, encryptedPrivateKey=encryptedPrivateKey)
	p1.save()
	return key.publickey().exportKey()

#---------------------------------
def makeCandidate(username, details, photo, approved=False):
	if len(Users.objects.filter(username=username)) == 0:
		 return False
	else:
		assert(len(Users.objects.filter(username=username)) == 1)
		assert(approved == False)
		assert(len(details) != 0)
		p1 = Candidates(username=username, details=details, photo=photo, approved=approved)
		p1.save()
		return True

#---------------------------------
def registerVote(plainText, username, password):
	"""Register plainText as the vote of user with given username and password"""
	userlist = Users.objects.filter(username=username)
	#print len(userlist)
	if (len(userlist) == 0):
		return False
	assert(len(userlist) == 1)
	decryptedPrivateKey = cryptography.symmetricDecrypt(userlist[0].encryptedPrivateKey,password)

	certificate = cryptography.asymmetricSign(plainText,decryptedPrivateKey)
	#key = RSA.importKey(decryptedPrivateKey)
	key = key.publickey().exportKey()
	assert(len(PublicKeys.objects.filter(publicKey=key)) == 1)
	publicKey = PublicKeys.objects.filter(publicKey=key)[0]

	challenobj = ChallengeStrings.objects.all()
	lenofcha = len(challenobj)
	rannum = lenofcha/2
	'''get a random number'''
	p1 = Votes(plainText=plainText, certificate=certificate, publicKey=publicKey, challengeStr = challenobj[rannum])
	p1.save()
	return True

#---------------------------------
def loginUser(username, password):
	if username =='kayush' and password == 'kayush':
		return True
	else:
		return False

#----------------------------------

def getUserDetails(username):
	details = { 'username':'kayush' , 'voted': True, 'Department':'cse', 'name':'Ayush', 'course':'btech','encryptedPrivateKey':'qwertyuiop' }
	return details

#-------------------------------

def validateAllVotes():
	validate = ['True','True' , 'False']
	return validate

#-----------------------

def getElectionStats():
	Stats = {'vote-count':{'candidate1':100, 'candidate2':97},'vote-turnout':0.67, 'vote-demographics':{'btech':0.4,'mtech':0.5, 'dual':0.1}}
	return Stats

#--------------------
# This function gets a stats parameter as returned by getStats()
# Returns a list in the same format as getStats() except that 
# it only contains information about the selected candidates
# and omits the second and third item in the tuples 
# eg: [('Vice President', [('candOne', 400, 'permaLink')]), 
# ('Senator', [('candFive', 500, 'xxx'), ('candSix', 764, 'xxx'), ('candSeven', 200, 'xxx')]),
# ('Technical Secratary', [('CandFour', 500)])]

def getWinner(Stats):
	winnerlist = []
	for post in Stats: 
		postwinners = []	
		postwinners = sorted(post[3], key=lambda x: x[1], reverse=True)
		postwinners = postwinners[:post[1]]		#Create a list with the list of selected candidates for the post
		tup = (post[0], postwinners)	#Create the tuple corresponding to the post
		winnerlist.append(tup)		
	return winnerlist
#-------------------

def approveCandidate(username):
	if username == 'sudhanshu':
		return True
	else:
		return False

#------------------------

def getCandidateDetail(username):
	details = {'username':'sudhanshu', 'post':'vp', 'picture':'sudhanshu.jpg','form-data':{'agenda':'my agenda', 'position-of-responsibility':'Director of IITG' }}
	return details

#----------------------

def setCandidateDetails(username):
	detail = getCandidateDetail(username);
	# converting dict to json
	detail = json.dumps(detail)
	return detail
#----------------------
def getElectionState(state):
	if state == 0:
		var = 'pre-election'
	elif state == 1:
		var = 'during election'
	else:
		var = 'post-election'
	return var
#-----------------------------
def setElectionState(state):
    if state == 0:
        var = 'pre-election'
    elif state == 1:
        var = 'during election'
    else:
        var = 'post-election'
#-------------------------
def getCandidatePost(postId):
	post = {'vp':{'candidate1':'Ayush ', 'Candidate2':'Sudhanshu'}, 'welfare':{'candidate1':'Ayush ', 'Candidate2':'Sudhanshu'}, 'sport':{'candidate1':'Ayush ', 'Candidate2':'Sudhanshu'}}
	return post

#--------------------------
def importElectionData(src):
	stats = {'':''}
	return stats
#------------------------

def getPosts():
	postList = Posts.objects.all()
	postDetailsList = []
	for post in postList :
		print(post.postName)
		#postDetails{'postName':post.postName,'postCount':post.postCount,'voterGender':post.voterGender,'voterCourse':post.voterCourse}
		postDetails = post.postName,post.postCount,post.voterGender,post.voterCourse
		postDetailsList.append(postDetails)
	return postDetailsList

#--------------------------

def addPost(postName,postCount,voterGender,voterCourse):
	p = Posts(postName=postName,voterGender=voterGender,voterCourse=voterCourse)
	p.save()
	return True

#---------------------------

def getCandidatesList():
	candidatesObj = Candidates.objects.all()
	candidatesList = []
	for item in candidatesObj :
		candidateTuple = (item.username,item.details,item.photo,item.approved)
		candidatesList.append(candidateTuple)
		print(candidateTuple)

	return candidatesList

#-----------------------------

#def getEligiblility(post):
	


#def isEligible(candidate,post):

def verifyVote(votes):
	"""Verifies all votes"""
	for vote in votes:
		value = cryptography.asymmetricVerify(vote.plainText, vote.certificate, vote.publicKey.publicKey)
		if value == False:
			print(error)			
	return value

def getVoterDetails(voterName):
	voterObj = Users.objects.get(username=voterName)
	voterDict = {'name':voterObj.username,'gender':voterObj.gender,'course':voterObj.course}
	return voterDict

def getVotablePosts(voterGender,voterCourse):
	postsObj = Posts.objects.filter(Q(eligibleGender=voterGender) | Q(eligibleGender='a'))
	postsObj = postsObj.filter(Q(eligibleCourse=voterCourse) | Q(eligibleCourse='a'))
	postsDictList = []
	for item in postsObj:
		postsDictList.append({'postName':item.postName,'postCount':item.postCount,'voterGender':item.voterGender,'voterCourse':item.voterCourse})
	return postsDictList

def getStats():
	postsObj = Posts.objects.all()	
	for item in postsObj:
		candStatList = []
		candCount = 0
		candObj = Candidates.objects.all()
		candObj = candObj.filter(contestingPost=postsObj.postName,approved=True)
		for cand in candObj:
			temp = (cand.username,cand.noOfVotes,'permaLink')
			candStatList.append(temp)
		tup = (postsObj.postName,postsObj.postCount, candCount ,candStatList)
		candStatList.append(tup)
	return candStatList
