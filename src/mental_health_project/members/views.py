from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# Create your views here.

def chatView(request):
    template = loader.get_template('chat.html')
    return HttpResponse(template.render())