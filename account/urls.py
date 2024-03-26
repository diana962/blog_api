from django.urls import path, include
# from dj_rest_auth import LoginView, LogoutView
from . import views
from dj_rest_auth.views import LoginView, LogoutView

urlpatterns = [
    path('register/', views.UserRegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('', views.UserListView.as_view()),
    path('<int:pk>/', views.UserDetailView.as_view())
]