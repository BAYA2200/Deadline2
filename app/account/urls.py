from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view()),
    path('profile/', views.ProfileListCreateView.as_view()),
    path('profile/<int:pk>/', views.ProfileRetrieveUpdateDeleteView.as_view()),
    path('', include('rest_framework.urls')),
    path('token/', obtain_auth_token),
]
