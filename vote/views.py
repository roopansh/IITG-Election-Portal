from django.shortcuts import render, redirect
from .models import Voter, Admin, Contestant
from django.urls import reverse 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
import random
from datetime import datetime, timedelta
import time
from django.conf import settings
from django.utils.datastructures import MultiValueDictKeyError
from django import http


errorMessage = ""


CATEGORY1 = {
        'VP': 'Vice President',
        'HAB': 'Hostel Affairs Board Seceratary',
        'UGS': 'Under Graduate Senate',
        'PGS':'Post Graduate Senate ',
        'GS':'Girl Senate',
        'Tech':'Technical Seceratary',
        'Cult':'Cultural Seceratary',
        'Welfare':'Welfare Seceratary',
        'Sports':'Sports Seceratary',
        'SAIL':'General Seceratry of SAIL',
        'CBS':'General Seceratry of CBS'
}

bread = {
        'VP': 2,
        'HAB': 5,
        'UGS': 1,
        'PGS':1,
        'GS':1,
        'Tech':3,
        'Cult':4,
        'Welfare':6,
        'Sports':7,
        'SAIL':8,
        'CBS':9,
}

# home page
def index(request):
    if request.user.is_authenticated() and Voter.objects.filter(username = request.user.username).exists():
        return render(request, 'vote/home.html', {'Voter_continue':False})
    else :
        return render(request, 'vote/home.html')

# admin login portal
def admin(request):
    if request.user.is_authenticated() and Admin.objects.filter(user = request.user).exists():
        return render(request, 'vote/key.html')
    else:
        return render(request, 'vote/admin.html')


# admin validate login
def adminLogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password'] 
        user = authenticate(username=username, password=password)
        if user is not None:
            if Admin.objects.filter(user=user).exists():
                login(request, user)
                return render(request, 'vote/key.html')
            else:
                    return render(request, 'vote/admin.html', { 'error_message' : "You are not authorised."})
        else:
            return render(request, 'vote/admin.html', { 'error_message' : "Wrong username/password combination"})
    elif request.user.is_authenticated() and Admin.objects.filter(user = request.user).exists():
        return render(request, 'vote/key.html')
    else:
        return render(request, 'vote/admin.html')  


# Key gen
def key(request):
    if request.method == 'POST':
        username = request.POST['webmail']
        if Voter.objects.filter(username=username).exists() :
            chars = "abcdefghjkmnpqrstuvwxyABCDEFGHJKLMNPQRSTUVWXY3456789"
            password = "".join(random.choice(chars) for _ in range(8))
            if User.objects.filter(username=username).exists():
                user = User.objects.get(username=username)
            else:
                user = User.objects.create_user(username)
            user.set_password(password)
            user.save()
            return render(request, 'vote/key.html', { 'error_message' : "Password for " + username + " username is : " + password + ""})
        else:
            return render(request, 'vote/key.html', { 'error_message' : "Incorrect webmail"})
    elif request.user.is_authenticated() and Admin.objects.filter(user = request.user).exists():
        return render(request, 'vote/key.html')
    else:
        return render(request, 'vote/admin.html')


def voter(request):
    # print(request)
    if request.method == 'POST':
        if not request.user.is_authenticated(): 
            username = request.POST['webmail']
            password = request.POST['password'] 
            user = authenticate(username=username, password=password)
        else:
            user =  request.user
            username = user.username
        if user is not None:
            if Voter.objects.filter(username = username).exists():
                contestlist = Contestant.objects.all()
                voter = Voter.objects.get(username = username)
                if voter.login_time and not settings.DEBUG:
                    return render(request, 'vote/message.html' , {'message' : "You have already voted! DON'T COME AGAIN !!"})
                login(request, user)
                time = 300
                request.session.set_expiry(time)
                voter.login_time = datetime.now()
                voter.logout_time = datetime.now() + timedelta(seconds=time)
                voter.save()
                # UG-Boy
                if (voter.category == '0' and not voter.bsen_status):
                    post = 'UGS'
                    ContestantsList = Contestant.objects.filter(post = post).order_by('?')
                    return render(request, 'vote/svote.html', {'heading':CATEGORY1[post] ,'post':post,'breadcrumb':1, 'ContestantsList' : ContestantsList, 'session_timer': get_expiry_age(voter.logout_time), 'error_message' : 'You can vote for atmost 7 senators'})
                # PG-Boy
                elif (voter.category == '2' and not voter.bsen_status):
                    post = 'PGS'
                    ContestantsList = Contestant.objects.filter(post = post).order_by('?')
                    return render(request, 'vote/svote.html', {'heading':CATEGORY1[post] ,'post':post,'breadcrumb':1, 'ContestantsList' : ContestantsList, 'session_timer': get_expiry_age(voter.logout_time)})
                # UG-Girl / PG-Girl
                elif (voter.category == '1' or voter.category == '3') and not voter.gsen_status:
                    post = 'GS'
                    ContestantsList = Contestant.objects.filter(post = post).order_by('?')
                    return render(request, 'vote/svote.html', {'heading':CATEGORY1[post] ,'post':post,'breadcrumb':1, 'ContestantsList' : ContestantsList, 'session_timer': get_expiry_age(voter.logout_time)}) ######################insert here
                else :
                    logout(request)
                    return render(request, 'vote/message.html' , {'message' : "You have already voted! DON'T COME AGAIN !!"})
            else :
                return render(request, 'vote/message.html' , {'message' :"YOU ARE NOT AUTHORISED TO VOTE."})
        else:
            return render(request, 'vote/home.html', {'error_message' : 'Incorrect Webmail/Key Combination!'})
    elif request.user.is_authenticated() and Voter.objects.filter(username = request.user.username).exists():
        return render(request, 'vote/home.html', {'Voter_continue':False})
    else :
        return render(request, 'vote/home.html')

