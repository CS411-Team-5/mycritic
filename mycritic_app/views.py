import tmdbsimple as tmdb
import os

from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from mycritic_app.models import *
from mycritic_app.forms import RegistrationForm, LoginForm

tmdb.API_KEY = os.environ['TMDB_KEY']

##########################
# REGISTRATION AND LOGIN #
##########################

def register(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/mycritic_app/logged_in')
    if request.method == 'POST':
        register_form = RegistrationForm(request.POST)
        if register_form.is_valid():
            register_form.save()
            return HttpResponseRedirect('/mycritic_app/register/complete')

    else:
        register_form = RegistrationForm()
    login_form = LoginForm()
    token = {}
    token.update(csrf(request))
    token['register_form'] = register_form
    token['login_form'] = login_form
    token['login'] = False

    return render_to_response('registration/login.html', token)

def registration_complete(request):
    
    return render_to_response('registration/registration_complete.html')

def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/mycritic_app/logged_in')
    message = ""
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    auth.login(request, user)
                    return HttpResponseRedirect('/mycritic_app/logged_in')
                else:
                    message = "Your account is inactive"
            else:
                message = "Invalid username and/or password, please reenter"
    else:
        login_form = LoginForm()
    register_form = RegistrationForm()
    return render(request, 'registration/login.html', {'message': message, 'login_form': login_form, 'register_form': register_form, 'login': True})
    
def logged_in(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    if profile.movies_rated < 5:
        return HttpResponseRedirect('/mycritic_app/search')
    return render_to_response('registration/logged_in.html',
                              {'username': request.user.username})

def login_error(request):
    return render_to_response('registration/login_error.html')

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/mycritic_app/login')


######################
# SEARCH AND RESULTS #
######################

def fetch_tmdb(string):
    results = []
    search = tmdb.Search()
    search.movie(query=string)
    response = []
    clean_response = []
    for result in search.results:
        response += [result]
        if result['poster_path'] is not None:
            clean_response += [[result['id'],
                                result['title'],
                                "http://image.tmdb.org/t/p/w342" + result['poster_path'],
                                result['overview']]]
        else:
            clean_response += [[result['id'],
                                result['title'],
                                "http://i.imgur.com/fVlnrIS.jpg",
                                result['overview']]]
    return (response, clean_response)

@login_required(login_url='/mycritic_app/login/')
def search(request):
    """
    View function for search page of site.
    """
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    need_to_rate = False
    username = request.user.username
    rated = profile.movies_rated
    if rated < 5:
        need_to_rate = True
    # Render the HTML template search.html with the data in the context variable
    return render(
        request,
        'base.html',
        context={'username': username, 'need_to_rate': need_to_rate, 'movies_to_rate': (5 - rated)},
    )

@login_required(login_url='/mycritic_app/login/')
def result(request):
    """
    View function for search result page of site.
    """
    query = request.GET.urlencode('search')[2:]
    query = query.replace("%20", " ")
    # If the query is in the database
    if SearchCache.objects.filter(search_query=query).exists():   #####
        obj = SearchCache.objects.get(search_query=query)         #####
        response = eval(obj.value)
        return render(
            request,
            'result.html',
            context={'query': query, 'response':response, 'clean_response':response, 'verbose':'', 'source':'Local Database'},
        )
    else:

        # Otherwise fetch it from TMDB
        tup = fetch_tmdb(query)
        response = tup[0]
        clean_response = tup[1]
        verbose = ""
        for movie in clean_response:
            verbose += str(movie) + "\n\n"

        # Put the search response into our local database
        obj = SearchCache.objects.create(search_query=query, value=str(clean_response)) #####
        
        # Render the HTML template search.html with the data in the context variable
        return render(
            request,
            'result.html',
            context={'query': query, 'response':response, 'clean_response':clean_response, 'verbose':verbose, 'source':'TMDB'},
        )
