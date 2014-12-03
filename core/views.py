# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, render_to_response, RequestContext, HttpResponseRedirect
from django.core.paginator import Paginator

from account.models import Account
from account.forms import AccountCreateForm
from challenge.models import Challenge
from utils.func import get_account_from_user

from datetime import datetime

def index(request):
    template = 'index.html'

    form = AccountCreateForm(request.POST or None)
    context = RequestContext(request)

    if request.user.is_authenticated():
        current_account = get_account_from_user(request.user)

        if current_account is None:
            logout(request)
            redirect('/')
        else:
            pass

        return home(request)

    return render_to_response(template, locals(), context_instance=context)

@login_required
def home(request, challenge_id = None):
    template = 'home.html'

    challenges = Challenge.objects.all().order_by('start_date')

    try:
        current_challenge = Challenge.objects.get(id=challenge_id)
    except:
        current_challenge = challenges[len(challenges)-1]

    NUM_PER_PAGE = 4

    p = Paginator(challenges, NUM_PER_PAGE)
    page_num = 1

    for i in p.page_range:
        if current_challenge in p.page(i).object_list:
            page_num = i
            break

    page = p.page(page_num)

    challenges = page.object_list

    now = datetime.now()

    for challenge in challenges:
        if challenge.start_date <= now.date() <= challenge.finish_date:
            challenge.active = True
        else:
            challenge.active = False


    current_account = get_account_from_user(request.user)
    if current_challenge.post_set.filter(account = current_account):
        disable_create_btn = True
    else:
        disable_create_btn = False

    for post in current_challenge.post_set.all():
        post.like = True

    return render(request,
                  template,
                  {'challenges': challenges,
                   'disable_create_btn': disable_create_btn,
                   'current_challenge': current_challenge,
                   'page_num_plus_1': page_num * NUM_PER_PAGE + 1,
                   'page_num_minus_1': (page_num - 1) * NUM_PER_PAGE - 1,
                   'has_next': page.has_next(),
                   'has_previous': page.has_previous() })

def about(request):
    pass
