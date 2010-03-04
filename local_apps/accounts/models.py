from django.db import models
from PIL import Image
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from tvshow.models import Episode

def autoincrement(sender, instance, created, **kwargs):
    # Autoincrements the user.episodes_submited field
    if created:
	    profile = UserProfile.objects.get(user=instance.author)
	    profile.episodes_submited += 1
	    profile.save()

post_save.connect(autoincrement, sender=Episode)

def user_post_save(sender, instance, **kwargs):
    # Create default user profile
    profile, new = UserProfile.objects.get_or_create(user=instance)

post_save.connect(user_post_save, sender=User)


class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    url = models.URLField(null=True, blank=True, default='')
    episodes_submited = models.IntegerField(null=True, blank=True, default=0)
    avatar = models.ImageField(
        upload_to='uploads/img/avatar/', 
        null=True, blank=True, default='uploads/img/avatar/noimage.jpg')

    def get_absolute_url(self):
        return ('profiles_profile_detail', (), { 'username': self.user.username })
    get_absolute_url = models.permalink(get_absolute_url)

    def save(self, size=(120, 120), **kwargs):
    
        if not self.id and not self.avatar:
            return
            
        super(UserProfile, self).save()
        pw = self.avatar.width
        ph = self.avatar.height
        nw = size[0]
        nh = size[1]
    
        # only do this if the image needs resizing
        if (pw, ph) != (nw, nh):
            filename = str(self.avatar.path)
            image = Image.open(filename)
            pr = float(pw) / float(ph)
            nr = float(nw) / float(nh)
        
            if pr > nr:
                # photo aspect is wider than destination ratio
                tw = int(round(nh * pr))
                image = image.resize((tw, nh), Image.ANTIALIAS)
                l = int(round(( tw - nw ) / 2.0))
                image = image.crop((l, 0, l + nw, nh))
            elif pr < nr:
                # photo aspect is taller than destination ratio
                th = int(round(nw / pr))
                image = image.resize((nw, th), Image.ANTIALIAS)
                t = int(round(( th - nh ) / 2.0))
                print((0, t, nw, t + nh))
                image = image.crop((0, t, nw, t + nh))
            else:
                # photo aspect matches the destination ratio
                image = image.resize(size, Image.ANTIALIAS)
            
            image.save(filename)

