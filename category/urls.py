from django.urls import path
from .views import CategoryAPIView, CategoryDetail

urlpatterns = [
    path('category_list/', CategoryAPIView.as_view()),
    path('category/<int:id>', CategoryDetail.as_view()),
]