# for calculating votes of all senates
def voter_senate(request, post):
    if request.method == 'POST': 
        #add votes and send to the next render fucntion
        # flag = False
        if request.user.is_authenticated():
            username = request.user.username
            voter = Voter.objects.get(username=username)
        else:
            return render(request, 'vote/message.html' , {'message' :"Your time has finished, votes up till then were taken, see you next year!"})

        username = request.user.username
        voter = Voter.objects.get(username=username)
        contestant = request.POST.getlist(post)
        count = len(contestant)

        for c in contestant:
            user = User.objects.get(username = c)
            # print(user.username[0:4])
            if user.username[0:4] == 'NOTA' and count > 1:
                ContestantsList = Contestant.objects.filter(post = post).order_by('?')
                return render(request, 'vote/svote.html', {'heading':CATEGORY1[post] ,'post':post,'breadcrumb':1, 'ContestantsList' : ContestantsList, 'session_timer': get_expiry_age(voter.logout_time), 'error_message':'Can\'t Select NOTA with other contestants!'})


        if count == 0 :             
            error_message = 'Select atleast one contestant!'
        elif post == 'GS' and count > 3:
            error_message = 'You can select maximum of 3 contestants!'
        elif count > 7:
            error_message = 'You can select maximum of 7 contestants!'
        else:
            error_message = ''

        if not error_message == "" and not voter.bsen_status:
            ContestantsList = Contestant.objects.filter(post = post).order_by('?')
            return render(request, 'vote/svote.html', {'heading':CATEGORY1[post] ,'post':post,'breadcrumb':1, 'ContestantsList' : ContestantsList, 'session_timer': get_expiry_age(voter.logout_time), 'error_message':error_message})

        # PG-Boy
        if voter.bsen_status:
            if not voter.vp_status:
                next_post = 'VP'
            # coming from Tech
            elif not voter.tech_status:
                next_post = 'Tech'
            # coming from Cult
            elif not voter.cult_status:
                next_post = 'Cult'
            # coming from HAB
            elif not voter.hostel_status:
                next_post = 'HAB'
            # coming from Welfare
            elif not voter.welf_status:
                next_post = 'Welfare'
            # coming from Sports
            elif not voter.sports_status:
                next_post = 'Sports'
            elif not voter.sail_status:
                next_post = 'SAIL'
            elif not voter.cbs_status:
                next_post = 'CBS'
            else:
                logout(request)
                return render(request, 'vote/message.html' , {'message' :"Vote Given to everyone"})
            post = next_post
            ContestantsList = Contestant.objects.filter(post = post).order_by('?')
            return render(request, 'vote/normvote.html', {'heading':CATEGORY1[post] ,'post':post,'breadcrumb':bread[post], 'ContestantsList' : ContestantsList, 'session_timer': get_expiry_age(voter.logout_time), 'error_message':'You had already voted for that post.'})
        # UG-Girl / PG-Girl
        elif (voter.category == '1' or voter.category == '3') and post=="GS" and voter.gsen_status:
            if voter.category == '1' :
                post = 'UGS'
            else:
                post = 'PGS'
            ContestantsList = Contestant.objects.filter(post = post).order_by('?')
            return render(request, 'vote/svote.html', {'heading':CATEGORY1[post] ,'post':post,'breadcrumb':1, 'ContestantsList' : ContestantsList, 'session_timer': get_expiry_age(voter.logout_time), 'error_message':'You had already voted for that post.'})
        for c in contestant:
            user = User.objects.get(username = c)
            c = Contestant.objects.get(user = user)
            c.vote_count = c.vote_count + 1
            c.save()
            # flag = True


        if post == 'GS':
            voter.gsen_status = True
            voter.save()
            # UG
            if voter.category == "1" and not voter.bsen_status:
                post = 'UGS'
                ContestantsList = Contestant.objects.filter(post = post).order_by('?')
                return render(request, 'vote/svote.html', {'heading':CATEGORY1[post] ,'post':post,'breadcrumb':1, 'ContestantsList' : ContestantsList, 'session_timer': get_expiry_age(voter.logout_time)})
            # PG
            elif voter.category == "3" and not voter.bsen_status :
                post = 'PGS'
                ContestantsList = Contestant.objects.filter(post = post).order_by('?')
                return render(request, 'vote/svote.html', {'heading':CATEGORY1[post] ,'post':post,'breadcrumb':1, 'ContestantsList' : ContestantsList, 'session_timer': get_expiry_age(voter.logout_time)})
        elif post == 'UGS' or post == 'PGS':
            voter.gsen_status = True
            voter.bsen_status = True
            voter.save()
            post = 'VP'
            ContestantsList = Contestant.objects.filter(post = post).order_by('?')
            return render(request, 'vote/normvote.html',{'heading':CATEGORY1[post] ,'post':post,'breadcrumb':2, 'ContestantsList':ContestantsList, 'session_timer': get_expiry_age(voter.logout_time)})
    elif request.user.is_authenticated() and Voter.objects.filter(username = request.user.username).exists():
        return render(request, 'vote/home.html', {'Voter_continue':False})
    else:
        return render(request, 'vote/home.html')


