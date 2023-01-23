from django.contrib import admin

# Register your models here.

from .models import Comment, Post


class PostAdmin(admin.ModelAdmin):

    list_display=('title','author_name','pub_date','level','category')

admin.site.register(Post,PostAdmin)

admin.site.register(Comment)
