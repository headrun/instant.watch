import requests
import datetime
import time
import md5
import json
import pdb
from django.shortcuts import render
from django.conf import settings
import hmac, hashlib
import urllib
from tornado.auth import _oauth10a_signature
from urllib import urlencode
from urlparse import parse_qsl

CONSUMER_TOKEN  = {"key": "686fa81bea30c4af40903fffca654b6958d29ba0614e90728cd03623c2cc5d29",\
                   "secret": "a52c32c1af43b321c4a08a265ff996dfd28b2eea72fbaa500fa68129e1792ad4"}
 # TMPLS = json.loads(open("templates.json").read())

service_id =str(1063353154)
year1 =datetime.datetime.now().year

#-------------------------------------------------------------------------------------------------------
def _get_deeplink_authtoken(rovi_id):
    i_dict = {}
    i_dict['rovi_group_id'] = rovi_id
    i_dict['rovi_id_version'] = 2.0
    i_dict['_version'] = 0
    i_dict['timestamp'] = datetime.datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
    i_dict['customer_id'] = 'test_portal'
    #i_dict['platform_id'] = 'pc'
    #i_dict['source_id'] = 'cinemanow'
    i_dict['type'] = 'from_store'
    qs_keys = list(set(i_dict.keys()))
    qs_keys.sort()
    msg = ''
    for key in qs_keys:
        msg += '%s%s'%(key, i_dict[key])
        secret_key='fz8TYUdY9fUctIvc3YiiMiyUWZ5iRyW4'
        hmac_obj = hmac.new(secret_key, msg, hashlib.sha256)
        computed_digest = hmac_obj.hexdigest()
        i_dict['authentication']='hmac_sha256_%s'%(computed_digest)
        return i_dict

#-------------------------------------------------------------------------------------------------------
def get_unique_str():

    date = str(datetime.datetime.now())

    return md5.md5(date).hexdigest()

#--------------------------------------------------------------------------------------------------------
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
    #args.update(parameters)
    signature = _oauth10a_signature(consumer_token, method, url, args)
    base_args["oauth_signature"] = signature

    return base_args
#---------------------------------------------------------------------------------------------------------------
def check_response(url):

    url = url.replace(" ", "")
    params = {'serviceId': service_id, 'by': -year1}
    extraArguments = oauth_request_parameters(url,
                                 CONSUMER_TOKEN,
                                  params)
    params.update(extraArguments)
    params = urlencode(params)
    response = requests.get("%s?%s" % (url, params), verify=False)
    resp = response.json()
    if response.status_code == requests.codes.ok:
        result =  {'error':0,'resp':resp }
    else:
        message = resp['problems'][0]['message']
        result = {'error':1,'message':message}
    return result
#------------------------------------------------------------------------------------------------------------
def get_availability(id):
    url = "http://mycloud-dev.veveoinc.com/rovi_group_id/?contentId="+id
    id = requests.get(url)
    id = id.json()
    rovi_id = id['result']
    i_dict = _get_deeplink_authtoken(rovi_id)
    deeplink_url = 'http://ottlinks.veveo.net/get_availability?%s' %(urllib.urlencode(i_dict))
    availability_response = requests.get(deeplink_url, verify=False)
    availability_resp = availability_response.json()
    if availability_response.status_code == requests.codes.ok:
        result =  {'error':0,'data': availability_resp }
    else:
        message = availability_response['problems'][0]['message']
        result = {'error':1,'message':message}
    return result


# ---------------------------------------------------------------------------------------------------------
# List of trending movies
def trending_movies():

    url= "https://private-anon-defbcd4c1-rovicloudapi.apiary-proxy.com/api/v1/resolve/2/discover_all_trending_video/movies"
    result = check_response(url)
    if result['error']:
        return result
    else:
        resp = result['resp']
        result = {'error':result['error']}
        movies = []
        for element in resp['items']:
            try:
                dict1 = {'name':element['name'],'id':element['ref']['id'],'year':element['year'],'image': None}
                movies.append(dict1)
            except:
                pass
        result.update({'movies':movies})
        return result

#----------------------------------------------------------------------------------------------------------
# List of trending series
def trending_series():
    url ="https://private-anon-defbcd4c1-rovicloudapi.apiary-proxy.com/api/v1/resolve/2/discover_all_trending_video/series"
    result = check_response(url)
    if result['error']:
        return result
    else:
        resp = result['resp']
        result = {'error':result['error']}
        series = []
        for element in resp['items']:
            try:
                dict1 = {'name':element['name'],'id':element['ref']['id'],'year':element['year'],'image':None}
                series.append(dict1)
            except:
                pass
        result.update({"series":series})
        return result

