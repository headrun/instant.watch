from django.shortcuts import render
from django.conf import settings
import urllib
from src import *

# -------------------------------------------------------------------------------------------------------------------
def index(request):

#   code for series
    series = trending_series()

# code for movies
    movies = trending_movies()

    context = {"serieses": series,"movieses":movies}
    return render(request, 'web/index.html',context)

# ----------------------------------------------------------------------------------------------------------------------
def detail_movies(request,movie_id):

    data = movie_detail(movie_id)
    #return HttpResponse(json.dumps(data),content_type='application/json')
    return render(request,'web/movie_detail.html',data)

#----------------------------------------------------------------------------------------------------------------------

def detail_series(request, series_id):

    data = series_detail(series_id)
    #return HttpResponse(json.dumps(data),content_type='application/json')
    return render(request,'web/series_detail.html',data)

#-----------------------------------------------------------------------------------------------------------------
def list_episode(request,season_id):

    data = episode_list(season_id)
    return render(request,'web/list_episode.html',data)

#----------------------------------------------------------------------------------------------------------------------
def detail_episode(request,episode_id):

    data = episode_detail(episode_id) 
    return render(request,'web/ep_details.html',data)