# for calculating votes of all senates
def voter_normal(request, post):
    if request.method == 'POST':
        if request.user.is_authenticated():
            username = request.user.username
            voter = Voter.objects.get(username=username)
        else:
            return render(request, 'vote/message.html' , {'message' :"Your time has finished, votes up till then were taken, see you next year!"})
        error_message = ""
        errorMessage = "You have already voted for that post"

        
        if not voter.vp_status:
            if post == 'VP':
                errorMessage = ""
            next_post = 'VP'
        # coming from Tech
        elif not voter.tech_status:
            if post == 'Tech':
                errorMessage = ""
            next_post = 'Tech'
        # coming from Cult
        elif not voter.cult_status:
            if post == 'Cult':
                errorMessage = ""
            next_post = 'Cult'
        # coming from HAB
        elif not voter.hostel_status:
            if post == 'HAB':
                errorMessage = ""
            next_post = 'HAB'
        # coming from Welfare
        elif not voter.welf_status:
            if post == 'Welfare':
                errorMessage = ""
            next_post = 'Welfare'
        # coming from Sports
        elif not voter.sports_status:
            if post == 'Sports':
                errorMessage = ""
            next_post = 'Sports'
        elif not voter.sail_status:
            if post == 'SAIL':
                errorMessage = ""
            next_post = 'SAIL'
        elif not voter.cbs_status:
            if post == 'CBS':
                errorMessage = ""
            next_post = 'CBS'
        else:
            logout(request)
            return render(request, 'vote/message.html' , {'message' :"Vote Given to everyone"})

        if errorMessage == "":
            #add votes and send to the next render fucntion
            try:
                contestantname = request.POST[post]
            except MultiValueDictKeyError:
                ContestantsList = Contestant.objects.filter(post = post).order_by('?')
                return render(request, 'vote/normvote.html', {'heading':CATEGORY1[post] ,'post':post,'breadcrumb':bread[post], 'ContestantsList' : ContestantsList, 'session_timer': get_expiry_age(voter.logout_time), 'error_message':'Select an option.'})
            user = User.objects.get(username = contestantname)
            contestant = Contestant.objects.get(user = user)
            contestant.vote_count = contestant.vote_count  + 1
            contestant.save()
            # coming from vp
            if not voter.vp_status:
                voter.vp_status = True
                post = 'Tech'
            # coming from Tech
            elif not voter.tech_status:
                voter.tech_status = True
                post = 'Cult'
           # coming from Cult
            elif not voter.cult_status:
                voter.cult_status = True
                post = 'HAB'
           # coming from HAB
            elif not voter.hostel_status:
                voter.hostel_status = True
                post = 'Welfare'
            # coming from Welfare
            elif not voter.welf_status:
                voter.welf_status = True
                post = 'Sports'
            # coming from Sports
            elif not voter.sports_status:
                voter.sports_status = True
                post = 'SAIL'
            elif not voter.sail_status:
                voter.sail_status = True
                post = 'CBS'
            elif not voter.cbs_status:
                voter.cbs_status = True
                voter.save()
                logout(request)
                return render(request, 'vote/message.html' , {'message' :"Vote Given to everyone"})
            voter.save()
        else:
            error_message = errorMessage
            post = next_post

        ContestantsList = Contestant.objects.filter(post = post).order_by('?')
        return render(request, 'vote/normvote.html', {'heading':CATEGORY1[post] ,'post':post,'breadcrumb':bread[post], 'ContestantsList' : ContestantsList, 'session_timer': get_expiry_age(voter.logout_time), 'error_message':error_message})

    elif request.user.is_authenticated() and Voter.objects.filter(username = request.user.username).exists():
        return render(request, 'vote/home.html', {'Voter_continue':False})
    else:
        return render(request, 'vote/home.html')


def logout_user(request):
    logout(request)
    return render(request, 'vote/home.html')


def get_expiry_age(logout_time):
    # print (logout_time,datetime.now())
    return int((logout_time - datetime.now()).total_seconds())