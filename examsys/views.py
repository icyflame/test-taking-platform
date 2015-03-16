from django.shortcuts import render

import hashlib

# def index(request):
#     return HttpResponse("Hello, world. You're at the polls index.")

# Create your views here.

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render

from examsys.models import *

def index(request):
	loggedin = False
	name = ""
	p = ""

	try:
		loggedin = request.session['loggedin']
	except KeyError:
		request.session['loggedin'] = False

	if loggedin:

		p = User.objects.filter(id=request.session['userid'])[0]
		name = p.name

	template = loader.get_template('index.html')
	context = RequestContext(request, {
		'loggedin' : loggedin,
		'name' : name,
		'p' : p
		})
	return HttpResponse(template.render(context))

def login(request):

	username = request.POST['username']
	password = request.POST['password']

	users = User.objects.filter(username=username)

	if len(users) > 0:

		if users[0].password == password:

			request.session["loggedin"] = True
			request.session["userid"] = users[0].id

			# redirect('views.index')

			# return HttpResponseRedirect("examsys/")

			return HttpResponse("Validated properly!" + str(request.session))

		else:

			return HttpResponse("Invalid password!")

	else:

		return HttpResponse("The user does not exist!")

	# print username, password

	return HttpResponse("hey " + str(username) + " with password " + str(password) + " num " + str(len(users)))

def logout(request):

	request.session["loggedin"] = False
	request.session["userid"] = 0

	return HttpResponse("You have been successfully logged out.")

def register(request):

	if request.method == "POST":

		name = request.POST['uname']
		username = request.POST['username']
		password = request.POST['password']

		users = User.objects.filter(username=username)

		if len(users) > 0:

			return HttpResponse("Username exists! Register with a different username!")

		else:

			u = User(name=name, username=username, password=password)
			u.save()

			return HttpResponse("Registered!")

	elif request.method == "GET":

		return render(request, 'register.html')

	else:

		return HttpResponse("You must have pressed register! :P")

def loggedin(request):

	return request.session['loggedin']

def choosetest(request):

	if not loggedin(request):

		return HttpResponse("You must log in to see this page.")

	t = Test.objects.all()

	return render(request, 'choosetest.html', {'alltests' : t})

def taketest(request, test_id):

	if not loggedin(request):

		return HttpResponse("You must log in to see this page.")

	# find all the questions in this test

	t = Test.objects.filter(id=test_id)[0]

	tq = TestToQuestion.objects.filter(tid_id=test_id)

	all_q = []

	for i in tq:

		q1 = Question.objects.filter(id=i.qid_id)
		all_q.append(q1[0])

	return render(request, 'test.html', {'t' : t, 'allq' : all_q})

	# return HttpResponse("So, you wanna take a test?" + str(test_id))

def submit(request):

	if not request.method == "POST":

		return HttpResponse("Only POST requests will be accepted!")

	marks = 0
	total = 0
	correctques = []
	wrongques = []

	for i in request.POST.keys():

		if i[0] == 'c':

			continue

		answer = request.POST[i].lower()
		
		qid = int(i)

		correctanswer = Question.objects.filter(id=qid)[0].correctans.lower()

		submitted = hashlib.sha224(answer).hexdigest()

		calculated = hashlib.sha224(correctanswer).hexdigest()

		if calculated == submitted:

			marks += 1 # add the question value
			total += 1
			correctques.append(Question.objects.filter(id=qid)[0])

		else:

			# deduct the question value (negative marking, if any)
			total += 1 # add the question value
			wrongques.append(Question.objects.filter(id=qid)[0])

	return render(request, 'results.html', {
		'correctques' : correctques,
		'wrongques' : wrongques,
		'marks_obtained' : marks,
		'total_marks' : total,
		'num_correct' : len(correctques),
		'num_wrong' : len(wrongques),
		})
