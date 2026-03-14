from django.urls import path
from . import views

app_name = 'blogapp'

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:id>/', views.post_detail, name='post_detail'),
    path('post/create/', views.post_create, name='post_create'),
    path('post/search/', views.post_search, name='post_search'),
    path('user/profile/', views.user_profile, name='user_profile'),
    path('category/<int:id>/', views.category_posts, name='category_posts'),
    path("search/", views.post_search, name="post_search"),
    path("search_suggestions/", views.search_suggestions, name="search_suggestions"),
]

