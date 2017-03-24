from django.conf.urls import url
from . import views

app_name='vote'

urlpatterns = [
    # home
    url(r'^$', views.index, name='index'),

    # admin login portal
    url(r'^admin/$', views.admin, name='admin'),
    
    # validating admin login
    url(r'^adminLogin/$', views.adminLogin, name='adminLogin'),
    
    # admin for generating security key
    url(r'^key/$', views.key, name='key'),

    # logout user 
    url(r'^logout/$', views.logout_user, name='logout'),
    
    # voter login
    url(r'^voter/$', views.voter, name='voter'),

    # votes calculator for senates
    url(r'^voter_senate/(?P<post>\w+)/$', views.voter_senate, name='voter_senate'),

    # votes calculator for Other posts
    url(r'^voter_normal/(?P<post>\w+)/$', views.voter_normal, name='voter_normal'),   
]
