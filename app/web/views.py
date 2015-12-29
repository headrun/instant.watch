from django.shortcuts import render
from django.conf import settings
import urllib
from src import *

<<<<<<< HEAD
from tornado.auth import _oauth10a_signature
from urllib import urlencode
from urlparse import parse_qsl

from django.http import HttpResponse
from django.http import HttpResponseRedirect

import pdb
from django.views.decorators.csrf import csrf_exempt

CONSUMER_TOKEN  = {"key": "686fa81bea30c4af40903fffca654b6958d29ba0614e90728cd03623c2cc5d29",\
                   "secret": "a52c32c1af43b321c4a08a265ff996dfd28b2eea72fbaa500fa68129e1792ad4"}

# TMPLS = json.loads(open("templates.json").read())

def get_unique_str():

  date = str(datetime.datetime.now())

  return md5.md5(date).hexdigest()

def oauth_request_parameters(url, consumer_token, parameters={},
                              method="GET"):
    """Returns the OAuth parameters as a dict for the given request.
    parameters should include all POST arguments and query string arguments
    that will be sent with the request.
    """
    base_args = dict(
        oauth_consumer_key=consumer_token["key"],
        oauth_signature_method="HMAC-SHA1",
        oauth_timestamp=str(int(time.time())),
        oauth_nonce=get_unique_str(),
        oauth_version="1.0a",
    )
    args = {}
    args.update(base_args)
    args.update(parameters)
    signature = _oauth10a_signature(consumer_token, method, url, args)
    base_args["oauth_signature"] = signature

    return base_args

=======
# -------------------------------------------------------------------------------------------------------------------
>>>>>>> d57a3be53d0c0fbadf2f0d441c6ac1a16d31d99d
def index(request):

#   code for series
<<<<<<< HEAD
    url ="https://private-anon-defbcd4c1-rovicloudapi.apiary-proxy.com/api/v1/resolve/2/discover_all_trending_video/series"


    extraArguments = oauth_request_parameters(url,
                             CONSUMER_TOKEN,
                             params)

    params.update(extraArguments)
    params = urlencode(params)

    resp = requests.get("%s?%s" % (url,params), verify=False)

    resp = resp.json()
    series = []
    for element in resp['items']:
        try:            
            dict1 = {'name':element['name'],'id':element['ref']['id'],'year':element['year']}
            series.append(dict1)
        except:
            pass


# code for movies
    url ="https://private-anon-defbcd4c1-rovicloudapi.apiary-proxy.com/api/v1/resolve/2/discover_all_trending_video/movies"
    resp = requests.get("%s?%s" % (url, params), verify=False)
    resp = resp.json()
    movies = []
    for element in resp['items']:
        try:
            dict1 = {'name':element['name'],'id':element['ref']['id'],'year':element['year']}
            movies.append(dict1)
        except:
            pass
# code for image
    url = "https://private-anon-defbcd4c1-rovicloudapi.apiary-proxy.com/api/v1/resolve/2/media_image/sized?id=172343929&aspect=3x4&size=large&zoom=std"
    image = requests.get("%s?%s" % (url, params ), verify=False)
    
    
    context = {"serieses": series,"movieses":movies,"image": 'image'}
    return render(request, 'web/main.html',context)

=======
    series = trending_series()

# code for movies
    movies = trending_movies()
>>>>>>> d57a3be53d0c0fbadf2f0d441c6ac1a16d31d99d

    context = {"serieses": series,"movieses":movies}
    return render(request, 'web/index.html',context)

<<<<<<< HEAD
@csrf_exempt
def detail_movies(request):
    movie_id = request.POST.get('send_data')
    service_id =str(1063353154)
    year1 =datetime.datetime.now().year
    params = {'serviceId': service_id, 'by': -year1}

