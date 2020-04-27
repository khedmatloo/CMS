from django.urls import path
from .views import PostWithCategoryFilter, PostAPIView, PostDetail, RateOfPost


urlpatterns = [
    path('post_list/category/<int:category>/page/<int:page>',
         PostWithCategoryFilter.as_view()),
    path('post_list/page/<int:page>', PostAPIView.as_view()),
    path('post/<int:id>', PostDetail.as_view()),
    path('post/rate/<int:id>', RateOfPost.as_view()),

]
