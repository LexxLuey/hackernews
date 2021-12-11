from django.urls import path

from .views import StoryList, HackerNewsItemList, StoryDetail, JobDetail, PollDetail, HackerNewsItemSearch, about_me

urlpatterns = [
    path('', HackerNewsItemList.as_view(), name='index'),
    path('stories', StoryList.as_view(), name='stories'),
    path('search/', HackerNewsItemSearch.as_view(), name='search_results'),
    path("stories/<int:pk>", StoryDetail.as_view(), name="story-detail"),
    path("jobs/<int:pk>", JobDetail.as_view(), name="job-detail"),
    path("polls/<int:pk>", PollDetail.as_view(), name="poll-detail"),
    path("about-me", about_me, name="about_me"),
]

