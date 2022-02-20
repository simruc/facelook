from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [ 
        
        path('login/', auth_views.LoginView.as_view(template_name = 'login.html'), name = 'login'),
        

        

        path('home/', views.home, name= 'home'),
        path('home/delete/<pk>/', views.post_delete, name='post-delete'),
        path('home/update/<pk>/', views.post_update, name='post-update'),

        path('add_friend/<pk>', views.add_friends, name = 'add_friends'),
        path('remove_friends/<id>', views.remove_friends, name = 'remove_friends'),


        path('home/profile/', views.ProfileDetailView, name='profile'),
        path('home/edit_profile1/', views.edit_profile1, name='edit_profile1'),
        path('home/society/<pk>/', views.detailprofile, name = 'other-profile'),

        path('home/society/', views.Friendlist, name='society'),
        

        
        path('inbox/', views.ListThread, name='inbox'),
        path('inbox/create-thread/', views.CreateThread.as_view(), name='create-thread'),
        path('inbox/<int:pk>/', views.threadview, name='thread'),
        path('inbox/<int:pk>/create-message/', views.create_message, name='create-message'),
        path('<int:pk>/comments', views.CommentList, name='commentlist'),


        path('send_invite/<pk>', views.send_invite, name='send_invite'),
        path('accept_invite/<pk>', views.accept_invite, name='accept_invite'),
        path('reject_invite/<pk>', views.reject_invite, name='reject_invite'),


        path('mutual/<pk>/', views.mutual_friends, name='mutual'),

        # Geosearch
        path('search', views.search, name='search'),
        path('geosearch/', views.search_by_location, name='geosearch'),
             
                
        ]