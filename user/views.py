from django.shortcuts import render
from .serializers import SignUpUserSerializer, AuthTokenSerializer, CustomUserSerializer
from .models import CustomUser
from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken


class SignUp(APIView):

    def get(self, request):
        return JsonResponse({'response': "Get method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def post(self, request):

        serializer = SignUpUserSerializer(data=request.data)
        email = request.data['email']
        data = {}
        if CustomUser.objects.filter(email=email).count() == 0:
            if serializer.is_valid():
                account = serializer.save()
                data['response'] = "خوش آمدید! ثبت نام شما انجام شد."
                token = Token.objects.get(user=account).key
                data['token'] = token
                return JsonResponse(data, status=status.HTTP_201_CREATED)
            else:
                data = serializer.errors
                return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)
        else:
            data['email'] = ["ایمیل مورد نظر ثبت شده است."]
            return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)


class ObtainAuthTokenOverride(ObtainAuthToken):

    def get(self, request):
        return JsonResponse({'response': "Get method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    serializer_class = AuthTokenSerializer


class UserFirstAndLastName(APIView):
    def get(self, request):
        try:
            print(request.user)
            user = CustomUser.objects.get(email=request.user)
            serializer = CustomUserSerializer(user)
            return JsonResponse(serializer.data, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        except:
            return JsonResponse({'response': 'کاربر وارد نشده است.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
