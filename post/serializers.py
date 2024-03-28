from rest_framework import serializers
from post.models import Post
from category.models import Category
from comment.serializers import CommentSerializer
from post.models import PostImage

class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = '__all__'

class PostListSerializer(serializers.ModelSerializer):
    owner_username = serializers.ReadOnlyField(source='owner.username')
    category_name = serializers.ReadOnlyField(source='category.name')

    # why nothing appears?

    class Meta:
        model = Post
        fields = ('id', 'title', 'owner', 'owner_username', 'category', 'category_name', 'preview', 'images')



class PostCreateSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(required=True, queryset=Category.objects.all())
    owner = serializers.ReadOnlyField(source='owner.id')
    images = PostImageSerializer(many=True, required=False)
    class Meta:
        model = Post
        fields = ('id', 'title', 'owner', 'category', 'preview', 'images')
    def create(self, validated_data):
        request = self.context.get('request')
        # print(request.FILES, '!!!')
        images = request.FILES.getlist('images')
        post = Post.objects.create(**validated_data)
        image_objects = [PostImage(image=image, post=post) for image in images]
        PostImage.objects.bulk_create(image_objects)
        return post



class PostDetailSerializers(serializers.ModelSerializer):
    owner_username = serializers.ReadOnlyField(source='owner.username')
    category_name = serializers.ReadOnlyField(source='category.name')
    comments = CommentSerializer(many=True, read_only=True)
    comments_count = serializers.ReadOnlyField(source='comments.count')
    images = PostImageSerializer(many=True, required=False)

    class Meta:
        model = Post
        fields = '__all__'



