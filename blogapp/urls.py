from django.urls import path
from . import views

app_name = "blogapp"
urlpatterns = [
    path('', views.index.as_view(), name='index'),
    path('profile/<name>', views.profile.as_view(), name="profile"),
    path('single/<int:id>', views.single.as_view(), name="single_post"),
    path('topic/<name>', views.topic, name="topic"),
    path('login', views.user_login, name='login'),
    path('logout', views.user_logout, name='logout'),
    path('create_post', views.create_post, name='create_post'),
    path('user', views.user_profile, name='user_profile' ),
    path('update_post/<int:post_id>', views.update_post, name='update_post'),
    path('delete_post/<int:post_id>', views.delete_post, name='delete_post'),
    path('register', views.register, name='register'),
    path('categorys', views.category, name='categorys'),
    path('create_category', views.create_category, name='create_category'),
    path('category_delete/<int:category_id>', views.category_delete, name='category_delete'),
    path('category_update/<int:category_id>', views.category_update, name='category_update')
]