# code for information about movie
 
    url = "https://private-anon-defbcd4c1-rovicloudapi.apiary-proxy.com/api/v1/resolve/2/data_movie?id="+movie_id+"&in=en-US&in2=en-*&in3=*"
    data_about_movie = requests.get("%s?%s" % (url, params ), verify=False)
    url = url.replace(" ", "")
    data_about_movie = data_about_movie.json()
    genres = data_about_movie['genres']
    name = data_about_movie['title']
    year_of_release = data_about_movie['year']
    language = data_about_movie['spoken']
    fan_rating = data_about_movie['rottenTomatoes']['fan']['score']
    try:
        facebook = data_about_movie['facebooks'][0]['uri']
    except:
        facebook = "Not Available"
    try:
        keywords = data_about_movie['keywords']
    except:
        pass
    duration = (data_about_movie['runtime']/60)
    
    
    # code for information about cast of movie
    casting = []
    url ="https://private-anon-defbcd4c1-rovicloudapi.apiary-proxy.com/api/v1/resolve/2/data_movie_credits/cast?id="+movie_id+"&in=en-US&in2=en-*&in3=*&page=1&by=role"
    url = url.replace(" ", "")
    casts = requests.get("%s?%s" % (url, params ), verify=False)
#    casts = casts.json()
 #   for cast in casts['credits']:
#        casting.append(cast['person']['name'])
 
 # code for information about crew of the movie
    crew = []
    url = "https://private-anon-defbcd4c1-rovicloudapi.apiary-proxy.com/api/v1/resolve/2/data_movie_credits/crew?id="+movie_id+"&in=en-US&in2=en-*&in3=*&page=1&by=type"
    url = url.replace(" ", "")
    crews_data = requests.get("%s?%s" % (url, params ), verify=False)
    crews_data = crews_data.json()
     ###   Lots of work to be done
=======
# ----------------------------------------------------------------------------------------------------------------------
def detail_movies(request,movie_id):

    data = movie_detail(movie_id)
    #return HttpResponse(json.dumps(data),content_type='application/json')
    return render(request,'web/movie_detail.html',data)

#----------------------------------------------------------------------------------------------------------------------

def detail_series(request, series_id):
>>>>>>> d57a3be53d0c0fbadf2f0d441c6ac1a16d31d99d

    data = series_detail(series_id)
    #return HttpResponse(json.dumps(data),content_type='application/json')
    return render(request,'web/series_detail.html',data)

#-----------------------------------------------------------------------------------------------------------------
def list_episode(request,season_id):

    data = episode_list(season_id)
    return render(request,'web/list_episode.html',data)

#----------------------------------------------------------------------------------------------------------------------
def detail_episode(request,episode_id):

<<<<<<< HEAD
    data = {'genre':genres,'year_of_release':year_of_release,'similar_movies':sim_movie,'name':name,'language':language,'fan_rating':fan_rating,'facebook_link':facebook,'duration':duration,"rating":rating,'synopsys':synopsys}
    return HttpResponse(json.dumps(data),content_type='application/json')

def detail_series(request, series_id):
    service_id =str(1063353154)
    year1 =datetime.datetime.now().year
    params = {'serviceId': service_id, 'by': -year1}
#    Getting info about series    
    url = "https://private-anon-defbcd4c1-rovicloudapi.apiary-proxy.com/api/v1/resolve/2/data_series?id="+ series_id+"&in=en-US&in2=en-*&in3=*"    
    url = url.replace(" ", "")
    series_data = requests.get("%s?%s" % (url, params ), verify=False)
    series_data= series_data.json()
    title = series_data['title']
    language = series_data['in']
    genre = series_data['genres']
    start_year = series_data['networks'][0]['start']
    end_year = series_data['networks'][0]['end']
    network = series_data['networks'][0]['name']
    facebook = 'None'
    #facebook = data_about_movie['facebooks'][0]['uri']
    
#    Getting info about Rating
    url = "https://private-anon-defbcd4c1-rovicloudapi.apiary-proxy.com/api/v1/resolve/2/data_series_ratings?id="+ series_id+"&country=US"
    url = url.replace(" ", "")
    series_rating = requests.get("%s?%s" % (url, params ), verify=False)
    series_rating = series_rating.json()
#    rating = series_rating['rating'][0]['rating']

# Getting synopsis of the series

    url = "https://private-anon-defbcd4c1-rovicloudapi.apiary-proxy.com/api/v1/resolve/2/data_series_synopses/best?id="+ series_id+"&length=short&length2=long&length3=plain&length4=extended&in=en-US&in2=en-*&in3=*"
    url = url.replace(" ", "")
    synopsys_data = requests.get("%s?%s" % (url, params ), verify=False)
    synopsys_data = synopsys_data.json()
    synopsis = synopsys_data['synopsis']['synopsis']


