

# Create your models here.
# from tkinter import W
from concurrent.futures import thread
from email.mime import image
from urllib import request
from django.db import models
from django.contrib import auth
from django.contrib.auth.models import BaseUserManager
from django.dispatch import receiver
from django.forms import PasswordInput, widgets
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q


# from django.utils.text import slugify

class UserManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError('you must have an email')

        if not username:
            raise ValueError('no username provided')

        user = self.model(
            email = self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
            username = username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, email, username, password):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password,
            first_name = first_name,
            last_name = last_name,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user


    def get_all_profiles_to_invite(self, sender):
        users = User.objects.all().exclude(username=sender.username)
        user = User.objects.get(username=sender.username)
       

        qs = Relationship.objects.filter(Q(sender=user)| Q(receiver=user))
        
        user_profile = UserProfile.objects.get(user=user)
        other_user_profiles = UserProfile.objects.all().exclude(user=user)

        accepted = set([])
        for rel in qs:
            if rel.status == 'accepted':
                user_p = UserProfile.objects.get(user=rel.sender)
                o_user_p = UserProfile.objects.get(user=rel.receiver)
                accepted.add(user_p)
                accepted.add(o_user_p)
        
        available = [userprofile for userprofile in other_user_profiles if userprofile not in accepted]
        return available
    def get_all_sent_invites(self, sender):
        
        users = User.objects.all().exclude(username=sender.username)
        user = User.objects.get(username=sender.username)

        qs = Relationship.objects.filter(sender=user)

        sent = []
        for rel in qs:
            if rel.status =='sent' and rel.status != 'accepted':
                user_p = UserProfile.objects.get(user=rel.receiver)
                sent.append(user_p)
        print(sent)
        return sent
            
                




class User(auth.models.User, auth.models.PermissionsMixin):
    
    friends = models.ManyToManyField(auth.models.User,related_name='friends')
    
    
    objects = UserManager()
    

    def __str__(self):
        return self.first_name


gender_choices = [('M', 'Male'),
                    ('F', 'Female'),
                    ('O', 'Others'),

                
                ]
class UserProfile(models.Model):
    user             = models.OneToOneField(User, on_delete=models.CASCADE, null = True,)
    first_name       = models.CharField(max_length=50, blank=True)
    last_name        = models.CharField(max_length=50, blank=True)
    slug             = models.SlugField(default='test')
    image            = models.ImageField(upload_to='images/', default= 'images/avatar.png')
    
    phone_number     = models.CharField(max_length=50, blank=True)
    
    gender           = models.CharField(max_length=1, choices=gender_choices, blank=True)
    city             = models.CharField(max_length=50, default='New Delhi')
    state            = models.CharField(max_length=50, blank=True)
    country          = models.CharField(max_length=50, blank=True)
    Hobbies          = models.CharField(max_length=50, blank=True)
    Languages        = models.CharField(max_length=50, blank=True)

        

    def __str__(self):
        return self.first_name


class ThreadModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+', null=True)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+', null=True)

class MessageModel(models.Model):
    thread = models.ForeignKey(ThreadModel, on_delete=models.CASCADE, related_name='+')
    sender_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    receiver_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+', null=True)
    body = models.CharField(max_length=100, null=True)
    image = models.ImageField(upload_to='photos/post_images', blank=True, null=True)
    date= models.DateTimeField(default=timezone.now)
    is_read= models.BooleanField(default=False)


STATUS_CHOICES = (
    ('sent', 'sent'),
    ('accepted', 'accepted'),
    ('rejected', 'rejected'),


)

class RelationshipManager(models.Manager):
    def received_invitations(self, receiver):
        qs = Relationship.objects.filter(receiver=receiver, status='sent')
        return qs


class Relationship(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    status = models.CharField(max_length=8, choices=STATUS_CHOICES)

    objects = RelationshipManager()

    def __str__(self):
        return f"{self.sender.first_name}  {self.sender.last_name}"
