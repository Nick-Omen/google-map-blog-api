from django.urls import path
from articles import views

urlpatterns = (
    [
        path('', views.ArticleList.as_view(), name='list'),
        path('<int:pk>/', views.ArticleDetails.as_view(), name='details'),
        path('<int:pk>/images/', views.ArticleImageList.as_view(), name='images'),
        path('<int:pk>/images/<int:image_pk>/', views.ArticleImageDetails.as_view(), name='image'),
    ],
    'articles'
)
