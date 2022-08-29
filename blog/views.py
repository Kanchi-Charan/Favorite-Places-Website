from ast import Try
from asyncio.windows_events import NULL
from django.shortcuts import redirect, render
from django.views.generic import ListView,CreateView
from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.utils.text import slugify

from .models import Comments, FavoritePlace,StoredPosts,ProfilePic
from .forms import CommentsForm, ProfilepicForm, RegisterForm,LoginForm,PostsForm
# Create your views here.

def StartingPage(request):
    posts = FavoritePlace.objects.all().order_by("-date")[:3]
    try:
        profilepic = ProfilePic.objects.get(user = request.user)
    except:
        profilepic = NULL
    return render (request,"blog/index.html",{
        "posts":posts,
        "profilepic":profilepic,
    })



#class StartingPage(ListView):
#   model = FavoritePlace
#    template_name = "blog/index.html"
#    ordering = ["-date"]
#    context_object_name = "posts"
#
#    def get_queryset(self):
#        queryset = super().get_queryset()
#        data = queryset[:3]
#        return data

#    def get_context_data(request ,self, **kwargs):
#        context = super().get_context_data(**kwargs)
#        profilepic = ProfilePic.objects.get(user = request.user.id)
#        context["profilepic"] = profilepic
#        return context
    

class RegisterView(View):
    def get(self,request):
        form = RegisterForm()
        return render(request,"blog/register.html",{
            "form":form,
        })

    def post(self,request):
        form = RegisterForm(request.POST)
        if (form.is_valid()):
            username = form.cleaned_data["username"]
            firstname = form.cleaned_data["first_name"]
            lastname = form.cleaned_data["last_name"]
            emailid = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            password1=form.cleaned_data["password1"]

            if User.objects.filter(username=username).exists():
                return render(request,"blog/register.html",{
                    "form":form,
                    "message":"User name already exists please choose another username."
                })

            if(password!=password1):
                return render(request,"blog/register.html",{
                    "form":form,
                    "message":"Password doesn't matches."
                })

            user = User.objects.create_user(username=username,first_name=firstname,last_name=lastname,email=emailid,password=password)
            user.save()
            return HttpResponseRedirect(reverse("login"))

        return render(request,"blog/register.html",{
            "form":form,
        })
        

class LoginView(View):
    def get(self,request):
        context = LoginForm
        return render(request,"blog/login.html",{
            "form":context,
        })

    def post(self,request):
        form = LoginForm(request.POST)
        if (form.is_valid()):
            user_name = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = authenticate(username = user_name,password=password)
            if user:
                login(request,user)
                return redirect('starting-page')

            else:
                return render(request,"blog/login.html",{
                    "form":form,
                    "message":"Invalid credentials",
                })

        return render(request,"blog/login.html",{
                    "form":form,
                })

def LogoutView(request):
    logout(request)
    return redirect("starting-page")


class CreateView(View):
    def get(self,request):
        form = PostsForm
        return render(request,"blog/create.html",{
            "form":form,
        })
        

    def post(self,request):
        form = PostsForm(request.POST,request.FILES)
        if (form.is_valid()):
            place_name = form.cleaned_data["place_name"]
            address = form.cleaned_data["address"]
            content = form.cleaned_data["content"]
            image = form.cleaned_data["image"]
            slug = slugify(form.cleaned_data["slug"])

            if FavoritePlace.objects.filter(slug=slug).exists():
                return render(request,"blog/create.html",{
                    "form" : form,
                    "message" : "Slug already taken."
                })
            post = FavoritePlace.objects.create(place_name=place_name,address=address,image=image,content = content,slug = slug,author=request.user)
            post.save()
            return HttpResponseRedirect(reverse("starting-page"))

        return render(request,"blog/create.html",{
            "form":form,
        })
            


class UsersView(ListView):
    model = User
    template_name = "blog/all-users.html"
    context_object_name = "users"



class PostDetail(View):
    def get(self,request,slug):
        post = FavoritePlace.objects.get(slug=slug)
        stored_post = StoredPosts.objects.filter(slug = slug)
        form = CommentsForm()
        comments = Comments.objects.filter(slug = slug)
        return render(request,"blog/post-detail.html",{
            "post" : post,
            "stored_post":stored_post,
            "form":form,
            "comments":comments,
        })

    def post(self,request,slug):
        comment = CommentsForm(request.POST)
        user = request.POST["user"]
        if comment.is_valid():
            comment1 = Comments.objects.create(slug = slug,user = user,comment = comment.cleaned_data['comment'])
            comment1.save()
        
        return HttpResponseRedirect(reverse("post-detail" ,args=[slug]))




class MyPostsView(ListView):
    model = FavoritePlace
    template_name = "blog/my-posts.html"
    context_object_name = "my_posts"
    

    def get_queryset(self):
        posts = super().get_queryset()
        current_user = self.request.user
        myposts = []
        for post in posts:
            if post.author == current_user:
                myposts.append(post)
        return myposts

class AllPostsView(ListView):
    model = FavoritePlace
    template_name = "blog/all-posts.html"
    context_object_name = "all_posts"
    ordering = ["date"]


class StoredPostsView(View):
    def get(self,request):
        all_posts = FavoritePlace.objects.all()
        user = request.user
        storedposts = StoredPosts.objects.all()
        storedposts = storedposts.filter(user = user.username)
        posts = []
        for post in storedposts:
            post1 = all_posts.get(slug = post.slug)
            posts.append(post1)
        return render(request,"blog/read-later.html",{
            "posts":posts,
        })


    def post(self,request):
        slug = request.POST["post_slug"]
        stored_post = StoredPosts.objects.filter(slug=slug)
        if stored_post:
            stored_post.delete()
        else:
            post = StoredPosts.objects.create(slug = slug,user = request.user.username)
            post.save()
        return redirect("read-later")

        
class ProfilePicView(View):
    def get(self,request):
        form = ProfilepicForm
        return render(request,"blog/profile-pic.html",{
            "form":form,
        })

    def post(self,request):
        form = ProfilepicForm(request.POST,request.FILES)
        if(form.is_valid()):
            image1 = form.cleaned_data["profile_pic"]
            try:
                profile1 = ProfilePic.objects.get(user = request.user).delete()
            except:
                profile1 = NULL
            profile = ProfilePic.objects.create(profile_pic = image1,user = request.user)
            profile.save()
            return redirect("starting-page")
        return render(request,"blog/profile-pic.html",{
            "form":form,
        })


class UserPageView(View):
    def get(self,request,slug):
        user1 = User.objects.get(username = slug)
        try:
            profilepic = ProfilePic.objects.get(user = user1)
        except:
            profilepic = NULL
        user = User.objects.get(username = slug)
        posts = FavoritePlace.objects.filter(author = user)
        return render(request,"blog/user-page.html",{
            "user1" : user,
            "profilepic":profilepic,
            "posts":posts,
        })

