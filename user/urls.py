from django.urls import path
from .views import SignUp, ObtainAuthTokenOverride, UserFirstAndLastName


urlpatterns = [
    path('signup', SignUp.as_view()),
    path('login', ObtainAuthTokenOverride.as_view()),
    path('info', UserFirstAndLastName.as_view()),
]
