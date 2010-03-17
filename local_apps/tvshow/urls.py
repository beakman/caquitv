from django.conf.urls.defaults import *
from django.views.generic import list_detail
from django.contrib.auth.decorators import login_required
from tvshow.models import Show, Season, Episode
from tvshow.views import *

show_info = {'queryset': Show.objects.all(),}

urlpatterns = patterns('caquitv.local_apps.tvshow.views',
    # Sort shows by name, view show details or episode details
    url(r'^([0-9A-Za-z])/$', shows_by, name='shows'),
    url(r'^all/$', shows_all, name='shows_all'),
    url(r'^(?P<slug>[-\w]+)/$', list_detail.object_detail, show_info, name="show_detail"),
    url(r'^(?P<show>[-\w]+)/(?P<season>\d+)/(?P<slug>[-\w]+)/$', episode_detail, name="episode_detail"),
    
    # Edit show info
    url(r'^edit/(?P<slug>[-\w]+)/$', edit_show, name="edit_show"),
    
    # Vote broken link
    url(r'^(?P<show>[-\w]+)/(?P<season>\d+)/(?P<episode>[-\w]+)/broken/$', broken_link, name='broken_link'),
    
    # Add shows, seasons or episodes
    url(r'^(?P<slug>[-\w]+)/addseason/', addseason, name="addseason"),
    url(r'^(?P<slug>[-\w]+)/addepisode/$', addepisode, name="addepisode"),

)

