from __future__ import annotations
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import DetailView, ListView

from .forms import ReviewForm
from .models import Movie


class MoviesView(ListView):
   '''Список фильмов'''
   model = Movie
   queryset = Movie.objects.filter(draft=False)
   template_name = "movies/movies_list.html"

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