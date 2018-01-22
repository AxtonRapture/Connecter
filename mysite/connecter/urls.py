from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('list_of_names', views.list_of_names),
    path('results', views.results),
    path('bookmarks', views.bookmarks),
    path('gender_graphs',views.gender_graphs),
    path('age_graphs', views.age_graphs)
]
