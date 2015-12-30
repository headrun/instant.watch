
from django.conf.urls import patterns, url
from web import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^movies/hot/$', views.list_movies, name='movie_list'),
    url(r'^tvseries/hot/$', views.list_series, name='series_list'),
    url(r'^movies/(?P<movie_id>\d+)/$',views.detail_movies, name='movie_details'),
    url(r'^tvseries/(?P<series_id>\d+)/$',views.detail_series, name= 'series_details'),
    url(r'^availability/(?P<id>\d+)/$', views.availability, name= 'availability')
)
