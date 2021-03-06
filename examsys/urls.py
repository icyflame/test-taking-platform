from django.conf.urls import patterns, url

from examsys import views

urlpatterns = patterns('',
		# (r'^$', lambda r: HttpResponseRedirect('examsys/'))
    url(r'^$', views.index, name='index'),
    url(r'^login/', views.login, name='login'),
    url(r'^logout/', views.logout, name='logout'),
    url(r'^register/', views.register, name='register'),
    url(r'^choosetest/', views.choosetest, name='choosetest'),
    url(r'^(?P<test_id>\d+)/$', views.taketest, name='taketest'),
    url(r'^submit/', views.submit, name='submit'),
    
)
