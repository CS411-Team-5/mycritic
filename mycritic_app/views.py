import tmdbsimple as tmdb
import os
tmdb.API_KEY = os.environ['TMDB_KEY']

from django.shortcuts import render
from django.http import HttpResponse
from mycritic_app.models import SearchCache   #####


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

def search(request):
    """
    View function for search page of site.
    """    
    # Render the HTML template search.html with the data in the context variable
    return render(
        request,
        'search.html',
        context={},
    )

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

