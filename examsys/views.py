from django.shortcuts import render

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

	# find all the questions in this test

	t = Test.objects.filter(id=test_id)[0]

	return render(request, 'test.html', {'t' : t})

	# return HttpResponse("So, you wanna take a test?" + str(test_id))
