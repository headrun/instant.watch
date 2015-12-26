
from django.conf.urls import patterns, url
from web import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^movies/(?P<movie_id>\d+)/$',views.detail_movies, name='movie_details'),
    url(r'^series/(?P<series_id>\d+)/$',views.detail_series, name= 'series_details'),
    url(r'^season/(?P<season_id>\d+)/$',views.list_episode, name='episode_list'),
    url(r'^episode/(?P<episode_id>\d+)/$', views.detail_episode, name = 'episode_detail'),
)
