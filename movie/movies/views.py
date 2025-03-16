from __future__ import annotations
import django
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import DetailView, ListView

from .forms import ReviewForm
from .models import Movie, Actor


class MoviesView(ListView):
   '''Список фильмов'''
   model = Movie
   queryset = Movie.objects.filter(draft=False)

class MovieDetailView(DetailView):
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
   
class ActorView(DetailView):
   '''Вывод информации об актере'''
   model = Actor
   slug_field = "name"
   def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    print(context)  # Вывод контекста в консоль
    return context
