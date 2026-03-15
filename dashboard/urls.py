from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    path("", views.dashboard_home, name="dashboard_home"),

    path("post/<int:id>/update/", views.post_update, name="post_update"),
    path("post/<int:id>/delete/", views.post_delete, name="post_delete"),
    path("post/<int:id>/toggle-status/", views.post_status, name="post_status"),

    path("comment/<int:id>/delete/", views.comment_delete, name="comment_delete"),

    path("category/create/", views.category_create, name="category_create"),
    path("category/<int:id>/update/", views.category_update, name="category_update"),
    path("category/<int:id>/delete/", views.category_delete, name="category_delete"),

    path("users/", views.user_list, name="user_list"),
    path("users/<int:id>/update/", views.user_update, name="user_update"),
    path("users/<int:id>/delete/", views.user_delete, name="user_delete"),
]
