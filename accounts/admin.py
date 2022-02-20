import imp
from django.contrib import admin
from .models import UserProfile,User, ThreadModel, MessageModel, Relationship

# Register your models here.
class UserProfileAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('first_name', 'last_name',)}
admin.site.register(UserProfile,UserProfileAdmin)
admin.site.register(User)

admin.site.register(ThreadModel)
admin.site.register(MessageModel)

admin.site.register(Relationship)