#    Getting info about session
    url = "https://private-anon-defbcd4c1-rovicloudapi.apiary-proxy.com/api/v1/resolve/2/data_series_seasons?id="+ series_id+"&in=en-US&in2=en-*&in3=*"
    url = url.replace(" ", "")
    seasons = []
    season_data = requests.get("%s?%s" % (url, params ), verify=False)
    season_data = season_data.json()

    for season in season_data['seasons']:
        try:
            season_dict ={'title':season['title'],'id':season['ref']['id'],'start':season['start'],'end':season['end']}
            seasons.append(season_dict)
        except:
            pass
#    Getting info about casts
    url = "https://private-anon-defbcd4c1-rovicloudapi.apiary-proxy.com/api/v1/resolve/2/data_series_credits/cast?id="+ series_id+"&page=1&by=role&by2=role&by3=role&by4=role&by5=role&in=en-US&in2=en-*&in3=*"
    url = url.replace(" ", "")
    casts_data = requests.get("%s?%s" % (url, params ), verify=False)
    casts_data = casts_data.json()

#    Getting info about crews
    url = "https://private-anon-defbcd4c1-rovicloudapi.apiary-proxy.com/api/v1/resolve/2/data_series_credits/crew?id="+ series_id+"&page=1&by=type&by2=type&by3=type&by4=type&by5=type&in=en-US&in2=en-*&in3=*"
    url = url.replace(" ", "")
    crews_data = requests.get("%s?%s" % (url, params ), verify=False)
    crews_data = crews_data.json()


    context = {'genre':genre,'name':title,'language':language,'synopsis':synopsis,'start':start_year,'end':end_year,'network':network,'seasons':seasons}
    return render(request,'web/series_detail.html',context)


def list_episode(request,season_id):
    service_id =str(1063353154)
    year1 =datetime.datetime.now().year
    params = {'serviceId': service_id, 'by': -year1}
    
    url = "https://private-anon-defbcd4c1-rovicloudapi.apiary-proxy.com/api/v1/resolve/2/data_season_episodes?id=914502705&page=1"
    
    url = url.replace(" ", "")
    list_ep = []
    list_episode = requests.get("%s?%s" % (url, params ), verify=False)
    list_episode = list_episode.json()
    
    for episode in list_episode['episodes']:
        ep_dict = {'id': episode['ref']['id'] ,'title': episode['title']}
        list_ep.append(ep_dict)
    context = {'list_episodes':list_ep}
    return render(request,'web/list_episode.html',context)


def detail_episode(request,episode_id):
    service_id =str(1063353154)
    year1 =datetime.datetime.now().year
    params = {'serviceId': service_id, 'by': -year1}
#    Information  to display episode datails

    url = "https://private-anon-defbcd4c1-rovicloudapi.apiary-proxy.com/api/v1/resolve/2/data_episode?id=906208182&in=en-US&in2=en-*&in3=*"
    url = url.replace(" ", "")
    episode_data = requests.get("%s?%s" % (url, params ), verify=False)
    episode_data = episode_data.json()
    title = episode_data['title']
    language = episode_data['in']
    time = episode_data['year']
    duration = int(episode_data['runtime'])/60
    genre = episode_data['genres']


# Information to display episode synopsis
    url = "https://private-anon-defbcd4c1-rovicloudapi.apiary-proxy.com/api/v1/resolve/2/data_episode_synopses/best?id=906208182&length=short&length2=long&length3=plain&length4=extended&in=en-US&in2=en-*&in3=*"
    url = url.replace(" ", "")
    synopsis_data = requests.get("%s?%s" % (url, params ), verify=False)
    synopsis_data = synopsis_data.json()
    synopsis = synopsis_data['synopsis']['synopsis']

    context = {'genre':genre,'name':title,'language':language,'synopsis':synopsis,'year':time,'duration':duration} 
    return render(request,'web/ep_details.html',context)

=======
    data = episode_detail(episode_id) 
    return render(request,'web/ep_details.html',data)
>>>>>>> d57a3be53d0c0fbadf2f0d441c6ac1a16d31d99d
