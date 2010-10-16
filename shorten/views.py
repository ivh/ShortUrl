from django.shortcuts import render_to_response,get_object_or_404
from django.http import HttpResponseRedirect

from models import URL

def redirect(request,key):
    url=get_object_or_404(URL,key=key)
    return HttpResponseRedirect(url.url)

def view(request,key):
    url=get_object_or_404(URL,key=key)
    render_to_response('view.html',{'url':url})

