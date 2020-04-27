from django.db import models
from category.models import Category
from datetime import datetime
from django.contrib.auth import get_user_model
from user.models import CustomUser
from tinymce.models import HTMLField


class Post(models.Model):
    title = models.CharField(max_length=150)
    summary = models.TextField(blank=True)
    main_image = models.ImageField(
        upload_to='Photos/Posts/%Y/%m/%d/', blank=True)
    rate = models.ManyToManyField(
        CustomUser, blank=True, related_name='post_likes')
    html_post = HTMLField(blank=True,)
    category = models.ForeignKey(
        Category, related_name='posts', on_delete=models.DO_NOTHING)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(blank=True, auto_now_add=True)
    author = models.ForeignKey(
        CustomUser, on_delete=models.DO_NOTHING, related_name='post_written')
    just_users = models.BooleanField()

    def __str__(self):
        return self.title
