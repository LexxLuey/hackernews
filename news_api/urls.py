from django.urls import path
from .views import HackerNewsItemSerializerViews

urlpatterns = [
    path('items/<int:id>', HackerNewsItemSerializerViews.as_view(), name="api-item-id"),
    path('items', HackerNewsItemSerializerViews.as_view(), name="api-items"),
]
