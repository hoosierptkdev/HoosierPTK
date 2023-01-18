from django.urls import path
from .views import Home, Posts, Detail, CreatePost, LatestPosts, SearchResults
from django.views.generic import TemplateView

app_name='forums'

urlpatterns = [
    path('', Home, name='home'),
    path('posts/<slug>/', Posts, name='posts'),
    path('detail/<slug>/', Detail, name='detail'),
    path('create_post', CreatePost, name='create_post'),
    path('latest_posts', LatestPosts, name='latest_posts'),
    path('search', SearchResults, name='search'),
]