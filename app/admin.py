from django.contrib import admin
from .models import *


class PostAdmin(admin.ModelAdmin):
    list_display = ('author',)
    list_filter = ('created', 'updated')
    search_fields = ('author__username',)
    date_hierarchy = ('created')


class ImagesAdmin(admin.ModelAdmin):
    list_display = ('post', 'image')


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'dob', 'photo')


admin.site.register(Post, PostAdmin)
admin.site.register(Images, ImagesAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Comment)
