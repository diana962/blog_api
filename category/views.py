from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from category.models import Category
from category import serializers

from rest_framework import generics, permissions

class CategoryCreateListView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = serializers.CategoryListSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]

class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]






# old Style:
# @api_view(['GET'])
# def category_list(request):
#     queryset = Category.objects.all()
#     serializer = CategoryListSerializer(instance=queryset, many=True)
#     return Response(serializer.data, status=200)
#
# @api_view(['POST'])
# def category_create(request):
#     data = request.data
#     serializer = CategoryListSerializer(data=data)
#     serializer.is_valid(raise_exception=True)
#     serializer.save()
#     return Response(serializer.data, status=201)