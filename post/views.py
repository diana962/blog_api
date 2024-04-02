from rest_framework import generics, permissions
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from comment.serializers import CommentSerializer
from like.models import Favorite
from like.serializers import LikeUserSerializer
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

    @action(['GET'], detail=True)
    def comments(self, request, pk):
        # post = Post.objects.get(pk=pk)
        post = self.get_object()
        comments = post.comments.all()
        serializer = CommentSerializer(instance=comments, many=True)
        return Response(serializer.data, status=200)

    @action(['GET'], detail=True)
    def likes(self, request, pk):
        post = self.get_object()
        likes = post.likes.all()
        serializer = LikeUserSerializer(instance=likes, many=True)
        return Response(serializer.data, status=200)

    @action(['POST', 'DELETE'], detail=True)
    def favorites(self, request, pk):
        post = self.get_object()
        user = request.user
        favorite = user.favorites.filter(post=post)

        if request.method == 'POST':
            if favorite.exists():
                return Response({'message': 'already in Favorites'}, status=400)
            Favorite.objects.create(owner=user, post=post)
            return Response({'message': 'created in Favorites'}, status=201)

        if favorite.exists():
            favorite.delete()
            return Response({'message': 'deleted'}, status=204)
        return Response({'message': 'Post not found in Favorites!'})


        # if favorite.exists():
        #     favorite.delete()
        #     return Response({'message': 'deleted'}, status=204)
        # else:
        #     favorite = Favorite(owner=user, post=post)
        #     favorite.save()
        #     return Response({'message': 'created'}, status=201)


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
