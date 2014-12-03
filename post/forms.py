#-*- coding: utf-8 -*-
from django import forms
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget

from .models import Post, Comment
from challenge.models import Challenge
from account.models import Account
from tag.models import Tag

class PostForm(forms.ModelForm):
    name = forms.CharField(label="Post name")
    github_link = forms.CharField(label="Github link", widget=forms.TextInput(attrs={'size' : 80}), initial="http://github.com/", required=True)
    content = forms.CharField(widget=SummernoteWidget(), help_text='사진은 드래그 앤 드롭으로 첨부 가능합니다 :)')
    
    class Meta:
        model = Post
        fields = ['name', 'github_link', 'content', ]

    def __init__(self, user=None, challenge_id=None, post_id=None, *args, **kwargs):
        self._user = user

        if challenge_id:
            self._challenge = Challenge.objects.get(id=challenge_id)

        if post_id:
            self._post = Post.objects.get(id=post_id)

        super(PostForm, self).__init__(*args, **kwargs)

    def is_valid(self):
        form = super(PostForm, self).is_valid()

        return form

    def save(self, commit=True):
        try:
            self._post.name = self.cleaned_data["name"]
            self._post.content = self.cleaned_data["content"]

            #self._post.tag_set.all().delete()
            #for tag in self.cleaned_data["tag_set"]:
            #    self._post.tag_set.add(tag)

            self._post.save()

            return self._post
        except:
            pass

        if not self._user:
            return None

        post = Post(name = self.cleaned_data["name"],
                    content = self.cleaned_data["content"],
                    github_link = self.cleaned_data["github_link"],
                    account = Account.objects.get(user=self._user))
        post.save()

        #for tag in self.cleaned_data["tag_set"]:
        #    post.tag_set.add(tag)

        post.save()

        try:
            self._challenge.post_set.add(post)
        except:
            pass

        #if commit:
        #    group.save()

        return post


class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'width': '100%', 'cols': 80, 'rows': 5}))
    
    class Meta:
        model = Post
        fields = ['content']

    def __init__(self, user=None, post_id=None, *args, **kwargs):
        self._user = user
        self._post = Post.objects.get(id=post_id)
        super(CommentForm, self).__init__(*args, **kwargs)

    def is_valid(self):
        form = super(CommentForm, self).is_valid()
        return form

    def save(self, commit=True):
        if not self._user:
            return None

        comment = Comment(content = self.cleaned_data["content"].replace('\r\n','<br />'),
                          account = Account.objects.get(user=self._user))
        comment.save()

        self._post.comment_set.add(comment)

        #if commit:
        #    group.save()

        return comment
