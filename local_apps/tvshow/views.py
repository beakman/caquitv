from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.views.generic.simple import direct_to_template
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.template.defaultfilters import slugify
from django.template import RequestContext
from tvshow.models import Show, Season, Episode
from caquitv.forms import EpisodeForm, SeasonForm, ShowForm

def shows_by(request, letter):
    if letter=='0':
        shows=Show.objects.filter(Q(name__startswith='0')|Q(name__startswith='1')|Q(name__startswith='2')|Q(name__startswith='3')|Q(name__startswith='4')|Q(name__startswith='5')|Q(name__startswith='6')|Q(name__startswith='7')|Q(name__startswith='8')|Q(name__startswith='9'))
        letter='#'
    else:       
        shows = Show.objects.filter(Q(name__istartswith=letter)|Q(name__istartswith='The '+letter))
    if shows:
        return render_to_response('tvshow/shows_by.html', {
            'shows': shows, 
            'letter':letter, 
            'user':request.user,
            'matches':len(shows),
            })
    else:
        return direct_to_template(request, template='tvshow/not_found.html')

def shows_all(request):
    shows=Show.objects.order_by('name').all()
    if shows:
        return render_to_response('tvshow/shows_all.html', {
            'shows': shows, 
            'user':request.user,
            'matches':len(shows),
            })
    else:
        return direct_to_template(request, template='tvshow/not_found.html')

def episode_detail(request, show, season, slug):
    episode = Episode.objects.get(show__slug=show, season__no=season, slug=slug)
    return render_to_response('tvshow/episode_detail.html', {
        'episode': episode,
        'user': request.user,
    })
        
def edit_show(request, slug):
    show = Show.objects.get(slug=slug)
    if request.method == 'POST':
        # formulario enviado
        show_form = ShowForm(request.POST, instance=show)
        
        if show_form.is_valid():
            show_form.save()
            return HttpResponseRedirect(reverse('show_detail', args=[slug]))
    else:
        show_form = ShowForm(instance=show)
        
    return render_to_response(
        'tvshow/editshow.html', 
        {'form': show_form,}, 
        context_instance=RequestContext(request))
    
def broken_link(request, show, season, episode):
    ep = Episode.objects.get(show__slug=show, season__no=season, slug=episode)
    if not ep.rating.get_rating_for_user(request.user, request.META['REMOTE_ADDR']):    
        if ep.rating.score==5 & ep-rating.get_rating_for_user(user=User.objects.get(username=beakman)):
            ep.delete()
        else:
            ep.rating.add(score=1, user=request.user, ip_address=request.META['REMOTE_ADDR'])
            
    return HttpResponseRedirect(reverse('show_detail', args=[show]))
       
@login_required
def addepisode(request, slug):
    if request.method == 'POST':
        e = Episode(author=request.user, show=Show.objects.get(slug=slug))
        form = EpisodeForm(slug, request.POST, instance=e)        
        if form.is_valid():
            form.save()		
            return render_to_response('done.html', {
                'form_data':form.cleaned_data,
                'show':slug,
                'user':request.user,
                })         
    else:
        form = EpisodeForm(slug)
        
    return render_to_response('tvshow/addepisode.html', {
        'form':form,
        'slug':slug,
        'user':request.user,
    })

@login_required
def addseason(request, slug):
    if request.method == 'POST':
        s = Season(author=request.user, show=Show.objects.get(slug=slug))
        form = SeasonForm(slug, request.POST, instance=s)
        if form.is_valid():
            form.save()		
            return HttpResponseRedirect(reverse('addepisode', args=[slug]))         
    else:
        form = SeasonForm(slug)
           
    return render_to_response('tvshow/addseason.html', {
        'form':form,
        'slug':slug,
        'user':request.user,
    })
    
@login_required
def addshow(request):
    if request.method == 'POST':
        s = Show(author=request.user)
        form = ShowForm(request.POST, instance=s)        
        if form.is_valid():            
            form.save()		
            return HttpResponseRedirect(reverse('addepisode', args=[slugify(form.cleaned_data["name"])]))        
    else:
        form = ShowForm()
        
    return render_to_response('tvshow/addshow.html', {
        'form':form,
        'user':request.user,
    })

