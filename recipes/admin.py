from django.contrib import admin
from .models import Category, Recipe


# regista os models na area de admin, permitindo fazer um crud por ex
class CategoryAdmin(admin.ModelAdmin):
    ...

# tanto com decoradores # noqa
@admin.register(Recipe) # noqa
class RecipeAdmin(admin.ModelAdmin):
    ...

# como dessa forma, a gente ta registrando os models na area de administração
admin.site.register(Category, CategoryAdmin) # noqa
