from email.mime import image
from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User

# Create your models here.

class Comments(models.Model):
    slug = models.SlugField(null = True)
    user = models.CharField(max_length=150)
    comment = models.TextField()

    def __str__(self):
        return f"{self.user}:{self.comment}"

class FavoritePlace(models.Model):
    place_name = models.CharField(max_length=150)
    address = models.CharField(max_length=200)
    image = models.ImageField(upload_to = "posts")
    date = models.DateTimeField(auto_now=True)
    content = models.TextField(validators=[MinLengthValidator(10)])
    slug = models.SlugField(unique=True,db_index = True)
    author = models.ForeignKey(User,related_name="posts",on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.place_name}"


class StoredPosts(models.Model):
    slug = models.SlugField()
    user = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.slug}"

