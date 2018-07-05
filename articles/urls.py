from django.urls import path
from articles import views

urlpatterns = (
    [
        path('', views.ArticleList.as_view(), name='list'),
        path('<int:pk>/', views.ArticleDetails.as_view(), name='details'),
    ],
    'articles'
)
