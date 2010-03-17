from django.contrib.syndication.feeds import Feed
from django.core.exceptions import ObjectDoesNotExist
from tvshow.models import Show, Season, Episode
from django.utils.translation import ugettext_lazy as _


class LatestEpisodes(Feed):
    title = _("Caqui.tv - Latest episodes")
    link = "/feeds/latest/"
    description = _("Updates on episodes additions.")
    
    def items(self):
        return Episode.objects.order_by('-pub_date')[:10]
        
    def item_title(self, item):
        return item

    def item_description(self, item):
        return item.url

    def item_pubdate(self, item):
        return item.pub_date
                
    def item_author_name(self, item):
        return item.author.username

class ShowFeed(Feed):
    link = "/episodefeed/"

    def get_object(self, bits):
        if len(bits) != 1:
            raise ObjectDoesNotExist
        return Show.objects.get(slug=bits[0])
    
    def title(self, obj):
        return "Feed for %s" %obj.name
               
    def description(self, obj):
        return obj.plot
        
    def items(self, obj):
        items=[]
        seasons = Season.objects.filter(show=obj.name)
        for season in seasons:
            for episode in season.episodes.all():
                items.append(episode)
        return items                

    def item_pubdate(self, item):
        return item.pub_date
                
    def item_author_name(self, item):
        return item.author.username
        
