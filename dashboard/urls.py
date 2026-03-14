from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    path("", views.dashboard_home, name="dashboard_home"),
    path("post/<int:id>/update/", views.post_update, name="post_update"),
    path("post/<int:id>/delete/", views.post_delete, name="post_delete"),
    path("comment/<int:id>/delete/", views.comment_delete, name="comment_delete"),
    path("category/create/", views.category_create, name="category_create"),
    path("category/<int:id>/update/", views.category_update, name="category_update"),
    path("category/<int:id>/delete/", views.category_delete, name="category_delete"),
]
