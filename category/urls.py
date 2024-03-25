from django.urls import path, include
# from category.views import category_list, category_create
from category import views

urlpatterns = [
    path('', views.CategoryCreateListView.as_view()),
    path('<int:pk>/', views.CategoryDetailView.as_view())


    # path('list/', category_list),
    # path('create/', category_create)
]

