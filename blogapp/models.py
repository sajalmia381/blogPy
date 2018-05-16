from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

# Create your models here.
class Author(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    author_picture = models.FileField()
    details = models.TextField()
    def __str__(self):
        return self.name.username

class Category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Article(models.Model):
    article_author = models.ForeignKey(Author, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    body = models.TextField()
    image = models.FileField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    posted_on = models.DateTimeField(auto_now=False, auto_now_add=True)
    update_on = models.DateTimeField(auto_now=True, auto_now_add=False)
    def __str__(self):
        return self.title
    class Meta:
        verbose_name = "Blog Article"
        verbose_name_plural = "Articles"

    def single_post_url(self):
        return reverse("blog:single_post", kwargs={"id": self.id } )
    def author_url(self):
        return reverse("blog:profile", kwargs={'name': self.article_author.name.username})
    def topic_url(self):
        return reverse("blog:topic", kwargs={"name": self.category.name})
    def category_url(self):
        return reverse("blog:categorys", kwargs=self.category.name)

class Comment(models.Model):
    post = models.ForeignKey(Article, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    email = models.EmailField()
    post_comment = models.TextField()
    def __str__(self):
        return self.post.id