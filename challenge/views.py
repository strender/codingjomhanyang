# Create your views here.
from django.conf import settings
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect, render_to_response, RequestContext, HttpResponseRedirect

from .models import Challenge, Tag
from account.models import Account
from account.forms import AccountCreateForm

from utils.func import *

def view_challenge_list(request):
    pass

def view_challenge_detail(request):
    pass

