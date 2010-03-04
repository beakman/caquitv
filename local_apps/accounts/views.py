#from caquitv.local_apps.accounts.models import UserProfile
#from django.shortcuts import render_to_response

#def profile(request, username):
#    user = UserProfile.objects.get(user__username=username)
#    params = {
#            'user':username,
#            'pic':user.avatar,
#            'web':user.url,
#            'email':user.user.email,
#            'karma':user.karma,
#            }
#    if request.user.is_authenticated():
#        return render_to_response("user_profile.html", params)


        
