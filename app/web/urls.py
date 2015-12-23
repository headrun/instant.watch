
from django.conf.urls import patterns, url
from web import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^details/(?P<movie_id>\d+)/$',views.detail_movies, name='movie_details')
)