#-----------------------------------------------------------------------------------------------------------
def movie_detail(movie_id):
    # code for information about movie

    url = "https://private-anon-defbcd4c1-rovicloudapi.apiary-proxy.com/api/v1/resolve/2/data_movie?id="+movie_id+"&in=en-US&in2=en-*&in3=*"
    result = check_response(url)

    if result['error']:
        return result
    else:
        movie_details = {'error':result['error']}
        data_about_movie = result['resp']
        genres = data_about_movie.get('genres','Not Available')
        name = data_about_movie['title']
        year_of_release = data_about_movie['year']
        language = data_about_movie['spoken']
        fan_rating = data_about_movie.get('rottenTomatoes',{}).get('fan',{}).get('score','None')
        facebook = data_about_movie.get('facebooks','Not available')
        try:
            facebook = data_about_movie.get['facebooks'][0]['uri']
        except:
            facebook = 'None'
        try:
            keywords = data_about_movie['keywords']
        except:
            pass
        duration = (data_about_movie['runtime']/60)

 # code for information about cast of movie
        #casting = []
        #url ="https://private-anon-defbcd4c1-rovicloudapi.apiary-proxy.com/api/v1/resolve/2/data_movie_credits/cast?id="+movie_id+"&in=en-US&in2=en-*&in3=*&page=1&by=role"
        #result = check_response(url)
       # if result['error']:
         #   return result
        #else:
        #    casts = result['resp']
        #   for cast in casts['credits']:
 #        casting.append(cast['person']['name'])

# code for information about crew of the movie
        #crew = []

        #url = "https://private-anon-defbcd4c1-rovicloudapi.apiary-proxy.com/api/v1/resolve/2/data_movie_credits/crew?id="+movie_id+"&in=en-US&in2=en-*&in3=*&page=1&by=type"
        #result = check_response(url)
        #if result['error']:
         #   return result
       # else:
        #    resp = result['resp']
    ###   Lots of work to be done
 # code for information about ratings of      the movie
        #rating = 'None'
        #url = "https://private-anon-defbcd4c1-rovicloudapi.apiary-proxy.com/api/v1/resolve/2/data_movie_ratings?id="+movie_id+"&country=US"
        #result = check_response(url)
       # if result['error']:
        #    return result
        #else:
         #   rating_data = result['resp']
#   for ratings in rating_data['rating']:
#       if ratings['rating']!='None':
#          rating = ratings['rating']
#      break

# code for getting related movie
       # url = "https://private-anon-defbcd4c1-rovicloudapi.apiary-proxy.com/api/v1/resolve/2/data_movie_related?id="+movie_id+"&relation=similar&in=en-US&in2=en-*&in3=*&page=1"
       # sim_movie = []
       # result = check_response(url)
        #if result['error']:
         #   return result
        #else:
         #   data_similar_movie = result['resp']
        # for similar_movies in data_similar_movie['related']:
#     dict_similar_movie={'title':similar_movies['content']['title'],'year':similar_movies['content']['year'],'id':similar_    movies['content']['ref']['id']}
#        sim_movie.append(dict_similar_movie)
# Information about synopsis of movie
        url = "https://private-anon-defbcd4c1-rovicloudapi.apiary-proxy.com/api/v1/resolve/2/data_movie_synopses/best?id="+movie_id+"&length=short&length2=long&length3=plain&length4=extended&in=en-US&in2=en-*&in3=*"
        result = check_response(url)

        if result['error']:
            pass
        else:
            synopsys_data = result['resp']
            synopsys = synopsys_data['synopsis']['synopsis']

# code for information about availability
#        availability_response = get_availability(movie_id)
        

        data = {'genre':genres,'year_of_release':year_of_release,'name':name,'language':language,'fan_rating':fan_rating,'facebook_link':facebook,'duration':duration,'synopsys':synopsys}
        movie_details.update({'data':data})
        return movie_details

