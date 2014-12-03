from django.db import models

from challenge.models import Challenge
from account.models import Account
from tag.models import Tag

class Post(models.Model):
    name = models.CharField(max_length=200)
    content = models.TextField(blank=False)

    github_link = models.URLField(blank=False)
    challenge = models.ForeignKey(Challenge, null=True)
    tag_set = models.ManyToManyField(Tag, blank=True, null=True)

    account = models.ForeignKey(Account)
    created_at = models.DateTimeField(auto_now_add=True)

    liked_account_set = models.ManyToManyField(Account, null=True, related_name="account_set")

    def __unicode__(self):
        return self.name

    def like_count(self):
        return len(liked_account_set)

class Comment(models.Model):
    content = models.TextField(blank=False)

    post = models.ForeignKey(Post, blank=True, null=True)

    creator = models.ForeignKey(Account)
    created_at  = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.content
