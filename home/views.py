from django.shortcuts import render, HttpResponse, redirect
from home.models import Contact
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from blog.models import Post
import markdown2
from blog.views import generate_slug


def home(request):
    return render(request, "home/home.html")


def contact(request):
    if request.method == "POST":
        name = request.POST["name"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        content = request.POST["content"]
        if len(name) < 2 or len(email) < 3 or len(phone) < 10 or len(content) < 4:
            messages.error(request, "Please fill the form correctly")
        else:
            contact = Contact(name=name, email=email, phone=phone, content=content)
            contact.save()
            messages.success(request, "Your message has been successfully sent")
    return render(request, "home/contact.html")


def search(request):
    query = request.GET.get("query", "").strip()
    if not query:
        allPosts = Post.objects.none()
    elif len(query) > 78:
        allPosts = Post.objects.none()
    else:
        allPosts = Post.objects.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query) |
            Q(content__icontains=query)
        )
    if allPosts.count() == 0:
        messages.warning(request, "No search results found. Please refine your query.")
    params = {"allPosts": allPosts, "query": query}
    return render(request, "home/search.html", params)


def handleSignUp(request):
    if request.method == "POST":
        # Get the post parameters
        username = request.POST["username"]
        email = request.POST["email"]
        fname = request.POST["fname"]
        lname = request.POST["lname"]
        pass1 = request.POST["pass1"]
        pass2 = request.POST["pass2"]

        # check for errorneous input
        if len(username) >= 50:
            messages.error(request, " Your user name must be under 50 characters")
            return redirect("home")

        if not username.isalnum():
            messages.error(
                request, " User name should only contain letters and numbers"
            )
            return redirect("home")
        
        # Check if username already exists to prevent database IntegrityError
        if User.objects.filter(username=username).exists():
            messages.error(request, " Username already exists! Please choose another username.")
            return redirect("home")

        if pass1 != pass2:
            messages.error(request, " Passwords do not match")
            return redirect("home")

        # Create the user
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, " Your blogverse has been successfully created")
        return redirect("home")

    else:
        return HttpResponse("404 - Not found")


def handeLogin(request):
    if request.method == "POST":
        # Get the post parameters
        loginusername = request.POST["loginusername"]
        loginpassword = request.POST["loginpassword"]
        next_url = request.POST.get("next") or request.GET.get("next")

        user = authenticate(username=loginusername, password=loginpassword)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            if next_url:
                return redirect(next_url)
            return redirect("home")
        else:
            messages.error(request, "Invalid credentials! Please try again")
            if next_url:
                return redirect(f"/login/?next={next_url}")
            return redirect("home")

    return render(request, "home/login.html")


def handelLogout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect("home")


def about(request):
    return render(request, "home/about.html")


@login_required
def editblog(request):
    sno = request.GET.get('sno')
    if not sno:
        messages.error(request, "No blog post specified to edit.")
        return redirect('home')
        
    post = Post.objects.filter(sno=sno).first()
    if not post:
        messages.error(request, "Blog post not found.")
        return redirect('home')
        
    # Check authorization: user must be the author of the post
    if post.author != request.user.username:
        messages.error(request, "You are not authorized to edit this blog post.")
        return redirect('home')
        
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        image = request.FILES.get('file')
        
        if not title or not content:
            if not title:
                messages.error(request, "Please enter the title")
            if not content:
                messages.error(request, "Please give more content about your blog")
        else:
            post.title = title
            post.content = markdown2.markdown(content)
            if image:
                post.file = image
            post.slug = generate_slug(title)
            post.save()
            messages.success(request, "Blog has been successfully updated")
            return redirect("blogPost", slug=post.slug)
            
    context = {'post': post}
    return render(request, "blog/editblog.html", context)
