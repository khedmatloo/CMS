from rest_framework import serializers
from .models import CustomUser
from django.contrib import auth
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name']


class SignUpUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True,
                         "error_messages": {"required": "کلمه عبور جهت ثبت نام الزامی است."},
                         },
            "email": {"error_messages": {"unique": ("ایمیل مورد نظر ثبت شده است."),
                                         "required": ("ایمیل جهت ثبت نام الزامی است."),
                                         "invalid": ("ایمیل نامعتبر است.")
                                         }},
            "first_name": {"error_messages": {"required": "نام جهت ثبت نام الزامی است."}},
            "last_name": {"error_messages": {"required": "نام خانوادگی جهت ثبت نام الزامی است."}}
        }

    def save(self):
        user = CustomUser(
            email=self.validated_data['email'],
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
        )
        password = self.validated_data['password']

        user.set_password(password)
        user.save()
        return user


class AuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        label=_("Username"),
        write_only=True,
        error_messages={"blank": ("ایمیل نمی تواند خالی باشد.")}
    )
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True,
        error_messages={"blank": ("رمزعبور نمی تواند خالی باشد.")}
    )
    token = serializers.CharField(
        label=_("Token"),
        read_only=True
    )

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)
            if not user:
                msg = _('ایمیل یا رمز عبور اشتباه است.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('ایمیل یا رمز عبور اشتباه است.')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
