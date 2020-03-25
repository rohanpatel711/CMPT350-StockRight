from django.urls import path
from . import views

urlpatterns = [
    path('news.html', views.news, name="news"),
]
