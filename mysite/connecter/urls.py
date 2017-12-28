from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('show_user', views.show_user),
    path('get_fb', views.get_fb)
]
