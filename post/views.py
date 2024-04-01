from rest_framework import generics, permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from post.models import Post
from post import serializers
from post.permissions import IsOwner, IsOwnerOrAdmin


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 3
    page_query_param = 'page'
    page_size_query_param = 'page_size'
    max_page_size = 1000
class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ('title', 'body')
    filterset_fields = ('owner', 'category')
    pagination_class = StandardResultsSetPagination

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.PostListSerializer
        elif self.action in ('create', 'update', 'partial_update'):
            return serializers.PostCreateSerializer
        return serializers.PostDetailSerializers

    def get_permissions(self):
        # only admin or the owner csn delete a post
        if self.action == 'destroy':
            return [IsOwnerOrAdmin(), ]
        # only owner can update a post
        elif self.action in ('update', 'partial_update'):
            return [IsOwner(), ]
        # other users can watch and create posts
        return [permissions.IsAuthenticatedOrReadOnly(), ]



# class PostListCreateView(generics.ListCreateAPIView):
#     queryset = Post.objects.all()
#     permission_classes = (permissions.IsAuthenticated, )
#
#     def get_serializer_class(self):
#         if self.request.method == 'GET':
#             return serializers.PostCreateSerializer
#         return serializers.PostCreateSerializer
#
#     def perform_create(self, serializer):
#         serializer.save(owner=self.request.user)
#
#
# class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Post.objects.all()
#
#     def get_serializer_class(self):
#         if self.request.method in ('PUT', 'PATCH'):
#             return serializers.PostCreateSerializer
#         return serializers.PostDetailSerializers
#
#     def get_permissions(self):
#         if self.request.method in ('PUT', 'PATCH'):
#             return [IsOwner()]
#         elif self.request.method == 'DELETE':
#             return [IsOwnerOrAdmin()]
#         return [permissions.IsAuthenticated()]
