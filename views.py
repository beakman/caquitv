from django.shortcuts import render_to_response
from django.db.models import Q
from django.views.generic.simple import direct_to_template
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
import datetime
from tvshow.models import Show, Season, Episode
from accounts.models import UserProfile
import registration
from forms import ContactForm

    
def index(request):
    top_users = UserProfile.objects.order_by('-episodes_submited')[0:5]
    one_hour_ago = datetime.datetime.now() - datetime.timedelta(hours=1)
    sql_datetime = datetime.datetime.strftime(one_hour_ago, '%Y-%m-%d %H:%M:%S')
    # Show the number of users that has been login an hour ago.
    online_users = User.objects.filter(last_login__gt=sql_datetime, is_active__exact=1).order_by('-last_login')
    latest_episodes = Episode.objects.order_by('-pub_date')[0:5]
    params = {
        'latest':latest_episodes,
        'top_users':top_users,
        'online_users':online_users,
    }
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('user_home'))
    return direct_to_template(request, template='index.html', extra_context=params)
    
def home(request):
    top_users = UserProfile.objects.order_by('-episodes_submited')[0:5]
    one_hour_ago = datetime.datetime.now() - datetime.timedelta(hours=1)
    sql_datetime = datetime.datetime.strftime(one_hour_ago, '%Y-%m-%d %H:%M:%S')
    # Show the number of users that has been login an hour ago.
    online_users = User.objects.filter(last_login__gt=sql_datetime, is_active__exact=1).order_by('-last_login')
    latest_episodes = Episode.objects.order_by('-pub_date')[0:5]
    params = {
        'user':request.user,
        'latest':latest_episodes,
        'top_users':top_users,
        'online_users':online_users,
    }
    return render_to_response("base.html", params)

def search(request):
    query = request.GET.get('q', '')
    if query:
        qset = (
            Q(name__icontains=query)           
        )
        results = Show.objects.filter(qset).distinct()
    else:
        results = []
    if request.user.is_authenticated():
        return render_to_response("search_results.html", {
            'results':results, 
            'query':query,
            'user':request.user,
            'matches':len(results),
            })
    else:
        return render_to_response("search_results.html", {
            'results':results, 
            'query':query,
            'matches':len(results),
            })

def advanced_search(request):
    return direct_to_template(request, template='advanced_search.html')
    
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = '[Contact] ' + form.cleaned_data['subject']
            message = form.cleaned_data['message']
            sender = form.cleaned_data['sender']
            cc_myself = form.cleaned_data['cc_myself']
            recipients = ['carasdepoker@gmail.com']
            if cc_myself:
                recipients.append(sender)

            from django.core.mail import send_mail
            send_mail(subject, message, sender, recipients)
            return direct_to_template(request, template='sent.html')

    else:
        form = ContactForm() # An unbound form

    return render_to_response('contact.html', {
        'form': form,
    })

def help(request):
    return direct_to_template(request, template='help.html')