# -------------------------------------------------------------------------------------------------------
def series_detail(series_id):
    
 #    Getting info about series
 
    url = "https://private-anon-defbcd4c1-rovicloudapi.apiary-proxy.com/api/v1/resolve/2/data_series?id="+ series_id+"&in=en-US&in2=en-*&in3=*"
    result = check_response(url)

    if result['error']:
        return result
    else:
        series_details = {'error':result['error']}
        series_data = result['resp']
        title = series_data['title']
        language = series_data['in']
        genre = series_data.get('genres','None')
        try:
            start_year = series_data['networks'][0]['start']
            end_year = series_data['networks'][0]['end']
            network = series_data['networks'][0]['name']
        except:
            start_year = "Not available"
            end_year = "Not available"
            network = "Not available"
        try:
            facebook = data_about_movie['facebooks'][0]['uri']
        except:
            facebook = None

    #    Getting info about Rating
    
        url = "https://private-anon-defbcd4c1-rovicloudapi.apiary-proxy.com/api/v1/resolve/2/data_series_ratings?id="+ series_id+"&country=US"
    #    result = check_response(url)
    #    if result['error']:
    #        pass
    #    else:
    #        series_rating = result['resp']
    #    rating = series_rating['rating'][0]['rating']

    # Getting synopsis of the series
        url = "https://private-anon-defbcd4c1-rovicloudapi.apiary-proxy.com/api/v1/resolve/2/data_series_synopses/best?id="+ series_id+"&length=short&length2=long&length3=plain&length4=extended&in=en-US&in2=en-*&in3=*"
        result = check_response(url)
        if result['error']:
            synopsis = "Not Available"
        else:
            synopsys_data = result['resp']
            synopsis = synopsys_data.get('synopsis',{}).get('synopsis','None')
#   Getting info about session
        url = "https://private-anon-defbcd4c1-rovicloudapi.apiary-proxy.com/api/v1/resolve/2/data_series_seasons?id="+ series_id+"&in=en-US&in2=en-*&in3=*"
        seasons = []
        result = check_response(url)
        if result['error']:
            pass
        else:
            season_data = result['resp']
            try:
                for season in season_data['seasons']:

                    season_dict ={'title':season['title'],'id':season['ref']['id'],'start':season['start'],'end':season['end']}
                    seasons.append(season_dict)
            except:
                pass
#    Getting info about casts
     #   url = "https://private-anon-defbcd4c1-rovicloudapi.apiary-proxy.com/api/v1/resolve/2/data_series_credits/cast?id="+ series_id+"&page=1&by=role&by2=role&by3=role&by4=role&by5=role&in=en-US&in2=en-*&in3=*"
      #  result = check_response(url)
     #   if result['error']:
    #        pass
    #    else:
    #        casts_data = result['resp']

#   Getting info about crews
     #   url = "https://private-anon-defbcd4c1-rovicloudapi.apiary-proxy.com/api/v1/resolve/2/data_series_credits/crew?id="+ series_id+"&page=1&by=type&by2=type&by3=type&by4=type&by5=type&in=en-US&in2=en-*&in3=*"
    #    result = check_response(url)
    #    if result['error']:
     #       pass
     #   else:
      #      crews_data = result['resp']

        data = {'genre':genre,'name':title,'language':language,'synopsis':synopsis,'start':start_year,'end':end_year,'network':    network,'seasons':seasons}
        series_details.update({'data':data})
        return series_details

#------------------------------------------------------------------------------------------------------------------
def episode_list(season_id):
    url = "https://private-anon-defbcd4c1-rovicloudapi.apiary-proxy.com/api/v1/resolve/2/data_season_episodes?id=914502705&page=1"
    list_ep = []
    result = check_response(url)
    if result['error']:
        return result
    else:
        list_episode = result['resp']
        for episode in list_episode['episodes']:
            ep_dict = {'id': episode['ref']['id'] ,'title': episode['title']}
            list_ep.append(ep_dict)
        return {'error':result['error'],'list_episodes':list_ep}

#-------------------------------------------------------------------------------------------------------------------
def episode_detail(episode_id):
     #    Information  to display episode datails

    url = "https://private-anon-defbcd4c1-rovicloudapi.apiary-proxy.com/api/v1/resolve/2/data_episode?id=906208182&in=en-US&in    2=en-*&in3=*"
    result = check_response(url)
    if result['error']:
        return result
    else:
        episode_data = result['resp']
        title = episode_data['title']
        language = episode_data['in']
        time = episode_data['year']
        duration = int(episode_data['runtime'])/60
        genre = episode_data['genres']


 # Information to display episode synopsis
        url = "https://private-anon-defbcd4c1-rovicloudapi.apiary-proxy.com/api/v1/resolve/2/data_episode_synopses/best?id=9062081    82&length=short&length2=long&length3=plain&length4=extended&in=en-US&in2=en-*&in3=*"
        result = check_response(url)
        if result['error']:
            return result
        else:
            synopsys_data = result['resp']
            synopsis = synopsys_data['synopsis']['synopsis']
        
       # availability_response = get_availability(episode_id)
        return {'error':result['error'],'genre':genre,'name':title,'language':language,'synopsis':synopsis,'year':time,'duration':duration}
