from audioop import reverse
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.forms import forms
from django.shortcuts import get_object_or_404, render, redirect

from accounts.models import UserProfile
from .models import Post,Comment
from .forms import CommentCreateForm, PostCreateForm
from accounts.models import User
from django.utils import timezone

# Create your views here.
def create_post(request):
    userprofile = UserProfile.objects.get(user_id = request.user.id)
    if request.method == 'POST':
        form = PostCreateForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user_id = request.user.id
            post.userprofile_id = userprofile.id
            post.userprofile_id.save()
            post.save()
        
           
            
    else:
        form = PostCreateForm()
    context = {
        'form': form
    }
    return render(request, 'home.html', context)


def like_post(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    user = User.objects.get(pk= request.user.pk)
    post.likes.add(user)
    return HttpResponseRedirect(reverse('accounts:home'))


def unlike(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    user = User.objects.get(pk= request.user.pk)
    if post.likes.filter(username=user.username).exists():
        post.likes.remove(user)
    return HttpResponseRedirect(reverse('accounts:home'))




def comment_post(request,pk):
    # post = get_object_or_404(Post, pk=pk)
    # user = request.user
    # context = {}
    # if request.method == 'POST':
    #     form = CommentCreateForm(request.POST)

        
    #     if form.is_valid():
    #         comment = form.save(commit=False)
    #         comment.post = post
    #         comment.user_id = user.id
    #         comment.created = timezone.now()
    #         comment.save()
            
    # else:
    #     form = CommentCreateForm()
    # context['form'] = 'form'
    # return redirect('accounts:home')

    post = get_object_or_404(Post, pk=pk)
   
    user = User.objects.get(pk=request.user.pk)
    

    comment = Comment.objects.create(
        post=post,
        user = user,
        created = timezone.now(),
        comment = request.POST.get('comment')
        
    )
    comment.save()
    return redirect('accounts:home')