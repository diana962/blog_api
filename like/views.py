from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Like
from .serializers import LikeSerializer


# class LikeView(APIView): didn't work
#     def post(self, request, *args, **kwargs):
#         view = LikeCreateView.as_view()
#         return view(request, *args, **kwargs)
#     def delete(self, request, *args, **kwargs):
#         view = LikeDeleteView.as_view()
#         return view(request, *args, **kwargs)
class LikeCreateView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = LikeSerializer
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class LikeDeleteView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated, ]

    def delete(self, request):
        if 'post' not in request.data:
            return Response({'message': 'Field "post" is required'})
        post = request.data.get('post')
        user = request.user
        like = user.likes.filter(post=post)
        if not like.exists():
            return Response({'message': 'You haven\'t liked this post'}, status=400)
        like.delete()
        return Response({'message': 'deleted'}, status=204)
