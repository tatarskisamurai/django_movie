from __future__ import annotations
import django
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import DetailView, ListView
from django.db.models import Q
from .forms import ReviewForm
from .models import Movie, Actor, Genre


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

class MovieDetailView(GenreYear, DetailView):
   '''Полное описание фильма'''
   model = Movie
   slug_field = "url"

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
    def get_queryset(self):
      years = self.request.GET.getlist("year")
      genres = self.request.GET.getlist("genre")

      queryset = Movie.objects.all()

      if years:
         queryset = queryset.filter(year__in=years)

      if genres:
         queryset = queryset.filter(genres__in=genres)

      return queryset.distinct()