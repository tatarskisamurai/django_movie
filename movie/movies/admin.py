from django.contrib import admin
import django.core.asgi
from django.utils.safestring import mark_safe
from .models import Actor, Category, Genre, Movie, MovieShots, Rating, RatingStar, Reviews

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
   list_display = ('id', 'name', 'url')
   list_display_links = ('name',)

class ReviewInline(admin.TabularInline):
   model = Reviews
   extra = 1
   readonly_fields = ('name', 'email')

class MovieShotsInline(admin.TabularInline):
   model = MovieShots
   extra = 1
   readonly_fields = ("get_image", )

   def get_image(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="100" height="110"/>')
        return "Нет изображения"

   get_image.short_description = 'Изображение'

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
   list_display = ('title', 'category', 'url', 'draft')
   list_filter = ('year', 'category')
   search_fields = ('title', 'category__name')
   inlines = [MovieShotsInline, ReviewInline]
   save_on_top = True
   save_as = True
   readonly_fields = ('get_image',)
   list_editable = ('draft',)
   fieldsets = (
      ("Основная информация", {
         "fields": (('title', 'tagline'),)
      }),
      ("Описание", {
         "fields": (('description', 'poster', 'category', 'get_image'),)
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

   def get_image(self, obj):
        if obj.poster:
            return mark_safe(f'<img src="{obj.poster.url}" width="100" height="110"/>')
        return "Нет изображения"

   get_image.short_description = 'Постер'

@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
   list_display = ('name', 'email', 'text', 'parent', 'movie', 'id')
   readonly_fields = ('name', 'email')

@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'image')
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="50" height="50"/>')
        return "Нет изображения"

    get_image.short_description = 'Изображение'
   

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'url')
    list_display_links = ('name',)
    search_fields = ('name',)
    
@admin.register(MovieShots)
class MovieShotsAdmin(admin.ModelAdmin):
    list_display = ('title', 'movie', 'get_image')
    list_display_links = ('title',)
    search_fields = ('title', 'movie__title')
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="50" height="50"/>')
        return "Нет изображения"

    get_image.short_description = 'Изображение'

@admin.register(RatingStar)
class RatingStarAdmin(admin.ModelAdmin):
    list_display = ('value',)
    list_display_links = ('value',)

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('star', 'movie', 'ip')
    list_display_links = ('star',)
    search_fields = ('movie__title', 'ip')

admin.site.site_title = "Django Movies"
admin.site.site_header = "Django Movies"