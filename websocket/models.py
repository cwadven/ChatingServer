from django.db import models


# Create your models here.
class GroupCount(models.Model):
    nickname = models.CharField(max_length=128)
    groupname = models.CharField(max_length=128)
    login_time = models.DateTimeField(db_column='createTime', auto_now_add=True, blank=True, null=True)
