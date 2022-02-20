from distutils.command.upload import upload

from django.db import models
from accounts.models import User
from accounts.models import UserProfile

# Create your models here.


class Post(models.Model):

    user = models.ForeignKey(User, related_name='posts', on_delete= models.CASCADE)
    userprofile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True)
    images = models.ImageField(upload_to='images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    message = models.CharField(max_length=1000)
    likes = models.ManyToManyField(User,related_name='likes')

    
    def total_likes(self):
        return self.likes.count()

    def unlike(self):
        return self.likes.count() -1

    def __str__(self):
        return self.message


    # def get_absolute_url(self):
    #     return reverse('posts:single', kwargs={'username':self.user.username, 'pk':self.pk})

    class Meta:
        ordering = ['-created_at']
        unique_together = ['user', 'message']


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=1000, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
