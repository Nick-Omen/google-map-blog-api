from django.urls import path
from places import views

urlpatterns = (
    [
        path('', views.PlaceList.as_view(), name='list'),
        path('<int:pk>/', views.PlaceDetails.as_view(), name='details'),
    ],
    'places'
)
