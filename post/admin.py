from django.contrib import admin
from post.models import Post
# Register your models here.

# admin.site.register(Post)


@admin.register(Post)
class Posts(admin.ModelAdmin):
    list_display = ('title', 'category')
