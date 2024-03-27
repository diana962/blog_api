from django.shortcuts import render
from .models import Comment
from . import serializers
from rest_framework import generics, permissions
from post.permissions import CommentsDeletePermission


class CommentCreateView(generics.CreateAPIView):
    serializer_class = serializers.CommentSerializer
    permission_class = (permissions.IsAuthenticated,)
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class CommentDetailView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    def get_permissions(self):
        if self.request.method == 'DELETE':
            return [CommentsDeletePermission(), ]
        return [permissions.IsAuthenticated(), ]

