from django.contrib import admin
from .models import Category, Recipe


# regista os models na area de admin, permitindo fazer um crud por ex
class CategoryAdmin(admin.ModelAdmin):
    ...

# tanto com decoradores # noqa
@admin.register(Recipe) # noqa
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'created_at', 'is_published']
    list_display_links = ['title', 'created_at']
    search_fields = ['id', 'title', 'description', 'slug', 'preparation_steps']
    list_filter = [
        'category', 'author', 'is_published', 'preparation_step'
    ]
    list_per_page = 10
    list_editable = 'is_published',
    ordering = '-id',
    prepopulated_fields = {'slug': ('title',)}

# como dessa forma, a gente ta registrando os models na area de administração
admin.site.register(Category, CategoryAdmin) # noqa
