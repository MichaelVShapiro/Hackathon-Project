from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from urllib.parse import urlencode
from django.views.decorators.csrf import csrf_exempt

from .forms import *
from .chatbot.rag_query import *

bot: RAGQueryMLX = RAGQueryMLX() # for cache

def getChatBotResponse(i: str):
    """
    Gets the response from the chat bot given an input
    Args:
        i: Required. A string representing the input
    
    Returns:
        Chatbot response
    """
    return bot.query(i)[0]

# Create your views here.

@csrf_exempt
def chatView(request):
    # make sure the user is logged in
    if not request.session.get('is_loggedin', False):
        pass
        # context = {
        #     'page': 'chat page'
        # }
        # return HttpResponse(loader.get_template('nloggedin.html').render(context, request))
    if request.method == 'POST':
        cleaned = ChatForm(request.POST)
        if not cleaned.is_valid():
            return HttpResponseForbidden()
        
        return HttpResponse(getChatBotResponse(cleaned.cleaned_data['chat_text']))
    template = loader.get_template('chat.html')
    context = {
        'username': request.session.get('username', 'anonymous')
    }
    return HttpResponse(template.render(context, request))

def loginView(request):
    # if user is logged in, deny it!
    if request.session.get('is_loggedin', False):
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
    if not request.session.get('is_loggedin', False):
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
    if request.session.get('is_loggedin', False):
        context = {
            'page': 'already logged in!'
        }
        return HttpResponse(loader.get_template('nlogged_in.html').render(context, request))
    
    return HttpResponse(loader.get_template('signup.html').render())

def processLogIn(request):
    # if logged in, skip
    if request.method != 'POST':
        return HttpResponseForbidden()
    
    # process login data
    login_data = UserLogInInfo(request.POST)
    if login_data.is_valid():
        if login_data.cleaned_data['is_logging_in']:
            # set session variables
            request.session['is_loggedin'] = True
            request.session['username'] = login_data.cleaned_data['username']
            context = {
                'username': login_data.cleaned_data['username']
            }
            return HttpResponse(loader.get_template('dashboard.html').render(context, request))
        else:
            request.session.clear()
            return HttpResponse(loader.get_template('login.html').render())
    return HttpResponseForbidden()