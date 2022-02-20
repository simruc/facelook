from ast import keyword
from dataclasses import Field
from email import message
from operator import mod
from django.dispatch import receiver
from django.http import Http404, request
from django.shortcuts import render,redirect,get_object_or_404
from django.template import context
from .models import MessageModel, Relationship, ThreadModel, UserProfile, User
from .forms import UserProfileForm, ProfileCreateForm, Threadform, Messageform, LocationForm
from django.contrib import auth,messages
from posts.models import Post
from posts.forms import PostCreateForm, CommentCreateForm
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import View, CreateView
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.views.decorators.cache import cache_control



#geolocation
from geopy.geocoders import Nominatim
from.utils import get_geo, get_ip_address
from geopy.distance import geodesic

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage, send_mail
from django.conf import settings
 
def register(request):
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            
            password = form.cleaned_data['password1']
            username = email.split('@')[0]
            
            user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
           
            user.save()
            return redirect('accounts:login')
        

    else:
        form = UserProfileForm()

    

    context = {
            'form' : form
        }

    return render(request, 'accounts/signup.html', context)


# Create your views here.
# def register(request):
    
#     if request.method == 'POST':
#         form = UserProfileForm(request.POST)

#         if form.is_valid():
            
#             form.save()
           

#     else:
#         form = UserProfileForm()

    

#     context = {
#             'form' : form
#         }

#     return render(request, 'accounts/signup.html', context)
# class RegisterView(CreateView):
#     model = User
#     fields = ('first_name', 'last_name', 'username', 'password')
#     template_name = 'accounts/signup.html'



# def login(request):
#     if request.method == 'POST':
#         email = request.POST['email']
#         password = request.POST['password']

#         user = auth.authenticate(email=email, password=password)

#         if user is not None:
#             auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
#             return redirect('/posts/create_post')

#         else:
#             messages.error(request, 'Invalid credentials')
#             return redirect('/accounts/register')

#     return render(request, 'accounts/signup.html')






