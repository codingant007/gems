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
from mainSite.databaseManager import getWinner, getElectionStats

# Create your views here.
def resultsView(request):
	indexPage = loader.get_template('index.html')
	
	stats = [	('Vice President',1,2,	[ ('candOne',400,'permaLink'),('candTwo',300,'xxx') ]	) ,
				('Senator',3,3,[('candFive',500,'xxx') , ('candSix',764,'xxx') , ('candSeven',200,'xxx')]),
				('Technical Secratary',1,2,[ ('candThree',400,'xxx') , ('candFour',500,'xxx')])
			]
	#winnerlist = getWinner(stats)	
	winnerlist = [('Vice President', [('candOne', 400, 'permaLink')]), ('Senator', [('candFive', 500, 'xxx'), ('candSix', 764, 'xxx'), ('candSeven', 200, 'xxx')]), ('Technical Secratary', [('candFour', 500, 'xxx')])] 	##Comment this line out in the final version
	NoOfVotes = 1000
	contextObj = Context({'stats':stats,'NoOfVotes':NoOfVotes, 'winnerlist':winnerlist})

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
	return render_to_response('blank-page.html',contextObj)


def selectedCandidates(request): 
	stats = getElectionStats()
	#winnerlist = getWinner(stats)	
	winnerlist = [('Vice President', [('candOne', 400, 'permaLink')]), ('Senator', [('candFive', 500, 'xxx'), ('candSix', 764, 'xxx'), ('candSeven', 200, 'xxx')]), ('Technical Secratary', [('CandFour', 500)])]
	contextObj = Context({'winnerlist' : winnerlist})
	return render_to_response('selected-candidates.html', contextObj)