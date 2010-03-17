from django.db import models
from django.contrib.auth.models import User
import re
from django.db import models, IntegrityError
from django.template.defaultfilters import slugify
from djangoratings.fields import RatingField

class Show(models.Model):
    LANGUAGE_CHOICES = (
                ('AR','Arabic'),
                ('CA', 'Catalan'),
                ('DE', 'German'),
                ('EN', 'English'),
                ('ES', 'Spanish'),
                ('EU', 'Basque'),
                ('FI', 'Finnish'),
                ('FR', 'French'),
                ('GL', 'Galician'),
                ('HI', 'Hindi'),
                ('IT', 'Italian'),
                ('JA', 'Japanese'),
                ('KO', 'Korean'),
                ('PT', 'Portuguese'),
                ('RU', 'Russian'),
                                                                                
            )
    name = models.CharField(null=False, blank=False, max_length=255, unique=True)
    plot = models.TextField(null=True, blank=True)
    language =  models.CharField(max_length=1, choices=LANGUAGE_CHOICES)
    pub_date = models.DateTimeField(auto_now=True)
    slug = models.SlugField(help_text = 'Autogenerado', unique=True)
    author = models.ForeignKey(User, related_name='shows', null=True, blank=True)
    
    def __unicode__(self):
        return u"%s" % self.name
            
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name) 
        
        while True:
            try:
                super(Show, self).save()
            except IntegrityError:
                match_obj = re.match(r'^(.*)-(\d+)$', self.slug)
                if match_obj:
                    next_int = int(match_obj.group(2)) + 1
                    self.slug = match_obj.group(1) + '-' + str(next_int)
                else:
                    self.slug += '-2'
            else:
                break
     
class Season(models.Model):    
    show = models.ForeignKey(Show, to_field='name', related_name='seasons')
    pub_date = models.DateTimeField(auto_now=True)
    no = models.IntegerField()
    author = models.ForeignKey(User, related_name='seasons', null=True, blank=True)
    
    class Meta:
        ordering = (('-no'),)
        unique_together = (('show', 'no'),)
        
    def __unicode__(self):
        return str(self.no).zfill(2)
        
class Episode(models.Model):
    QUALITY_CHOICES = (
                ('HD','HDTV'),
                ('DV', 'DVD'),
                ('DR', 'DVD-Rip'),
                ('SA', 'SAT-Rip'),
                ('72', '720P'),                
                ('H7', '720P-HDTV'),
                ('TV', 'TV-Rip'),
                ('VH', 'VHS-Rip'),
                ('SC', 'Screener'),
                ('CA', 'CAM'),
                ('UN', 'Unknown'),
            )
    quality =  models.CharField(max_length=1, choices=QUALITY_CHOICES, default='UN')
    show = models.ForeignKey(Show, to_field='name', related_name='episodes', null=True)
    season = models.ForeignKey(Season, related_name='episodes')
    no = models.IntegerField()
    title = models.CharField(max_length=255)
    url = models.TextField()
    password = models.CharField(max_length=255, blank=True, null=True)
    pub_date = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, related_name='episodes')
    rating = RatingField(range=5, allow_anonymous = True)
    slug = models.SlugField(help_text = 'Autogenerado', unique=True)
    prepopulated_fields = {"slug": ("title",)}
       
    class Meta:
        ordering = ('-no',)

    def __unicode__(self):
        season_no = str(self.season.no).zfill(2)
        episode_no = str(self.no).zfill(2)
        formated_name = "S%sE%s - %s [%s]" % (season_no, episode_no, self.title, self.get_quality_display())
        return formated_name
    
    def save(self, *args, **kwargs):            
        if not self.slug:
            self.slug = slugify(self.title) 
        
        while True:
            try:
                super(Episode, self).save()
            except IntegrityError:
                match_obj = re.match(r'^(.*)-(\d+)$', self.slug)
                if match_obj:
                    next_int = int(match_obj.group(2)) + 1
                    self.slug = match_obj.group(1) + '-' + str(next_int)
                else:
                    self.slug += '-2'
            else:
                break
    
    def get_absolute_url(self):
        return "/shows/%s/%d/%s/" % (self.show.slug, self.season.no, self.slug)



