from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.PostListCreateView.as_view()),
    # path('<int:pk>/', views.PostListCreateView.as_view())
]