from django.db import models
# settingsをimport
from django.conf import settings

# timezoneをimport
from django.utils import timezone


class Tag(models.Model):
    name    = models.CharField(verbose_name="タグ名",max_length=10)

    def __str__(self):
        return self.name
    
    def str_id(self):
        return str(self.id)

class Topic(models.Model):
    title   = models.CharField(verbose_name="タイトル",max_length=100)
    comment = models.CharField(verbose_name="コメント",max_length=2000)
    dt      = models.DateTimeField(verbose_name="投稿日時",default=timezone.now)
    user    = models.ForeignKey(settings.AUTH_USER_MODEL,verbose_name="投稿者", on_delete=models.CASCADE)

    tag     = models.ManyToManyField(Tag,verbose_name="タグ",blank=True)

    def __str__(self):
        return self.title