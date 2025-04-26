from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from urllib.parse import urlencode
from forms import *

# Create your views here.

def chatView(request):
    # make sure the user is logged in
    if not request.session['is_loggedin']:
        context = {
            'page': 'chat page'
        }
        return HttpResponse(loader.get_template('nlogged_in.html').render(context, request))
    template = loader.get_template('chat.html')
    context = {
        'user_id': request.session['user_id'],
        'username': request.session['username'],
    }
    return HttpResponse(template.render(context, request))

def loginView(request):
    # if user is logged in, deny it!
    if not request.session['is_loggedin']:
        context = {
            'page': 'log in page'
        }
        return HttpResponse(loader.get_template('nlogged_in.html').render(context, request))
    context = {
        'status': request.GET.get('status', 'n')
    }
    
    return HttpResponse(loader.get_template('login.html').render(context, request))

def processLoginView(request):
    # very useful: https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Server-side/Django/Forms
    # this is meant strictly for processing
    # so post data must exist
    if request.method != 'POST':
        return HttpResponseForbidden() # forbiden!
    
    # we need to process everything
    f = LogInForm(request.POST)

    # make sure form data is valid
    if not f.is_valid():
        u = redirect('login')
        params = {
            'status': 'fail'
        }
        encoded = urlencode(params)
        return redirect(f'{u}?{encoded}')
    
    username = f.cleaned_data['username']
    pwd = f.cleaned_data['password']
    #TODO: DO REMEMBER ME
    # run through all the data

def connectView(request):
    # must be logged in
    if not request.session['is_loggedin']:
        context = {
            'page': 'log in page'
        }
        return HttpResponse(loader.get_template('nlogged_in.html').render(context, request))
    
    context=  {
        'username': request.session['username']
    }
    return HttpResponse(loader.get_template('connect.html').render(context, request))

def signUpView(request):
    # users logged in shouldn't make another account!
    if request.session['is_loggedin']:
        context = {
            'page': 'already logged in!'
        }
        return HttpResponse(loader.get_template('nlogged_in.html').render(context, request))
    
    return HttpResponse(loader.get_template('signup.html').render())