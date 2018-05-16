from django.shortcuts import render, HttpResponse, get_object_or_404, redirect, Http404
from .models import Author, Category, Article, Comment
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
# Message
from django.contrib import messages

# paginations
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.db.models import Q

from .forms import Create_post, User_creation, Author_user, Single_post_comment, Create_category

# Create your views here.
from django.views import View
class index(View):
    template_name = 'index.html'
    def get(self, request):
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
        return render(request, self.template_name, context)

class profile(View):
    template_name = 'profile.html'
    def get(self, request, name):
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
        return render(request, self.template_name, context)

class single(View):
    template_name = 'single.html'
    def get(self, request, id):
        post = get_object_or_404(Article, pk=id)
        first = Article.objects.first()
        last = Article.objects.last()
        form = Single_post_comment(request.POST or None)
        comments = Comment.objects.filter(post=id)
        related = Article.objects.filter(category=post.category).exclude(id=id)[:4]
        context = {
            "post": post,
            "first": first,
            "last": last,
            "related": related,
            "form": form,
            "comments": comments
        }
        return render(request, self.template_name, context)
    def post(self, request, id):
        post = get_object_or_404(Article, pk=id)
        form = Single_post_comment(request.POST or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.post = post
            instance.save()
        return render(request, self.template_name,{'form': form})


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
  return redirect('blog:index')

def create_post(request):
    if request.user.is_authenticated:
        current_user = get_object_or_404(Author, name=request.user.id)
        form = Create_post(request.POST or None, request.FILES or None )
        if form.is_valid():
            instance = form.save(commit=False)
            instance.article_author = current_user
            instance.save();
            # messages.SUCCESS(request, 'Posted SuccessFull')
            return redirect('blog:index')
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
        return redirect('blog:login')

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
    # category_item = Article.objects.filter(category=)
    return render(request, 'categorys.html', {'post': post})

def create_category(request):
    form = Create_category(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.error(request, "Category Add")
        return redirect('blog:categorys')
    return render(request, 'create_category.html', {'form': form})

def category_delete(request, category_id):
    item = Category.objects.filter(id=category_id)
    item.delete()
    messages.success(request, "Category deleted")
    return redirect('blog:categorys')
def category_update(request, category_id):
    item = get_object_or_404(Category, id=category_id)
    form = Create_category(request.POST or None, instance=item)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return redirect('blog:categorys')
    return render(request, 'create_category.html', {'form': form})
