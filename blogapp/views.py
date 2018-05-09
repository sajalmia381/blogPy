from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from .models import Author, Category, Article, Comment
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
# paginations
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from .forms import Create_post, User_creation, Author_user, Single_post_comment
from django.db.models import Q
# Message
from django.contrib import messages


# Create your views here.

def index(request):
  post = Article.objects.all()
  paginator = Paginator(post, 8)
  page = request.GET.get('page')
  total_article = paginator.get_page(page)
  # Search
  search = request.GET.get('searching')
  if search:
      post = post.filter(
          Q(title__icontains=search)
      )
  context = {
    "post": total_article,
  }
  return render(request, 'index.html', context)

def profile(request, name):
  post_author = get_object_or_404(User, username=name)
  auth = get_object_or_404(Author, name=post_author.id)
  post = Article.objects.filter(article_author=auth.id)
  paginator = Paginator(post, 4)
  page = request.GET.get('page')
  total_article = paginator.get_page(page)

  context = {
    'post': total_article,
    'auth': auth,
  }
  return render(request, 'profile.html', context)

def single(request, id):
  post = get_object_or_404(Article, pk=id)
  first = Article.objects.first()
  last = Article.objects.last()
  comments = Comment.objects.filter(post=id)
  related = Article.objects.filter(category=post.category).exclude(id=id)[:4]
  form = Single_post_comment(request.POST or None)
  if form.is_valid():
      instance = form.save(commit=False)
      instance.post = post
      instance.save()
  context = {
    "post": post,
    "first": first,
    "last": last,
    "related": related,
    "form": form,
    "comments": comments
  }
  return render(request, 'single.html', context)

def topic(request, name):
  cat = get_object_or_404(Category, name=name)
  post = Article.objects.filter(category=cat.id)
  return render(request, 'category.html', {"post": post})

def user_login(request):
  if request.user.is_authenticated:
      return redirect(index)
  else:
      if request.POST:
          user = request.POST.get('user')
          password = request.POST.get('pass')
          auth=authenticate(request, username=user, password=password)
          if auth is not None:
              login(request, auth)
              return redirect('blog:index')
          else:
              messages.add_message(request, messages.ERROR, "User and password not correct")
  return render(request, 'login.html')

def user_logout(request):
  logout(request)
  return redirect(index)

def create_post(request):
    if request.user.is_authenticated:
        current_user = get_object_or_404(Author, name=request.user.id)
        form = Create_post(request.POST or None, request.FILES or None )
        if form.is_valid():
            instance = form.save(commit=False)
            instance.article_author = current_user
            instance.save();
            # messages.SUCCESS(request, 'Posted SuccessFull')
            return redirect(index)
        return render(request, 'create_post.html', {'form': form})
    else:
        return redirect('blog:login')

def update_post(request, post_id):
    if request.user.is_authenticated:
        current_author = get_object_or_404(Author, name=request.user.id)
        post = get_object_or_404(Article, id=post_id)
        form = Create_post(request.POST or None, request.POST or None, instance=post)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.article_author=current_author
            instance.save()
            return redirect('blog:user_profile')
        return render(request, 'update_post.html', {'form': form})
    else:
        return redirect('login')

def delete_post(request, post_id):
    if request.user.is_authenticated:
        post = get_object_or_404(Article, id=post_id)
        post.delete()
        return redirect('blog:user_profile')
    else:
        return redirect('blog:login')

def user_profile(request):
    if request.user.is_authenticated:
        user = get_object_or_404(User, id=request.user.id)
        author_profile = Author.objects.filter(name=user.id)
        if author_profile:
            author_user = get_object_or_404(Author, name=request.user.id)
            post = Article.objects.filter(article_author=author_user.id)
            return render(request, 'user.html', {'post': post, 'user': author_user})
        else:
            form = Author_user(request.POST or None, request.FILES or None)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.name = user
                instance.save()
                return redirect('blog:user_profile')
            return render(request, 'new_article_user.html', {'form': form})
    else:
        return redirect('login')

def register(request):
    form = User_creation(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "user successfully created")
        return redirect('blog:login')
    return render(request, 'register.html', {'form': form})

def category(request):
    post = Category.objects.all()
    return render(request, 'categorys.html', {'post': post})