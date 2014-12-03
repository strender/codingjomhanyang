from django.shortcuts import render, redirect, render_to_response, RequestContext, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from .forms import PostForm, CommentForm
from .models import Post, Comment
from challenge.models import Challenge
from core.views import home

import sys
from utils.func import *

########################
# View post
########################

@login_required
def view_post(request, post_id, challenge_id=None):
    form = CommentForm(data=request.POST or None, user=request.user, post_id=post_id)

    context = RequestContext(request)
    template = 'post/view_post.html'

    current_account = get_account_from_user(request.user)

    try:
        post = Post.objects.get(id=post_id)

        for comment in post.comment_set.all():
            comment.content = comment.content.replace('\r\n','<br />')

        return render(request, template, {'form': form, 'post': post, 'challenge_id': post.challenge.id, 'user': request.user})

    except:
        for e in sys.exc_info():
            print e
        return HttpResponseRedirect(reverse('core:home'))


########################
# Create comment
########################

@login_required
def create_comment(request, post_id, challenge_id=None):
    form = CommentForm(data=request.POST or None, user=request.user, post_id=post_id)
    context = RequestContext(request)

    if request.method == "POST":
        if form.is_valid():
            comment = form.save(commit=False)
            comment.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

########################
# Delete comment
########################

@login_required
def delete_comment(request, challenge_id=None, comment_id=None, post_id=None):
    comment = Comment.objects.get(id=comment_id)
    comment.delete()

    if study_group_id == '0':
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
    else:
        return HttpResponseRedirect(reverse('view_post', kwargs={'challenge_id': challenge_id, 'post_id': post_id, }))

########################
# Create post
########################

@login_required
def create_post(request, challenge_id=None):
    form = PostForm(data=request.POST or None, user=request.user, challenge_id=challenge_id)

    context = RequestContext(request)
    template = 'core/create_post.html'

    if request.method == "POST":
        if form.is_valid():
            post = form.save(commit=False)
            post.save()

            return HttpResponseRedirect(reverse('core:home', args=(challenge_id)))
        else:
            return create_post_view(request, challenge_id)

    return create_post_view(request, challenge_id)

@login_required
def create_post_view(request, challenge_id):
    form = PostForm(data=request.POST or None, user=request.user, challenge_id=challenge_id)
    template = 'post/create_post.html'

    challenge = Challenge.objects.get(id=challenge_id)

    return render(request, template, {'form': form, 'challenge_id': challenge_id, 'current_challenge': challenge, })

########################
# Edit post
########################

@login_required
def edit_post(request, challenge_id=None, post_id=None):
    instance = Post.objects.get(id=post_id)
    form = PostForm(data=request.POST or None, user=request.user, instance=instance, post_id=post_id)

    context = RequestContext(request)
    template = 'core/create_post.html'

    if request.method == "POST":
        if form.is_valid():
            post = form.save()

            return HttpResponseRedirect(reverse('core:home', args=(challenge_id)))
        else:
            return edit_post_view(request, challenge_id, post_id)

    return edit_post_view(request, challenge_id, post_id)

########################
# Delete post
########################

@login_required
def delete_post(request, challenge_id=None, post_id=None):
    instance = Post.objects.get(id=post_id)
    instance.delete()

    return HttpResponseRedirect(reverse('core:home', args=(challenge_id)))

@login_required
def like_post(request, challenge_id=None, post_id=None):
    instance = Post.objects.get(id=post_id)
    current_account = get_account_from_user(request.user)

    if current_account in instance.liked_account_set.all():
        instance.liked_account_set.remove(current_account)
    else:
        instance.liked_account_set.add(current_account)

    return HttpResponseRedirect(reverse('core:home', args=(challenge_id)))

@login_required
def edit_post_view(request, challenge_id, post_id):
    instance = Post.objects.get(id=post_id)
    form = PostForm(data=request.POST or None, user=request.user, instance=instance, post_id=post_id)

    template = 'post/create_post.html'

    return render(request, template, {'form': form, 'challenge_id': challenge_id, 'post_id': post_id})

