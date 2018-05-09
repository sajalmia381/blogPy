from django.contrib import admin
from .models import Author,Category, Article, Comment

# Register your models here.
class Model_Author(admin.ModelAdmin):
    list_display = ["__str__"]
    search_fields = ["__str__", "details"]
    class Meta:
        Model=Author
admin.site.register(Author, Model_Author)

class Model_Category(admin.ModelAdmin):
    list_display = ["__str__",]
    search_fields = ["__str__", "name"]
    list_per_page = 10
    list_filter = ["name"]
    class Meta:
        Model = Category
admin.site.register(Category, Model_Category)

class Model_Article(admin.ModelAdmin):
    list_display = ["__str__", "posted_on", "update_on"]
    search_fields = ["__str__", "title"]
    list_per_page = 8
    list_filter = ["posted_on", "category"]
    class Meta:
        Model = Article
admin.site.register(Article, Model_Article)

class Model_Comment(admin.ModelAdmin):
    list_display = ["name", "email", "__str__"]
    list_per_page = 10
    class Meta:
        Model = Comment
admin.site.register(Comment, Model_Comment)