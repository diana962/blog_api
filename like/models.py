from django.db import models
from post.models import Post

class Like(models.Model):
    owner = models.ForeignKey('auth.User', related_name='likes', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.owner.username} --> {self.post.title}'

    class Meta:
        unique_together = ['owner', 'post'] #can't like the same post twice


class Favorite(models.Model):
    owner = models.ForeignKey('auth.User', related_name='favorites', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='favorites', on_delete=models.CASCADE)

    class Meta:
        unique_together = ['owner', 'post']