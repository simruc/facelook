from accounts.models import User, UserProfile
from django.shortcuts import redirect, render
from django.db.models import Q


def user_name(request):
    # user = User.objects.get(pk=request.user.pk)
    
        
    if request.user.is_authenticated:
        user = request.user
        userprofile = UserProfile.objects.get(user_id = request.user.id)
        image = userprofile.image
        user_name = user.username
        full_name = userprofile.first_name + ' '+ userprofile.last_name
        return dict(user_name=user_name, full_name=full_name,image=image)
    
    else:
        return{}
            
        
        

def friends_count(request):
    # user = User.objects.get(pk=request.user.pk)
    
    
        

    if request.user.is_authenticated:

        user = request.user
        friends_count = user.friends.all().count()
        return dict(friends_count=friends_count)
    else:
        return {}

    
# def search(request):
#     if 'keyword' in request.GET:
#         keyword = request.GET['keyword']

#         if keyword:
#             users = User.objects.filter(Q(first_name__icontains=keyword)|Q(last_name__icontains=keyword)|Q(username__icontains=keyword))

#         return dict(users=users)
                    
        
        
