from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("postComment", views.postComment, name="postComment"),
    path("", views.blogHome, name="bloghome"),
    path("createblog", views.create_blog, name='createblog'),
    path("<str:slug>", views.blogPost, name="blogPost"),
    # path("viewprofile", views.viewprofile, name="viewprofile"),
]
