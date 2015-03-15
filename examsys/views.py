from django.shortcuts import render

# def index(request):
#     return HttpResponse("Hello, world. You're at the polls index.")

# Create your views here.

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext, loader
from examsys.models import *

def index(request):
	loggedin = False
	try:
		loggedin = request.session['loggedin']
	except KeyError:
		request.session['loggedin'] = False

	template = loader.get_template('index.html')
	context = RequestContext(request, {
		'loggedin' : loggedin,
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

	return HttpResponse("You must have pressed register! :P")
