from django.contrib import admin
from post.models import Post
# Register your models here.

# admin.site.register(Post)


@admin.register(Post)
class Posts(admin.ModelAdmin):
    list_display = ('id', 'owner', 'title', 'category')
    # list_display = ('__all__') cant work
#asdasd