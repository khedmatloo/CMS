from rest_framework import serializers
from .models import Post
from category.serializers import CategorySerializer
from user.serializers import CustomUserSerializer
from category.models import Category


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'summary', 'rate', 'just_users', 'main_image']


class PostDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    author = CustomUserSerializer()

    class Meta:
        model = Post
        fields = ['id', 'title', 'summary', 'html_post', 'category',
                  'created_at', 'author', 'just_users', 'main_image']


# class RateOfPostSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Post
#         fields = ['rate']
