from django.contrib import admin

# modelをインポートする
from .models import Tag,Topic

admin.site.register(Tag)
admin.site.register(Topic)