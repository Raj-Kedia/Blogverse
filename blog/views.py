import re
from django.shortcuts import render, HttpResponse, redirect
from blog.models import Post, BlogComment
from django.contrib import messages
from django.contrib.auth.models import User
from blog.templatetags import extras
import markdown2
from blog.models import *


def blogHome(request):
    allPosts = Post.objects.all()
    context = {'allPosts': allPosts}
    return render(request, "blog/blogHome.html", context)


def blogPost(request, slug):
    post = Post.objects.filter(slug=slug).first()
    comments = None
    replyDict = {}
    if post:
        post.views = post.views + 1
        post.save()
        comments = BlogComment.objects.filter(post=post, parent=None)
        replies = BlogComment.objects.filter(post=post).exclude(parent=None)
        replyDict = {}
        for reply in replies:
            if reply.parent.sno not in replyDict.keys():
                replyDict[reply.parent.sno] = [reply]
            else:
                replyDict[reply.parent.sno].append(reply)

    context = {'post': post, 'comments': comments,
               'user': request.user, 'replyDict': replyDict}
    return render(request, "blog/blogPost.html", context)


def postComment(request):
    if request.method == "POST":
        comment = request.POST.get('comment')
        user = request.user
        postSno = request.POST.get('postSno')
        post = Post.objects.get(sno=postSno)
        parentSno = request.POST.get('parentSno')
        if parentSno == "":
            comment = BlogComment(comment=comment, user=user, post=post)
            comment.save()
            messages.success(
                request, "Your comment has been posted successfully")
        else:
            parent = BlogComment.objects.get(sno=parentSno)
            comment = BlogComment(
                comment=comment, user=user, post=post, parent=parent)
            comment.save()
            messages.success(
                request, "Your reply has been posted successfully")

    return redirect(f"/blog/{post.slug}")


def generate_slug(title):
    slug = re.sub(r'\s+', '+', title)
    return slug


def create_blog(request):
    # return render(request, 'blog/createblog.html')
    print('in the create blog')
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        # Assuming you're getting the username from the form
        author_username = request.POST.get('author')
        # Get the user object based on the username
        author = User.objects.filter(username=author_username).first()
        # file = request.FILES.get('file')
        image = request.FILES.get('image')
        html_content = markdown2.markdown(content)
        # created_at = models.DateTimeField(auto_now_add=True)
        if not title:
            messages.error(request, "Please enter the title")
        if not content:
            messages.error(request, "Please give more content about your blog")
        else:
            # Generate the slug
            slug = generate_slug(title)

            post = Post(title=title, content=html_content, author=author_username,
                        file=image, slug=slug)
            post.save()
            messages.success(request, "Blog has been successfully created")

    return render(request, 'blog/createblog.html')
