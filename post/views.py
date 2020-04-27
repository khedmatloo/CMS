from django.shortcuts import render
from .serializers import PostSerializer, PostDetailSerializer
from .models import Post
from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status, permissions, request
from rest_framework.pagination import PageNumberPagination
from django.core.paginator import Paginator
from rest_framework.response import Response


class PostWithCategoryFilter(APIView):
    def get(self, request, category, page):
        try:
            posts = Post.objects.filter(category=category)
            paginatedpost = Paginator(posts, 10)
            pageinfo = paginatedpost.page(page)
            serializer = PostSerializer(posts, many=True)
            if serializer.data == []:
                data = {}
                data['response'] = "‍پستی در این دسته بندی وجود ندارد."
                return JsonResponse(data, status=status.HTTP_204_NO_CONTENT)
            else:
                return JsonResponse(serializer.data, safe=False)
        except:
            data = {}
            data['response'] = "صفحه مورد نظر یافت نشد."
            return JsonResponse(data, status=status.HTTP_404_NOT_FOUND)


class PostAPIView(APIView):

    def get(self, request, page):
        try:
            posts = Post.objects.all()
            paginatedpost = Paginator(posts, 10)
            pageinfo = paginatedpost.page(page)
            serializer = PostSerializer(pageinfo, many=True)
            return JsonResponse(serializer.data, safe=False)
        except:
            data = {}
            data['response'] = "صفحه مورد نظر یافت نشد."
            return JsonResponse(data, status=status.HTTP_404_NOT_FOUND)


class PostDetail(APIView):

    def get(self, request, id):
        try:
            posts = Post.objects.filter(
                id=id).select_related('category')
            serializer = PostDetailSerializer(posts, many=True)
            if serializer.data == []:
                data = {}
                data['response'] = "‍پست مورد نظر یافت نشد."
                return JsonResponse(data, status=status.HTTP_404_NOT_FOUND)
            else:
                for post in posts:
                    if post.just_users == True:
                        if request.user.is_anonymous:
                            data = {}
                            data['response'] = "‍تنها کاربران سایت به این مطلب دسترسی دارند."
                            return JsonResponse(data, status=status.HTTP_401_UNAUTHORIZED)
                        else:
                            return JsonResponse(serializer.data, safe=False)
                    else:
                        return JsonResponse(serializer.data, safe=False)
        except:
            data = {}
            data['response'] = "‍پست مورد نظر یافت نشد."
            return JsonResponse(data, status=status.HTTP_404_NOT_FOUND)


class RateOfPost(APIView):

    def get(self, request, id):
        try:
            rate_obj = Post.objects.filter(id=id).values('rate')
            post = Post.objects.get(id=id)
            user = request.user
            data = {}
            data['rate'] = len(rate_obj)
            if user in post.rate.all():
                data['is_liked'] = True
            else:
                data['is_liked'] = False
            return JsonResponse(data, safe=False)
        except:
            return JsonResponse('صفحه مورد نظر یافت نشد.', status=status.HTTP_404_NOT_FOUND, safe=False)

    def post(self, request, id):
        try:
            rate_obj = Post.objects.filter(id=id).values('rate')
            post = Post.objects.get(id=id)
            user = request.user
            data = {}
            data['rate'] = len(rate_obj)
            if user in post.rate.all():
                data['is_liked'] = True
            else:
                data['is_liked'] = False
            if user.is_authenticated:
                if user in post.rate.all():
                    post.rate.remove(user)
                else:
                    post.rate.add(user)
                rate_obj = Post.objects.filter(id=id).values('rate')
                return JsonResponse(data, status=status.HTTP_200_OK, safe=False)
            else:
                return JsonResponse('تنها کاربران سایت قادر به ثبت رای برای مطالب هستند.', status=status.HTTP_404_NOT_FOUND, safe=False)
        except:
            return JsonResponse('صفحه مورد نظر یافت نشد.', status=status.HTTP_404_NOT_FOUND, safe=False)
