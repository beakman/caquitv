from django import forms
from django.contrib.auth.models import User
from tvshow.models import Episode, Season, Show

class ShowForm(forms.ModelForm):
    def __init__(self, *args, **kwargs): 
        super(ShowForm, self).__init__(*args, **kwargs)
        self.fields['plot'].widget.attrs['cols'] = 40
        self.fields['plot'].widget.attrs['rows'] = 3
                
    class Meta:
        model = Show
        exclude = ('slug', 'pub_date')        

        
class SeasonForm(forms.ModelForm):
    no = forms.IntegerField(min_value=0, max_value=50)
    def __init__(self, slug, *args, **kwargs):
        super(SeasonForm, self).__init__(*args,**kwargs)
        
    class Meta:
        model = Season
        exclude = ('show', 'pub_date')

class EpisodeForm(forms.ModelForm):
    no = forms.IntegerField(min_value=1, max_value=50)
    def __init__(self, slug, *args, **kwargs):
        super(EpisodeForm, self).__init__(*args,**kwargs)
        self.fields['season'].queryset = Season.objects.filter(show__slug=slug)
        
    class Meta:
        model = Episode
        exclude = ('show', 'author', 'pub_date', 'status', 'slug')
        
class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)

