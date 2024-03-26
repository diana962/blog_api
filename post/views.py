from rest_framework import generics, permissions
from post.models import Post
from post import serializers

class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.PostCreateSerializer
        return serializers.PostCreateSerializer
