from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from .models import Category
from .serializers import CategorySerializer
from rest_framework.views import APIView
from rest_framework import status


class CategoryAPIView(APIView):

    def get(self, request, format=None):
        categories = Category.objects.all().order_by('title')
        serializer = CategorySerializer(categories, many=True)
        return JsonResponse(serializer.data, safe=False)


class CategoryDetail(APIView):
    def get(self, request, id):
        try:
            categories = Category.objects.filter(id=id)
            serializer = CategorySerializer(categories, many=True)
            if serializer.data == []:
                data = {}
                data['response'] = "دسته بندی مورد نظر یافت نشد."
                return JsonResponse(data, status=status.HTTP_404_NOT_FOUND)
            else:
                return JsonResponse(serializer.data, safe=False)
        except:
            data = {}
            data['response'] = "دسته بندی مورد نظر یافت نشد."
            return JsonResponse(data, status=status.HTTP_404_NOT_FOUND)


'''
def category_list(request):

    if request.method == 'GET':
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return JsonResponse(serializer.data, safe=False)
'''
