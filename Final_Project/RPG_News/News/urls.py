from django.urls import path, include
from django.contrib import admin
from .views import *
urlpatterns = [
    path('news/', NewsList.as_view(), name='post_list'),
    path('author_now/', author_now, name='author_now'),
    path('news/<int:pk>/', NewsDetail.as_view(), name='post'),
    path('news/create/', NewsCreate.as_view(), name='post_create'),
    path('news/<int:pk>/edit/', NewsUpload.as_view(), name='post_edit'),
    path('news/<int:pk>/delete/', NewsDelete.as_view(), name='post_delete'),
]