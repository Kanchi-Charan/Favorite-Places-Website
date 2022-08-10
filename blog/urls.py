from django.urls import path
from . import views

urlpatterns = [
    path('',views.StartingPage.as_view(),name="starting-page"),
    path('register',views.RegisterView.as_view(),name = "register"),
    path('login',views.LoginView.as_view(),name = "login"),
    path('logout', views.LogoutView,name='logout'),
    path('create',views.CreateView.as_view(),name = 'create'),
    path('all-users',views.UsersView.as_view(),name = "all-users"),
    path('posts/<slug:slug>',views.PostDetail.as_view(),name = "post-detail"),
    path('my_posts',views.MyPostsView.as_view(),name = "my-posts"),
    path('all_posts',views.AllPostsView.as_view(),name = "all-posts"),
    path('stored_posts',views.StoredPostsView.as_view(),name = "read-later"),
]
