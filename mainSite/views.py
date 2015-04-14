#import field dependencies
from django.shortcuts import render_to_response, render
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext, loader,Template,Context
from .databaseManager import *
from mainSite.models import *
import json
from django.core.context_processors import csrf
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

#import database fields
from mainSite.models import Users, Candidates,Votes, PublicKeys, ChallengeStrings , Posts

# Create your views here.
def resultsView(request):
	indexPage = loader.get_template('index.html')
	
	'''
	stats = [	('vp',1,2,	[ ('candOne',200,'permaLink'),('candTwo',300,'xxx') ]	) ,
				('tech',1,2,[ ('candThree',400,'xxx') , ('candFour',500,'xxx')]),
				('welfare',1,3,[('candFive',500,'xxx') , ('candSix',764,'xxx') , ('candSeven',200,'xxx')])
			]
	'''
	# stats = [	('vp',1,2,	[ ('candOne',200,'permaLink'),('candTwo',300,'xxx') ]	) ,
	# 			('tech',1,2,[ ('candThree',400,'xxx') , ('candFour',500,'xxx')]),
	# 			('welfare',2,3,[('candFive',500,'xxx') , ('candSix',764,'xxx') , ('candSeven',200,'xxx')])
	# 		]

	stats = getStats()
	winnerlist = getWinner(stats)
	NoOfVotes = 1000
	contextObj = Context({'stats':stats,'NoOfVotes':NoOfVotes, 'winnerlist' :winnerlist})

	return render_to_response('results.html',contextObj)
	#return HttpResponse("index.html")
def candidateStat(request,candidateName):
	deptStats = {('cse',35),('ece',56)}
	courseStats = {('ug',55),('pg',26),('phd',33)}
	hostelStats = {('umiam',33),('kameng',55),('barak',24)}
	contextObj =Context({'candidatename':candidateName,'deptStats':deptStats,'courseStats':courseStats,'hostelStats':hostelStats})
	return render_to_response('candidateStats.html',contextObj)

def candidateView(request,candidateName):
	candidateDetails = getCandidateDetail(candidateName)
	contextObj = Context({'candidateName':candidateName,'candidateDetails':candidateDetails})
	return render_to_response('myTest.html',contextObj)

def candidatesListView(request):
	
	candidatesList = getCandidatesList()
	contextObj = Context({'candidatesList':candidatesList})
	return render_to_response('candidates.html',contextObj)



def user_login(request):                      #url for login page is home/login
    if request.method == 'POST':
    	username= request.POST.get('username')
    	password = request.POST.get('password')
    	user = authenticate(username=username,password=password)
    	if user:
    	    if (user.is_active and user.is_staff):
    	        login(request, user)
    	        return HttpResponseRedirect('/gems/admin')
    	    else:
                login(request, user)
                return HttpResponseRedirect('/gems/voterHome')
    	else:
    	    return HttpResponse("your account is diabled")		
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request, 'login.html', {})		
    return render(request, 'index.html', context_dict)

@login_required
def voterHome(request):
	return render(request, 'main_page.html')

def view_candidate(request):
	candidate_i = New_Candidate.objects.all()
	candidate_data = {"candidate_detail" : candidate_i}
	return render_to_response('view_candidates.html', candidate_data, context_instance=RequestContext(request))

def candidateView(request,candidateName):
	b = New_Candidate.objects.get(name=candidateName)
	data = {"detail" : b}
	#candidateDetails = getCandidateDetail(candidateName)
	#contextObj = Context({'candidateName':candidateName,'candidateDetails':candidateDetails})
	return render_to_response('test.html',data,context_instance=RequestContext(request))

def register(request):
	return render(request, 'registration_form.html')

def add_candidate(request):
	if request.GET:
		new_candidate = New_Candidate(name=request.GET['name'],post=request.GET['optionsRadios'],  roll=request.GET['roll'], department=request.GET['dept'], cpi=request.GET['cpi'], sem=request.GET['sem'], backlogs=request.GET['back'], email=request.GET['email'], contact=request.GET['contact'], hostel=request.GET['hostel'], room=request.GET['room'], agenda=request.GET['agenda'])
		new_candidate.save()
	return HttpResponseRedirect('/main')

def voterView(request):
	voterDetail = getVoterDetails('Nik')
	votablePosts = getVotablePosts(voterDetail['gender'],voterDetail['course'])
	contextObj = Context({'votablePosts':votablePosts})
	postdata= []
	for postTemp in votablePosts:
		candidates=Candidates.objects.filter(contestingPost=postTemp['postName'])
		cList = []
		for cand in candidates:
			cList += [cand.username]
		dat = {}
		dat['candidates'] = cList
		dat['post'] = postTemp['postName']
		dat['postcount'] = postTemp['postCount']
		postdata += [dat]
		contextObj = Context({'data':postdata})
	return render_to_response('votingpage.html',contextObj)

def voteRequestView(request):
	voterDetail = getVoterDetails('Nik')
	votablePosts = getVotablePosts(voterDetail['gender',voterDetail['course']])
	jsonDict = {}
	for item in votablePosts:
		candidatesVoted = request.POST.getlist(item.PostName)
		jsonDict[item.PostName] = candidatesVoted
		for candidate in candidatesVoted:
			candObj = Candidates.objects.all()
			candObj = candObj.filter(username=candidate.username)
			candObj.noOfVotes = candObj.noOfVotes + 1
			candObj.save()
	jsonStr = json.dumps(jsonDict)
	registerVote(jsonStr,voterDetail['name'],request.POST.get('alertInput'))
	contextObj = Context()
	return render_to_response('blank-page.html',contextObj)

#To Display the list of selected candidates after the election 
def selectedCandidates(request): 
	stats = getStats()
	# stats = [	('vp',1,2,	[ ('candOne',200,'permaLink'),('candTwo',300,'xxx') ]	) ,
	# 			('tech',1,2,[ ('candThree',400,'xxx') , ('candFour',500,'xxx')]),
	# 			('welfare',2,3,[('candFive',500,'xxx') , ('candSix',764,'xxx') , ('candSeven',200,'xxx')])
	# 		]
	winnerlist = getWinner(stats)	
	#winnerlist = [('Vice President', [('candOne', 400, 'permaLink')]), ('Senator', [('candFive', 500, 'xxx'), ('candSix', 764, 'xxx'), ('candSeven', 200, 'xxx')]), ('Technical Secratary', [('CandFour', 500)])]
	contextObj = Context({'winnerlist' : winnerlist})
	return render_to_response('selected-candidates.html', contextObj)

