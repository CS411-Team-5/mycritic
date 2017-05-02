import tmdbsimple as tmdb
import os

from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from mycritic_app.models import *
from mycritic.settings import *
from mycritic_app.forms import *

tmdb.API_KEY = os.environ['TMDB_KEY']

##########################
# REGISTRATION AND LOGIN #
##########################

def register(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/mycritic_app')
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
        return HttpResponseRedirect('/mycritic_app')
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
                    return HttpResponseRedirect('/mycritic_app')
                else:
                    message = "Your account is inactive"
            else:
                message = "Invalid username and/or password, please reenter"
    else:
        login_form = LoginForm()
    register_form = RegistrationForm()
    return render(request, 'registration/login.html', {'message': message, 'login_form': login_form, 'register_form': register_form, 'login': True})

@login_required(login_url='/mycritic_app/login/')
def logged_in(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    if profile.movies_rated < 5:
        return HttpResponseRedirect('/mycritic_app/search')
    if request.method == "POST":
        rating = Rating.objects.create_rating(request.POST['user_id'], request.POST['movie_id'], request.POST['rating'], request.user)
        return HttpResponseRedirect('/mycritic_app')
    # Below is the code to re-evaluate the user similarity scores for this user.
    username = request.user.username
    user_scores = {}
    movies_rated = Rating.objects.filter(user_id=username)
    ratings = [(r.movie_id, r.rating) for r in movies_rated]
    if len(ratings) != 0:
        for tup in ratings:
            other_users_ratings = Rating.objects.filter(movie_id=int(tup[0])).exclude(user_id=username)
            for other_user in other_users_ratings:
                diff = abs(tup[1] - other_user.rating)
                if diff <= 2.5: # Users are in agreement
                    diff = 2.5 - diff
                else: # Users are in disagreement
                    diff = -(diff - 2.5)

                # Save the resulting 'score' in the user_scores
                if other_user.user_id not in user_scores:
                    user_scores[other_user.user_id] = (diff, 1)
                else:
                    orig = user_scores[other_user.user_id][0]
                    count = user_scores[other_user.user_id][1]
                    user_scores[other_user.user_id] = (orig + diff, count + 1)
                print("Updated against user: " + other_user.user_id)
    profile = UserProfile.objects.filter(user=request.user).update(similarity_scores=str(user_scores))

    # Now actually get the info for similar movies
    already_rated = []
    user_movies = []
    profile = UserProfile.objects.get(user=request.user)
    sim_scores = eval(profile.similarity_scores)

    for other_user in sim_scores:
        if sim_scores[other_user][0] / sim_scores[other_user][1] >= 1.0:
            other_rated = Rating.objects.filter(user_id=other_user).exclude(user_id=username)
            other_ratings = [(r.movie_id, r.rating) for r in other_rated]
            for rating in other_ratings:
                dupe = False
                for user_rating in ratings:
                    if rating[0] == user_rating[0]:
                        dupe = True
                        break
                if rating[0] not in already_rated and rating[1] >= 4.0 and dupe == False:
                    already_rated += [rating[0]]
                    movie = Movie.objects.get(identifier=int(rating[0]))
                    user_movies += [[movie.identifier,
                                     movie.title,
                                     movie.poster,
                                     movie.description,
                                     movie.genre_list]]
    
    return render(request,
                  'home.html',
                  context={'username': request.user.username, 'user_movies': user_movies})

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
                                result['overview'],
                                result['genre_ids']]]
        else:
            clean_response += [[result['id'],
                                result['title'],
                                "http://i.imgur.com/fVlnrIS.jpg",
                                result['overview'],
                                result['genre_ids']]]
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
        'search.html',
        context={'user': request.user.id, 'username': username, 'need_to_rate': need_to_rate, 'movies_to_rate': (5 - rated)},
    )

@login_required(login_url='/mycritic_app/login/')
def result(request):
    """
    View function for search result page of site.
    """
    
    if request.method == "POST":
        rating = Rating.objects.create_rating(request.POST['user_id'], request.POST['movie_id'], request.POST['rating'], request.user)
        return HttpResponseRedirect('/mycritic_app')
    else:
        username = request.user.username
        query = request.GET.urlencode('search')[2:]
        query = query.replace("%20", " ")
        # If the query is in the database
        if SearchCache.objects.filter(search_query=query).exists():   #####
            obj = SearchCache.objects.get(search_query=query)         #####
            response = eval(obj.value)
            return render(
                request,
                'result.html',
                context={'username': username, 'query': query, 'response':response, 'clean_response':response, 'verbose':'', 'source':'Local Database'},
            )
        else:

            # Otherwise fetch it from TMDB
            tup = fetch_tmdb(query)
            response = tup[0]
            clean_response = tup[1]
            #print(response)
            verbose = ""
            for movie in clean_response:
                verbose += str(movie) + "\n\n"
                db_movie = Movie.objects.create_movie(movie[0], movie[1], movie[2], movie[3], movie[4])

            # Put the search response into our local database
            obj = SearchCache.objects.create(search_query=query, value=str(clean_response)) #####
            
            # Render the HTML template search.html with the data in the context variable
            return render(
                request,
                'result.html',
                context={'username': username, 'query': query, 'response':response, 'clean_response':clean_response, 'verbose':verbose, 'source':'TMDB'},
            )

###########
# TWITTER #
###########

def begin_auth(request):
    """The view function that initiates the entire handshake.
    For the most part, this is 100% drag and drop.
    """
    # Instantiate Twython with the first leg of our trip.
    twitter = Twython(settings.SOCIAL_AUTH_TWITTER_KEY, settings.SOCIAL_AUTH_TWITTER_SECRET)

    # Request an authorization url to send the user to...
    callback_url = request.build_absolute_uri(reverse('twython_django_oauth.views.thanks'))
    auth_props = twitter.get_authentication_tokens(callback_url)

    request.session['request_token'] = auth_props

    request.session['next_url'] = request.GET.get('next',None)

    return HttpResponseRedirect(auth_props['auth_url'])


def thanks(request, redirect_url=SOCIAL_AUTH_LOGOUT_REDIRECT_URL):
    """A user gets redirected here after hitting Twitter and authorizing your app to use their data.
    This is the view that stores the tokens you want
    for querying data. Pay attention to this.
    """
    # Now that we've got the magic tokens back from Twitter, we need to exchange
    # for permanent ones and store them...
    oauth_token = request.session['request_token']['oauth_token']
    oauth_token_secret = request.session['request_token']['oauth_token_secret']
    twitter = Twython(settings.SOCIAL_AUTH_TWITTER_KEY, settings.SOCIAL_AUTH_TWITTER_SECRET, oauth_token, oauth_token_secret)

    # Retrieve the tokens we want...
    authorized_tokens = twitter.get_authorized_tokens(request.GET['oauth_verifier'])

    # If they already exist, grab them, login and redirect to a page displaying stuff.
    try:
        user = User.objects.get(username=authorized_tokens['screen_name'])
    except User.DoesNotExist:
        # We mock a creation here; no email, password is just the token, etc.
        user = User.objects.create_user(authorized_tokens['screen_name'], "notreal@email.com", authorized_tokens['oauth_token_secret'])
        profile = UserProfile()
        profile.user = user
        profile.oauth_token = authorized_tokens['oauth_token']
        profile.oauth_secret = authorized_tokens['oauth_token_secret']
        profile.save()

        user = authenticate(
                            username=authorized_tokens['screen_name'],
                            password=authorized_tokens['oauth_token_secret']
                            )
        login(request, user)
        redirect_url = request.session.get('next_url', redirect_url)

        HttpResponseRedirect(redirect_url)
