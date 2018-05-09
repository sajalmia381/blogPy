from django.urls import path
from . import views

app_name = "blogapp"
urlpatterns = [
    path('', views.index, name='index'),
    path('profile/<name>', views.profile, name="profile"),
    path('single/<int:id>', views.single, name="single_post"),
    path('topic/<name>', views.topic, name="topic"),
    path('login', views.user_login, name='login'),
    path('logout', views.user_logout, name='logout'),
    path('create_post', views.create_post, name='create_post'),
    path('user', views.user_profile, name='user_profile' ),
    path('update_post/<int:post_id>', views.update_post, name='update_post'),
    path('delete_post/<int:post_id>', views.delete_post, name='delete_post'),
    path('register', views.register, name='register'),
    path('category', views.category, name='category')
]