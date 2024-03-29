from django.shortcuts import render
from django.conf import settings
import urllib
from src import *

from django.http import HttpResponse
from django.http import HttpResponseRedirect

from django.views.decorators.csrf import csrf_exempt

# -------------------------------------------------------------------------------------------------------------------
def index(request):

    return render(request, 'web/main.html')

#---------------------------------------------------------------------------------------------------------------------
@csrf_exempt
def list_movies(request):
    movies = trending_movies()
    return HttpResponse(json.dumps(movies),content_type='application/json')

#-----------------------------------------------------------------------------------------------------------------
@csrf_exempt
def list_series(request):
    series = trending_series()
    return HttpResponse(json.dumps(series),content_type='application/json')

@csrf_exempt
def detail_movies(request,movie_id):

    data = movie_detail(movie_id)
    return HttpResponse(json.dumps(data),content_type='application/json')

#----------------------------------------------------------------------------------------------------------------------
@csrf_exempt
def detail_series(request, series_id):

    data = series_detail(series_id)
    return HttpResponse(json.dumps(data),content_type='application/json')
    
#-----------------------------------------------------------------------------------------------------------------
def list_episode(request,season_id):

    data = episode_list(season_id)
    return render(request,'web/list_episode.html',data)

#----------------------------------------------------------------------------------------------------------------------
def detail_episode(request,episode_id):
    data = episode_detail(episode_id) 
    return HttpResponse(json.dumps(data),content_type='application/json')

#---------------------------------------------------------------------------------------------------------------------
def availability(request, id):
    data = get_availability(id)
    return HttpResponse(json.dumps(data),content_type='application/json')
