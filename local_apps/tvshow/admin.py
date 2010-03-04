from django.contrib import admin
from django.contrib.auth.models import User
from tvshow.models import Show, Season, Episode
from accounts.models import UserProfile

class ShowAdmin(admin.ModelAdmin):
    fields = ['name', 'plot', 'slug', 'pub_date', 'author']
    prepopulated_fields = {"slug": ("name",)}

class EpisodeAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    
class UserAdmin(admin.ModelAdmin):
    inlines = [ UserProfileInline ]
    
admin.site.register(Show, ShowAdmin)
admin.site.register(Season)
admin.site.register(Episode, EpisodeAdmin)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)


