import datetime
import requests
from .helpers import *
from django.shortcuts import redirect
from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from .models import Story, Job, Poll, PollOption, HackerNewsItem


def about_me(request):
    return render(request,
                  'news/about.html')


class BaseNewsList(ListView):
    paginate_by = 10


class HackerNewsItemList(BaseNewsList):
    model = HackerNewsItem
    context_object_name = 'items'


class HackerNewsItemSearch(BaseNewsList):
    model = HackerNewsItem
    context_object_name = 'items'

    def get_queryset(self):
        if self.request.GET.get('sort'):
            query = self.request.GET.get('sort')
            print("Query sort: ", query)
            return HackerNewsItem.objects.filter(
                Q(type=query)
            )
        elif self.request.GET.get('q'):
            query = self.request.GET.get('q')
            print("Query text: ", query)
            return HackerNewsItem.objects.filter(
                Q(title__icontains=query) | Q(type__icontains=query)
            )


class StoryList(BaseNewsList):
    model = Story
    context_object_name = 'stories'


class StoryDetail(DetailView):
    model = Story

    def get_context_data(self, **kwargs):
        context = super(StoryDetail, self).get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(parent_comment=self.kwargs.get('pk'))
        return context


class StoryCreate(CreateView):
    model = Story
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('stories')


class StoryUpdate(UpdateView):
    model = Story
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('stories')


class StoryDelete(DeleteView):
    model = Story
    context_object_name = 'story'
    success_url = reverse_lazy('stories')


class JobList(BaseNewsList):
    model = Job


class JobDetail(DetailView):
    model = Job


class JobCreate(CreateView):
    model = Job
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('jobs')


class JobUpdate(UpdateView):
    model = Job
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('jobs')


class JobDelete(DeleteView):
    model = Job
    context_object_name = 'job'
    success_url = reverse_lazy('jobs')


class PollList(BaseNewsList):
    model = Poll


class PollDetail(DetailView):
    model = Poll


class PollCreate(CreateView):
    model = Poll
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('polls')


class PollUpdate(UpdateView):
    model = Poll
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('polls')


class PollDelete(DeleteView):
    model = Poll
    context_object_name = 'poll'
    success_url = reverse_lazy('polls')


class PollOptionList(ListView):
    model = PollOption


class PollOptionDetail(DetailView):
    model = PollOption


class PollOptionCreate(CreateView):
    model = PollOption
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('poll_options')


class PollOptionUpdate(UpdateView):
    model = PollOption
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('poll_options')


class PollOptionDelete(DeleteView):
    model = PollOption
    context_object_name = 'poll_option'
    success_url = reverse_lazy('poll_options')
