from __future__ import annotations
import django
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import DetailView, ListView
from django.db.models import Q
from .forms import RatingForm, ReviewForm
from .models import Movie, Actor, Genre, Rating
from django.http import JsonResponse

class GenreYear:
   '''Жанры и года выхода фильмов'''
   def get_genres(self):
      return Genre.objects.all()
   
   def get_years(self):
      return Movie.objects.filter(draft=True).values('year')

class MoviesView(GenreYear, ListView):
   '''Список фильмов'''
   model = Movie
   queryset = Movie.objects.filter(draft=True)
   paginate_by = 1

class MovieDetailView(GenreYear, DetailView):
    '''Полное описание фильма'''
    model = Movie
    slug_field = "url"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Получаем IP-адрес пользователя
        ip = self.request.META.get('REMOTE_ADDR')
        
        # Ищем рейтинг для этого фильма и IP
        user_rating = Rating.objects.filter(
            movie=self.object,  # Текущий фильм
            ip=ip
        ).first()
        
        # Создаём форму с начальными данными
        initial_data = {'star': user_rating.star.id} if user_rating else {}
        context['star_form'] = RatingForm(initial=initial_data)
        
        return context

class AddReview(View):
   '''Отзывы'''
   def post(self, request, pk):
      form = ReviewForm(request.POST)
      movie = Movie.objects.get(id=pk)
      if form.is_valid():
         form = form.save(commit=False)
         if request.POST.get('parent', None):
            form.parent_id = int(request.POST.get('parent'))
         form.movie = movie
         form.save()
      print(request.POST)
      return redirect(movie.get_absolute_url())
   
class ActorView(GenreYear, DetailView):
   '''Вывод информации об актере'''
   model = Actor
   slug_field = "name"
   def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    print(context)  # Вывод контекста в консоль
    return context

class FilterMoviesView(GenreYear, ListView):
    """Фильтр фильмов"""
    paginate_by = 1

    def get_queryset(self):
        queryset = Movie.objects.filter(
            Q(year__in=self.request.GET.getlist("year")) |
            Q(genres__in=self.request.GET.getlist("genre"))
        ).distinct()
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["year"] = ''.join([f"year={x}&" for x in self.request.GET.getlist("year")])
        context["genre"] = ''.join([f"genre={x}&" for x in self.request.GET.getlist("genre")])
        return context




    
class JsonFilterMoviesView(ListView):
    """Фильтр фильмов в json"""

    def get_queryset(self):
        queryset = Movie.objects.filter(
            Q(year__in=self.request.GET.getlist("year")) |
            Q(genres__in=self.request.GET.getlist("genre"))
        ).distinct().values("title", "tagline", "url", "poster")
        return queryset

    def get(self, request, *args, **kwargs):
        queryset = list(self.get_queryset())
        return JsonResponse({"movies": queryset}, safe=False)

    
class AddStarRating(View):
    """Добавление рейтинга фильму"""
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def post(self, request):
        form = RatingForm(request.POST)
        if form.is_valid():
            Rating.objects.update_or_create(
                ip=self.get_client_ip(request),
                movie_id=int(request.POST.get("movie")),
                defaults={'star_id': int(request.POST.get("star"))}
            )
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)
        
class Search(ListView):
    """Поиск фильмов"""
    paginate_by = 1

    def get_queryset(self):
        return Movie.objects.filter(title__iregex=self.request.GET.get("q"))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["q"] = f'q={self.request.GET.get("q")}&'
        return context