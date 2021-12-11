from django.db import models


JOB = 'job'
STORY = 'story'
COMMENT = 'comment'
POLL = 'poll'
POLLOPT = 'pollopt'

NEWS_TYPE_CHOICES = (
    (JOB, 'job'),
    (STORY, 'story'),
    (COMMENT, 'comment'),
    (POLL, 'poll'),
    (POLLOPT, 'pollopt'),
)


class Base(models.Model):
    id = models.IntegerField(db_index=True, primary_key=True)
    type = models.CharField(choices=NEWS_TYPE_CHOICES, null=True, max_length=200)
    author = models.CharField(max_length=200, null=True)
    created = models.DateField(null=True)

    class Meta:
        abstract = True


class Story(Base):
    title = models.CharField(max_length=500)
    comment_count = models.IntegerField(null=True)
    score = models.IntegerField(null=True)
    url = models.URLField(max_length=200, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Stories"
        ordering = ['-created']


class Job(Base):
    comment_count = models.IntegerField(null=True)
    url = models.URLField(max_length=200, null=True)
    content = models.TextField(null=True)
    title = models.CharField(max_length=500)
    score = models.IntegerField(null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created']


class Poll(Base):
    comment_count = models.IntegerField(null=True)
    url = models.URLField(max_length=200, null=True)
    content = models.TextField(null=True)
    title = models.CharField(max_length=500)
    score = models.IntegerField(null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created']


class PollOption(Base):
    comment_count = models.IntegerField(null=True)
    url = models.URLField(max_length=200, null=True)
    poll = models.ForeignKey(Poll,
                             related_name='poll_options',
                             null=True,
                             on_delete=models.CASCADE)
    score = models.IntegerField(null=True)

    def __str__(self):
        return "Poll Options"

    class Meta:
        ordering = ['-created']


class Comment(Base):
    story = models.ForeignKey(Story,
                              related_name='comments',
                              null=True,
                              on_delete=models.CASCADE)
    job = models.ForeignKey(Job,
                            related_name='comments',
                            null=True,
                            on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll,
                             related_name='comments',
                             null=True,
                             on_delete=models.CASCADE)
    poll_option = models.ForeignKey(PollOption,
                                    related_name='comments',
                                    null=True,
                                    on_delete=models.CASCADE)
    comment_count = models.IntegerField(null=True)
    parent_comment = models.IntegerField(null=True)
    content = models.TextField(null=True)

    def __str__(self):
        return self.content

    class Meta:
        ordering = ['-created']


class HackerNewsItem(models.Model):
    id = models.IntegerField(db_index=True, primary_key=True)
    type = models.CharField(choices=NEWS_TYPE_CHOICES, null=True, max_length=200)
    author = models.CharField(max_length=200, null=True, blank=True)
    created = models.DateField(null=True, blank=True)
    title = models.CharField(max_length=500, null=True, blank=True)
    comment_count = models.IntegerField(null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    score = models.IntegerField(null=True, blank=True)
    url = models.URLField(max_length=200, null=True, blank=True)

    poll = models.ForeignKey(Poll,
                             related_name='item_polls',
                             null=True, blank=True,
                             on_delete=models.CASCADE)
    parent_comment_id = models.IntegerField(null=True, blank=True)
    story = models.ForeignKey(Story,
                              related_name='item_story',
                              null=True, blank=True,
                              on_delete=models.CASCADE)
    job = models.ForeignKey(Job,
                            related_name='item_jobs',
                            null=True, blank=True,
                            on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment,
                                related_name='item_comments',
                                null=True, blank=True,
                                on_delete=models.CASCADE)
    poll_option = models.ForeignKey(PollOption,
                                    related_name='item_poll_options',
                                    null=True, blank=True,
                                    on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created']
