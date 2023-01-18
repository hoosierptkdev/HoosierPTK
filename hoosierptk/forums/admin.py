from django.contrib import admin
from .models import Profile, Forum, Topic, Post, Comment, Reply

# Register your models here.
admin.site.register(Profile)
admin.site.register(Forum)
admin.site.register(Topic)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Reply)