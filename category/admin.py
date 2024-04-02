from django.contrib import admin
from category.models import Category

# admin.site.register(Category)

@admin.register(Category)
class Categ(admin.ModelAdmin):
    list_display = ('name', 'count', 'parent')

    def count(self, obj):
        return f'{obj.posts.count()}' #-> мы в category.models.py не создаем переменную post, \
        # так как в post.models.py он уже связан с ним в переменной category