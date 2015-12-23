import requests

import datetime
import time
import md5
import json
import pdb
from django.shortcuts import render
from django.conf import settings

from tornado.auth import _oauth10a_signature
from urllib import urlencode
from urlparse import parse_qsl

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

def index(request):

    service_id =str(1063353154)
    year1 =datetime.datetime.now().year
    params = {'serviceId': service_id, 'by': -year1}


#   code for series
    url ="https://private-anon-defbcd4c1-rovicloudapi.apiary-proxy.com/api/v1/resolve/2/discover_all_trending_video/series"
    

    extraArguments = oauth_request_parameters(url,
                             CONSUMER_TOKEN,
                             params)

    params.update(extraArguments)
    params = urlencode(params)

    resp = requests.get("%s?%s" % (url,params), verify=False)

    print "Series"
    print "%s?%s" % (url,params)
    
    resp = resp.json()
    series = []
    for element in resp['items']:
        series.append(element['name'])


# code for movies
    url ="https://private-anon-defbcd4c1-rovicloudapi.apiary-proxy.com/api/v1/resolve/2/discover_all_trending_video/movies"
    resp = requests.get("%s?%s" % (url, params), verify=False)
    resp = resp.json()
    movies = []
    
    print "Movies"
    print "%s?%s" % (url, params)
    for element in resp['items']:
        dict1 = {'name':element['name'],'id':element['ref']['id'],'year':element['year']}
        movies.append(dict1)


# code for image
    url = "https://private-anon-defbcd4c1-rovicloudapi.apiary-proxy.com/api/v1/resolve/2/media_image/sized?id=172343929&aspect=3x4&size=large&zoom=std"
    image = requests.get("%s?%s" % (url, params ), verify=False)
    
    
    context = {"serieses": series,"movieses":movies,"image": image}
    return render(request, 'web/index.html',context)


def main(request):
    return render(request,'web/main.html')



def detail_movies(request,movie_id):
    service_id =str(1063353154)
    year1 =datetime.datetime.now().year
    params = {'serviceId': service_id, 'by': -year1}
    # code for information about movie
 
    url = "https://private-anon-defbcd4c1-rovicloudapi.apiary-proxy.com/api/v1/resolve/2/data_movie?id="+movie_id+"&in=en-US&in2=en-*&in3=*"
    data_about_movie = requests.get("%s?%s" % (url, params ), verify=False)
    data_about_movie = data_about_movie.json()
    genres = data_about_movie['genres']
    name = data_about_movie['title']
    year_of_release = data_about_movie['year']
    language = data_about_movie['spoken']
    fan_rating = data_about_movie['rottenTomatoes']['fan']['score']
    facebook = data_about_movie['facebooks'][0]['uri']
    keywords = data_about_movie['keywords']
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

# code for information about ratings of the movie
    rating = 'None'
    url = "https://private-anon-defbcd4c1-rovicloudapi.apiary-proxy.com/api/v1/resolve/2/data_movie_ratings?id="+movie_id+"&country=US"
    url = url.replace(" ", "")
    rating_data = requests.get("%s?%s" % (url, params ), verify=False)
    rating_data = rating_data.json()
#    for ratings in rating_data['rating']:
#        if ratings['rating']!='None':
#            rating = ratings['rating']
#        break

# code for getting related movie
    url = "https://private-anon-defbcd4c1-rovicloudapi.apiary-proxy.com/api/v1/resolve/2/data_movie_related?id="+movie_id+"&relation=similar&in=en-US&in2=en-*&in3=*&page=1"
    url = url.replace(" ", "")
    data_about_movie = requests.get("%s?%s" % (url, params ), verify=False)
 #Lots of works need to be  done
 
# code for information about synopsis of movie
    url = "https://private-anon-defbcd4c1-rovicloudapi.apiary-proxy.com/api/v1/resolve/2/data_movie_synopses/best?id="+movie_id+"&length=short&length2=long&length3=plain&length4=extended&in=en-US&in2=en-*&in3=*"
    url = url.replace(" ", "")
    synopsys_data = requests.get("%s?%s" % (url, params ), verify=False)
    synopsys_data = synopsys_data.json()
    synopsys = synopsys_data['synopsis']['synopsis']


    context = {'genre':genres,'year_of_release':year_of_release,'name':name,'language':language,'fan_rating':fan_rating,'facebook_link':facebook,'duration':duration,"rating":rating,'synopsys':synopsys}
    return render(request,'web/movie_detail.html',context)
