from django.contrib import admin
from home.models import Friend
from .models import Create
from .models import Post, Aboutpage, Newsletter

# Register your models here.
#admin.site.register(Comment)

admin.site.register(Post)
admin.site.register(Create)
admin.site.register(Friend)
admin.site.register(Aboutpage)
admin.site.register(Newsletter)