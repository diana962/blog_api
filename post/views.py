from rest_framework import generics, permissions
from post.models import Post
from post import serializers
from post.permissions import IsOwner, IsOwnerOrAdmin


class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.PostCreateSerializer
        return serializers.PostCreateSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()

    def get_serializer_class(self):
        if self.request.method in ('PUT', 'PATCH'):
            return serializers.PostCreateSerializer
        return serializers.PostDetailSerializers

    def get_permissions(self):
        if self.request.method in ('PUT', 'PATCH'):
            return [IsOwner()]
        elif self.request.method == 'DELETE':
            return [IsOwnerOrAdmin()]
        return [permissions.IsAuthenticated()]
