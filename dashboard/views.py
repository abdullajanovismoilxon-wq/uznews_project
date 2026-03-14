from django.contrib.admin.views.decorators import staff_member_required
from blogapp.models import Post, Comment, Category
from django.shortcuts import render, get_object_or_404, redirect
from blogapp.forms import PostForm, CategoryForm


@staff_member_required
def category_create(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("dashboard:dashboard_home")
    else:
        form = CategoryForm()
    return render(request, "dashboard/category/category_form.html", {"form": form, "title": "Yangi kategoriya qo‘shish"})

@staff_member_required
def category_update(request, id):
    category = get_object_or_404(Category, id=id)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect("dashboard:dashboard_home")
    else:
        form = CategoryForm(instance=category)
    return render(request, "dashboard/category/category_form.html", {"form": form, "title": "Kategoriyani tahrirlash"})

@staff_member_required
def category_delete(request, id):
    category = get_object_or_404(Category, id=id)
    if request.method == "POST":
        category.delete()
        return redirect("dashboard:dashboard_home")
    return render(request, "dashboard/category/category_delete.html", {"category": category})


@staff_member_required
def dashboard_home(request):
    posts = Post.objects.all().order_by("-publish")
    comments = Comment.objects.all().order_by("-created")
    categories = Category.objects.all()
    return render(request, "dashboard/dashboard.html", {
        "posts": posts,
        "comments": comments,
        "categories": categories,
    })

@staff_member_required
def post_update(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect("dashboard:dashboard_home")
    else:
        form = PostForm(instance=post)
    return render(request, "dashboard/post/post_update.html", {"form": form, "post": post})

@staff_member_required
def post_delete(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == "POST":
        post.delete()
        return redirect("dashboard:dashboard_home")
    return render(request, "dashboard/post/post_delete.html", {"post": post})

@staff_member_required
def comment_delete(request, id):
    comment = get_object_or_404(Comment, id=id)
    if request.method == "POST":
        comment.delete()
        return redirect("dashboard:dashboard_home")
    return render(request, "dashboard/comment/comment_delete.html", {"comment": comment})