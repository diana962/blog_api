from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Like
from .serializers import LikeSerializer
# Create your views here.


class LikeCreateView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = LikeSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)