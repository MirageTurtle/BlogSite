from django.db import models

# Create your models here.

# import built-in User model
from django.contrib.auth.models import User
# timezone is used for managing time
from django.utils import timezone

# Blog Article


class ArticlePost(models.Model):

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    body = models.TextField()
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    # add view numbers
    total_views = models.PositiveIntegerField(default=0)  # default=0 measn the variable begin with 0

    # inner class Meta is for meta data
    class Meta:

        # ordering指定模型返回的数据排列顺序 -created表示倒序
        # ordering是元组
        ordering = ('-created',)

    def __str__(self):
        return self.title
