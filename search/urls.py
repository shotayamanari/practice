from django.urls import path
from . import views

app_name    = "search"
              #↑アプリ名称と同じにしておくことを推奨。必ず設定すること。

urlpatterns = [
    path('', views.index, name="index"),
    path('tag/<int:pk>/', views.tag, name="tag"),
]