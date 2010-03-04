from django.conf.urls.defaults import *
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic.simple import direct_to_template
from feeds import ShowFeed, LatestEpisodes
from views import index, home
from tvshow.views import addshow
from accounts.forms import UserProfileForm
from registration.views import activate
from registration.views import register
#from caquitv.external_apps import profiles
#from caquitv.external_apps import chronograph

admin.autodiscover()

feeds = {
    'show': ShowFeed,
    'latest': LatestEpisodes,
}

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    url(r'^admin/chronograph/job/(?P<pk>\d+)/run/$', 'chronograph.views.job_run', name="admin_chronograph_job_run"),
    url(r'^$', index, name="index"),
    url(r'^home/$', login_required(home), name='user_home'),
    url(r'^search/$', 'views.search', name='search'),
    url(r'^search/advanced$', 'direct_to_template', {'template': 'advanced_search.html'}, name='advanced_search'),
    (r'^help/$', direct_to_template, {'template': 'help.html'}),
    url(r'^contact$', 'views.contact', name='contact'),
    (r'^shows/', include('tvshow.urls')),
    url(r'^show/add/$', addshow, name='addshow'),
    (r'^accounts/', include('registration.backends.default.urls')),
    (r'^profiles/edit', 'profiles.views.edit_profile', {'form_class': UserProfileForm,}),
    (r'^profiles/', include('profiles.urls')),
    (r'^comments/', include('django.contrib.comments.urls')),
    (r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
)
