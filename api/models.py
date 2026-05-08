from django.db import models


class User(models.Model):
    name     = models.CharField(max_length=100)
    username = models.CharField(max_length=50)
    email    = models.EmailField()
    address  = models.JSONField(default=dict)
    phone    = models.CharField(max_length=30)
    website  = models.CharField(max_length=100)
    company  = models.JSONField(default=dict)

    class Meta:
        ordering = ['id']


class Post(models.Model):
    user  = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=200)
    body  = models.TextField()

    class Meta:
        ordering = ['id']


class Comment(models.Model):
    post  = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name  = models.CharField(max_length=200)
    email = models.EmailField()
    body  = models.TextField()

    class Meta:
        ordering = ['id']


class Album(models.Model):
    user  = models.ForeignKey(User, on_delete=models.CASCADE, related_name='albums')
    title = models.CharField(max_length=200)

    class Meta:
        ordering = ['id']


class Photo(models.Model):
    album        = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='photos')
    title        = models.CharField(max_length=255)
    url          = models.URLField(max_length=500)
    thumbnailUrl = models.URLField(max_length=500)

    class Meta:
        ordering = ['id']


class Todo(models.Model):
    user      = models.ForeignKey(User, on_delete=models.CASCADE, related_name='todos')
    title     = models.CharField(max_length=255)
    completed = models.BooleanField(default=False)

    class Meta:
        ordering = ['id']
