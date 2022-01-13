from django.db import models


# Create your models here.
class GroupCount(models.Model):
    nickname = models.CharField(max_length=128)
    room_type = models.CharField(max_length=128)
    room_detail = models.CharField(max_length=128)
    channel_name = models.CharField(max_length=128)
    join_time = models.DateTimeField(auto_now_add=True)


class GroupChatLog(models.Model):
    nickname = models.CharField(max_length=128)
    content = models.TextField()
    room_type = models.CharField(max_length=128)
    room_detail = models.CharField(max_length=128)
    create_time = models.DateTimeField(auto_now_add=True)
