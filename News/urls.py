# newsletter/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('news/', views.hospital_news, name='hospital_news'),
    path('news/<int:news_id>/', views.news_detail, name='news_detail'),


]
