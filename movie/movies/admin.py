from django.contrib import admin
from .models import Actor, Category, Genre, Movie, MovieShots, Rating, RatingStar, Reviews

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
   list_display = ('id', 'name', 'url')
   list_display_links = ('name',)

class ReviewInline(admin.TabularInline):
   model = Reviews
   extra = 1
   readonly_fields = ('name', 'email')

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
   list_display = ('title', 'category', 'url', 'draft')
   list_filter = ('year', 'category')
   search_fields = ('title', 'category__name')
   inlines = [ReviewInline]
   save_on_top = True
   save_as = True
   list_editable = ('draft',)
   fieldsets = (
      ("Основная информация", {
         "fields": (('title', 'tagline'),)
      }),
      ("Описание", {
         "fields": (('description', 'poster', 'category'),)
      }),
      ("Дата и место", {
         "fields": (('year', 'country', 'world_primiere'),)
      }),
      ("Создатели", {
         "classes": ('collapse',),
         "fields": (('directors', 'actors', 'genres'),)
      }),
      ("Финансы", {
         "fields": (('budget', 'free_in_usa'),)
      }),
      ("Дополнительно", {
         "fields": (('url', 'draft'),)
      }),
   )

@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
   list_display = ('name', 'email', 'text', 'parent', 'movie', 'id')
   readonly_fields = ('name', 'email')

@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ('name', 'age')
    list_display_links = ('name',)
    search_fields = ('name',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'url')
    list_display_links = ('name',)
    search_fields = ('name',)
    
@admin.register(MovieShots)
class MovieShotsAdmin(admin.ModelAdmin):
    list_display = ('title', 'movie')
    list_display_links = ('title',)
    search_fields = ('title', 'movie__title')

@admin.register(RatingStar)
class RatingStarAdmin(admin.ModelAdmin):
    list_display = ('value',)
    list_display_links = ('value',)

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('star', 'movie', 'ip')
    list_display_links = ('star',)
    search_fields = ('movie__title', 'ip')