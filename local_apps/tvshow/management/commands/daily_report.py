from django.core.management.base import NoArgsCommand
from django.core.mail import send_mail
from tvshow.models import Show, Season, Episode
import datetime

class Command(NoArgsCommand):
    help = "Sends a report with information about new entries in db."
    
    def handle_noargs(self, **options):
        subject = '[Caqui.tv] Daily report'
        sender = 'pakoman@gmail.com'
        destination = 'psalido@gmail.com'    
        today = datetime.datetime.today()
        yesterday = datetime.datetime.today() - datetime.timedelta(days=1)
        message = ''        
        shows = Show.objects.filter(
            pub_date__year=today.year, 
            pub_date__month=today.month, 
            pub_date__day=today.day
            )
        for show in shows:
            message += '\nShow: ' + show.name + '\n'
            for season in show.seasons.all():
                message += '-Season ' + str(season.no) + '\n'
                for episode in season.episodes.all():
                        message += '    * '+str(episode)+'\n      ('+str(episode.pub_date)+' by '+str(episode.author)+')\n'
        message += '\n--' + str(today.year)+'-'+str(today.month)+'-'+str(today.day)+' CaquiBot <'+sender+'>\n'
        send_mail(subject, message, sender, [destination], fail_silently=False)
