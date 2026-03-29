import os

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
# from django.views.generic import ListView
from django.utils.text import slugify
from django.db.models import Q
from django.http import JsonResponse, Http404

from config import settings
from .forms import CommentForm, PostForm
from .models import Post, Category
from django.core.paginator import Paginator

def category_posts(request, id):
    category = get_object_or_404(Category, id=id)
    posts = Post.objects.filter(category=category, status="published")
    return render(request, "blogapp/post/category_posts.html", {
        "category": category,
        "posts": posts
    })


def post_list(request):
    posts = Post.published.all().order_by('-publish')

    page_number = request.GET.get('page', '1')
    per_page = 9 if page_number == '1' else 3

    paginator = Paginator(posts, per_page)
    page_obj = paginator.get_page(page_number)

    return render(request, 'blogapp/post/list.html', {
        'posts': page_obj.object_list,
        'page_obj': page_obj
    })



def post_detail(request, id=id):
    post = get_object_or_404(Post, id=id)

    # status tekshirish
    if post.status == "published":
        pass
    elif post.status == "draft":
        if post.author != request.user and not request.user.is_staff:
            raise Http404("Post topilmadi")

    # izohlar
    comments = post.comments.filter(active=True)
    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()

    # shu postning kategoriyasiga oid boshqa postlar
    related_posts = Post.objects.filter(
        category=post.category, status="published"
    ).exclude(id=post.id).order_by('-publish')

    # paginator: har safar 3 ta
    page_number = request.GET.get('page', 1)
    paginator = Paginator(related_posts, 3)
    page_obj = paginator.get_page(page_number)

    return render(request,
                  'blogapp/post/detail.html',
                  {
                      'post': post,
                      'comments': comments,
                      'new_comment': new_comment,
                      'comment_form': comment_form,
                      'related_posts': page_obj.object_list,
                      'page_obj': page_obj
                  })


@login_required
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.publish = timezone.now()
            new_post.status = "draft"
            if not new_post.slug:
                new_post.slug = slugify(new_post.title)
            new_post.save()
            return redirect(new_post.get_absolute_url())
    else:
        form = PostForm()
    return render(request, "blogapp/post/create.html", {"form": form})


@login_required
def upload_image(request):
    if request.method == 'POST':
        image = request.FILES.get('file')
        if image:
            # Faylni media/posts/ ichiga saqlash
            image_path = os.path.join('posts', image.name)
            full_path = os.path.join(settings.MEDIA_ROOT, image_path)

            with open(full_path, 'wb+') as destination:
                for chunk in image.chunks():
                    destination.write(chunk)

            return JsonResponse({'location': settings.MEDIA_URL + image_path})
    return JsonResponse({'error': 'Upload failed'}, status=400)


def post_search(request):
    query = request.GET.get("q")
    results = []
    if query:
        results = Post.published.filter(
            Q(title__icontains=query) | Q(body__icontains=query)
        )
    return render(request, "blogapp/post/search.html", {
        "query": query,
        "results": results
    })

def search_suggestions(request):
    query = request.GET.get("q", "")
    suggestions = []
    if query:
        posts = Post.published.filter(
            Q(title__icontains=query) | Q(body__icontains=query)
        )[:5]  # faqat 5 ta natija
        suggestions = [{"id": p.id, "title": p.title} for p in posts]
    return JsonResponse(suggestions, safe=False)


@login_required
def user_profile(request):
    posts = Post.objects.filter(author=request.user).order_by('-publish')
    return render(request, 'blogapp/user/profile.html', {'posts': posts})


@login_required
def user_post_update(request, id):
    post = get_object_or_404(Post, id=id, author=request.user)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect("blogapp:user_profile")
    else:
        form = PostForm(instance=post)
    return render(request, "blogapp/user/post_update.html", {"form": form, "post": post})


@login_required
def user_post_delete(request, id):
    post = get_object_or_404(Post, id=id, author=request.user)
    if request.method == "POST":
        post.delete()
        return redirect("blogapp:user_profile")
    return render(request, "blogapp/user/post_delete.html", {"post": post})