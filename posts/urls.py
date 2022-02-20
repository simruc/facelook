from django.urls import path
# from django.contrib.auth import views as auth_views
from . import views


app_name = 'posts'

urlpatterns = [ 

        # path('create_post/', views.create_post, name= 'create_post'),
        path('like_post/<pk>', views.like_post, name='like_post' ),
        path('comment_post/<pk>', views.comment_post, name='comment_post' ),

        path('unlike/<pk>', views.unlike, name='unlike' ),
        
                
                
                ]