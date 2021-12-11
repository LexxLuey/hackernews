from rest_framework import serializers
from news.models import HackerNewsItem, Story, PollOption, Poll, Job


class HackerNewsItemSerializer(serializers.ModelSerializer):
    type = serializers.CharField(max_length=200)
    author = serializers.CharField(max_length=200)
    created = serializers.DateField()
    title = serializers.CharField(max_length=500)
    comment_count = serializers.IntegerField()
    score = serializers.IntegerField()
    url = serializers.URLField(max_length=200)

    class Meta:
        model = HackerNewsItem
        fields = '__all__'
