import imp
from django.db.models.signals import post_save
from accounts.models import User, UserProfile, Relationship
from django.dispatch import receiver


@receiver(post_save, sender=User)
def post_save_create_profile(sender, instance, created, **kwargs):
    print(sender)
    print(instance)
    if created:
        UserProfile.objects.create(user=instance, first_name=instance)
        print(instance)

@receiver(post_save, sender=Relationship)
def post_save_add_to_friend(sender, instance, created, **kwargs):
        sender_ = instance.sender
        receiver_ = instance.receiver
        if instance.status == 'accepted':
            sender_.friends.add(receiver_)
            receiver_.friends.add(sender_)
            sender_.save()
            receiver_.save()
