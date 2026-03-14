from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
# from django.views.generic import ListView
from django.utils.text import slugify
from django.db.models import Q
from django.http import JsonResponse, Http404
from .forms import CommentForm, EmailPostForm, PostForm
from .models import Post, Category


# class PostListView(ListView):
#     queryset = Post.published.all()
#     context_object_name = 'posts'
#     paginate_by = 20
#     template_name = "blogapp/post/list.html"

def category_posts(request, id):
    category = get_object_or_404(Category, id=id)
    posts = Post.objects.filter(category=category, status="published")
    return render(request, "blogapp/post/category_posts.html", {
        "category": category,
        "posts": posts
    })



# Post ro‘yxati (Bosh sahifa)
def post_list(request):
    posts = Post.published.all().order_by('-publish')
    return render(request, "blogapp/post/list.html", {"posts": posts})


# Post tafsiloti
def post_detail(request, id):
    post = get_object_or_404(Post, id=id)

    # Agar published bo‘lsa → hammaga ko‘rinadi
    if post.status == "published":
        pass
    # Agar draft bo‘lsa → faqat muallif yoki admin ko‘ra oladi
    elif post.status == "draft":
        if post.author != request.user and not request.user.is_staff:
            raise Http404("Post topilmadi")

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

    return render(request,
                  'blogapp/post/detail.html',
                  {
                      'post': post,
                      'comments': comments,
                      'new_comment': new_comment,
                      'comment_form': comment_form
                  })


# Yangi post yaratish
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


# Qidiruv
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


# User profil sahifasi
@login_required
def user_profile(request):
    posts = Post.objects.filter(author=request.user).order_by('-publish')
    return render(request, 'blogapp/user/profile.html', {'posts': posts})