@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def home(request):
    if request.method == 'POST':
        form = PostCreateForm(request.POST, files=request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user_id = request.user.id
            post.save()      
                 
    else:
        form = PostCreateForm()

    # users = User.objects.exclude(username = request.user.username)
    # try:
    #     friend = Friend.objects.get(current_user=request.user)
    # except ObjectDoesNotExist:
    #     friend = Friend.objects.create(current_user=request.user)
    # friends = friend.users.all()
    comment_form = CommentCreateForm()
    user = User.objects.get(pk= request.user.pk)
    users = User.objects.exclude(username = request.user.username)
    
    friends = user.friends.all()
    my_posts = Post.objects.filter(user=user)
    posts = Post.objects.filter(user__in=friends)
    all_posts = my_posts|posts
    paginator = Paginator(all_posts,1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    print(all_posts)
    print(friends)

    # likes = Like.objects.get(pk=post.pk)
    # for post in posts:
    #     if like >=1 :
    #         if like==True:
    #             like+=1
        
    context = {
        'users':users,
        'form': form,
        'friends': friends,
        'posts': all_posts,
        'comment_form':comment_form,
        'my_posts': my_posts,
        'page_obj': page_obj
        
    }
    return render(request, 'home.html', context)


@cache_control(no_cache=True, must_revalidate=True)
def logout(request):
    auth.logout(request)
    messages.success(request,'you are successfully logged out')
    return redirect('accounts:login')

def post_delete(request,pk):
    post = Post.objects.get(pk=pk)
    post.delete()

    return redirect('accounts:home')

@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def post_update(request, pk):
    post = Post.objects.get(pk=pk)
    if request.method == 'POST':
        form = PostCreateForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('accounts:home')
    else:
        form = PostCreateForm()

    context = {
        'form': form,
        'post': post
    }
    return render(request, 'accounts/post_update.html', context )
        



# def change_friends(request, operation, pk):
#     new_friend = User.objects.get(pk=pk)
#     if operation =='add':
#         Friend.make_friend(request.user, new_friend)

#     elif operation == 'remove':
#         Friend.lose_friend(request.user, new_friend)
#     return redirect('accounts:home')
@login_required
def CommentList(request,pk):
    post = Post.objects.get(pk=pk)
    comments=post.comment_set.all()
    comments_count = comments.count()

    context={
        'post':post,
        'comments':comments,
        'comments_count': comments_count

    }

    return render(request, 'posts/comments.html', context)



def add_friends(request, pk):
    friend = User.objects.get(pk=pk)
    print(friend)
    user = User.objects.get(pk= request.user.pk)
    print(user)
    friend.friends.add(user)
    user.friends.add(friend)
    
    return redirect('/accounts/home/society')

def remove_friends(request, id):

    
    user = User.objects.get(id=request.user.id)
    user_p= UserProfile.objects.get(id=id)
    
    friend = user_p.user
    print(user)
    
    print(friend)
    
    user.friends.remove(friend)
    friend.friends.remove(user)
    Rel= Relationship.objects.filter(Q(sender=friend, receiver=user, status='accepted')| Q(sender=user, receiver=friend, status='accepted'))
    Rel.delete()
    
    return redirect('/accounts/home/society')

# def profile(request):
#     user = User.objects.get(pk= request.user.pk)
#     friends = user.friends.all()
#     context={
#         'friends': friends
#     }
#     return render(request, 'accounts/profile.html', context)

@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def edit_profile1(request):
    userprofile = UserProfile.objects.get(user_id=request.user.id)
    form = ProfileCreateForm(instance=userprofile)
    if request.method == 'POST':
        form = ProfileCreateForm(request.POST, request.FILES, instance=userprofile)
        if form.is_valid():
            form.save()
           
        
            
    else:
        form = ProfileCreateForm()
    context ={
        'form': form
    }        
    return render(request, 'accounts/edit_profile1.html', context)

@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def ProfileDetailView(request):
    
    context={}
    
    # template_name = 'accounts/profile.html'
    
    # def get_context_data(self, **kwargs):
    #     # Call the base implementation first to get a context
    #     context = super().get_context_data(**kwargs)
    #     # Add in a QuerySet of all the books
        
    #     context['profile'] = UserProfile.objects.filter(user=request.user)
    #     return context

    # def get_queryset(self):
    #     return get_object_or_404(UserProfile,

    #         slug=self.kwargs['slug']
    #     )
    context['object'] = UserProfile.objects.get(user=request.user)
    
    return render(request, 'accounts/profile.html', context)


@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def Friendlist(request):
    context={}
    
    user_profile = UserProfile.objects.get(user_id= request.user.id)
    other_user_profile= UserProfile.objects.exclude(user_id = request.user.id)
    

    # invites = list(Relationship.objects.received_invitations(user))
    invites = list(Relationship.objects.filter(receiver=user_profile.user, status='sent'))
    accepted =list(Relationship.objects.filter(receiver=user_profile.user, status='accepted'))

    available_list = User.objects.get_all_profiles_to_invite(user_profile.user)
    sent_list = User.objects.get_all_sent_invites(user_profile.user)
    print('###available list:', available_list)
    print('@@@@@sent_list',sent_list)
    print("invites", invites)
    print('accepted: ', accepted)

    # invitations = list(invites)
    user_friends = list(user_profile.user.friends.all().exclude(username=request.user.username))
    friends=[]
    for f in user_friends:
        userprofile=UserProfile.objects.get(user=f)
        friends.append(userprofile)
    print('friends :', friends)

    context['accepted'] = accepted
    context['friends'] = friends
    context['users'] = other_user_profile
    context['invites']= invites
    context['available_list']= available_list
    context['sent_list'] = sent_list
   
   
    return render(request, 'accounts/society.html', context)


@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def ListThread(request):
    threads= ThreadModel.objects.filter(Q(user=request.user)|Q(receiver=request.user))
    context={'threads':threads}
    return render(request, 'accounts/inbox.html', context)

# def CreateThread(request):
#     if request.method== "POST":
#         form = Threadform(request.POST)
#         username = request.POST.get('username')
#         # try:
#         receiver = User.objects.get(username=username)
#         user = User.objects.get(username=request.user.username)
#         if ThreadModel.objects.filter(user=user, receiver=receiver).exists():
#             thread= ThreadModel.objects.filter(user=user, receiver=receiver)
#             return redirect('accounts:thread', pk=thread.pk)
#         elif ThreadModel.objects.filter(user=receiver, receiver=user).exists():
#             thread= ThreadModel.objects.filter(user=receiver, receiver=user)
#             return redirect('accounts:thread', pk=thread.pk)

#         if form.is_valid():
#             thread=ThreadModel(user=user, receiver= receiver)
#             thread.save()
#             return redirect('accounts:thread', pk=thread.pk)
#         # except:
#         #     return redirect('accounts:create-thread')
#     else:
#         form = Threadform()

        
#     return render(request, 'accounts/create_thread.html', {'form':form})



class CreateThread(View):
    def get(self, request, *args, **kwargs):
        form = Threadform()

        context = {
            'form': form
        }

        return render(request, 'accounts/create_thread.html', context)

    def post(self, request, *args, **kwargs):
        form = Threadform(request.POST)

        username = request.POST.get('username')
        r_user = User.objects.get(pk = request.user.pk)

        try:
            receiver = User.objects.get(username=username)
            if ThreadModel.objects.filter(user=r_user, receiver=receiver).exists():
                thread = ThreadModel.objects.filter(user=r_user, receiver=receiver)[0]
                return redirect('chat:room', thread.receiver.username)
            elif ThreadModel.objects.filter(user=receiver, receiver=r_user).exists():
                thread = ThreadModel.objects.filter(user=receiver, receiver=r_user)[0]
                return redirect('chat:room', thread.user.username)

            if form.is_valid():
                thread = ThreadModel(
                    user=r_user,
                    receiver=receiver
                )
                thread.save()

                return redirect('chat:room', thread.receiver.username)
        except:
            return redirect('accounts:create-thread')


@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def threadview(request, pk):
    form = Messageform()
    thread = ThreadModel.objects.get(pk=pk)
    message_list = MessageModel.objects.filter(thread__pk__contains=pk)
    context = {
        'thread': thread,
        'form': form,
        'message_list': message_list,
    }
    return render(request, 'accounts/thread1.html', context)



def create_message(request, pk):
    thread = ThreadModel.objects.get(pk=pk)
    user= User.objects.get(username=request.user.username)
    if thread.receiver == user:
        receiver = thread.user

    else:
        receiver = thread.receiver

    message = MessageModel.objects.create(
        thread=thread,
        sender_user = user,
        receiver_user = receiver,
        body = request.POST.get('message')
        
    )
    message.save()
    return redirect('accounts:thread', pk=pk)


def send_invite(request,pk):
    
    user_profile= UserProfile.objects.get(user_id=request.user.id)
    
    other_user_profile = UserProfile.objects.get(pk=pk)
    rel =Relationship.objects.create(sender=user_profile.user, receiver=other_user_profile.user, status='sent')
    rel.save()
    return redirect('accounts:society')


def accept_invite(request,pk):
    user_profile= UserProfile.objects.get(user_id=request.user.id)
    other_user= User.objects.get(pk=pk)
    other_user_profile = UserProfile.objects.get(user=other_user)
    rel =Relationship.objects.create(sender=other_user_profile.user, receiver=user_profile.user, status='accepted')
    rel.save()
    rel1= Relationship.objects.filter(receiver=user_profile.user, sender=other_user_profile.user, status='sent')
    if rel:
        rel1.delete()

    print('rel',rel)
    return redirect('accounts:society')


def mutual_friends(request,pk):
    r_user = User.objects.get(pk= request.user.pk)
    other_user = User.objects.get(pk=pk)

    friends = list(r_user.friends.all())
    other_user_friends = list(other_user.friends.all())

    mutual =[]
    for f in friends:
        if f in other_user_friends:
            mutual.append(f)
            
        print(mutual)
    mutual_count = mutual.count()
    context ={
        'mutual': mutual,
        'mutual_count': mutual_count
    }

    return render(request,'accounts/user.html', context)


@login_required
def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']

        if keyword:
            users = User.objects.filter(Q(first_name__icontains=keyword)|Q(last_name__icontains=keyword)|Q(username__icontains=keyword))

        context = {
            'users': users
        }
        return render(request, 'accounts/search.html', context)


@login_required
def search_by_location(request):
    # ip_ = get_ip_address(request)
    user= UserProfile.objects.get(user_id=request.user.id)
    location_= user.city

    geolocator = Nominatim(user_agent='accounts')
    location= geolocator.geocode(location_)

    l_lat= location.latitude
    l_lon= location.longitude
    pointA= (l_lat, l_lon)
    
    users= UserProfile.objects.all().exclude(user_id=request.user.id)
    user_list= []
    if 'keyword' in request.GET:
        keyword = int(request.GET['keyword'])
    
        
        for u in users:
            try:
                destination_ = u.city
            except ObjectDoesNotExist:
                raise Http404

        
            destination= geolocator.geocode(destination_)
            d_lat= destination.latitude
            d_lon= destination.longitude
            pointB= (d_lat,d_lon)
            
            distance = round(geodesic(pointA,pointB).km,2)
            if distance < keyword:
                user_list.append(u)

    context={
        'users'   : users,
        'location': location,
        # 'destination': destination,
        # 'distance': distance,
        'user_list': user_list,
        
    }

    return render (request, 'accounts/geolocation.html', context)



def reject_invite(request, pk):
    user= User.objects.get(username= request.user.username)
    sender= User.objects.get(pk=pk)
    rel= Relationship.objects.filter(sender=sender, receiver=user)
    if rel.exists():
        rel.delete()
    

    return redirect('accounts:society')


@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def detailprofile(request,pk):
    
    userprofile = UserProfile.objects.get(pk=pk)
    user=User.objects.get(username=userprofile.user.username)
    r_user = User.objects.get(pk= request.user.pk)
    sent_list = User.objects.get_all_sent_invites(r_user)
    accepted_list = []
    qs= Relationship.objects.filter(Q(sender=r_user, status='accepted')|Q(receiver=r_user, status='accepted'))
    for rel in qs:
        if rel.receiver==r_user:
            u_profile = UserProfile.objects.get(user=rel.sender)
            accepted_list.append(u_profile)
        if rel.sender==r_user:
            u_profile = UserProfile.objects.get(user=rel.receiver)
            accepted_list.append(u_profile)
        

    friends = list(r_user.friends.all())
    print('userfriends', friends)
    
    
    other_user_friends = list(user.friends.all())
    print('detailuser', user)

    friends_profile=[]
    for f in friends:
        o_userprofile= UserProfile.objects.get(user=f)
        friends_profile.append(o_userprofile)

    other_friends_profile=[]
    for f in other_user_friends:
        e_userprofile= UserProfile.objects.get(user=f)
        other_friends_profile.append(e_userprofile)

    mutual =[]
    
    for f in friends_profile:
        if f in other_friends_profile:
            mutual.append(f)
            
    print('mutual:' ,mutual)
    
    mutual_count = len(mutual)
    

    friends_count = user.friends.all().count()
    full_name = user.first_name + " " +user.last_name

    context = {
        
        'userprofile': userprofile,
        'friends_count': friends_count,
        'full_name': full_name,
        'mutual': mutual,
        'mutual_count': mutual_count,
        'user': user,
        'sent_list': sent_list,
        'accepted_list':accepted_list,
        'friends': friends,

    }

    return render(request, 'accounts/other_profile.html', context)






