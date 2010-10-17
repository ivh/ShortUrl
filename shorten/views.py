from django.shortcuts import render_to_response,get_object_or_404,redirect
from django.template import RequestContext
from django.http import HttpResponsePermanentRedirect,HttpResponse
from django import forms

from qrencode import encode as makeQR

from models import URL,newKey

class UrlForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UrlForm, self).__init__(*args, **kwargs)
        self.fields['key'].widget = forms.TextInput(attrs={'size':'4'})
        self.fields['url'].widget = forms.TextInput(attrs={'size':'64'})

    class Meta:
        model=URL


# actual views start here

def redir(request,key):
    url=get_object_or_404(URL,key=key)
    return HttpResponsePermanentRedirect(url.url)

def view(request,key):
    url=get_object_or_404(URL,key=key)
    render_to_response('view.html',{'url':url})

def new(request):
    if request.method=='POST':
        url=UrlForm(request.REQUEST)
        if url.is_valid():
            url.save()
            return redirect(url.instance)
    else:
        key=newKey(3)
        try:
            URL.objects.get(pk=key)
            key+=newKey(3)
        except: pass
        url=UrlForm(initial={'key':key})
        
    c=RequestContext(request,{'url':url})
    return render_to_response('shorten.html', c)

def qrs(request,key):
    url=get_object_or_404(URL,key=key)
    qr=makeQR('http://tmy.se/'+url.key)[-1].resize((96,96))
    response = HttpResponse(mimetype="image/png")
    qr.save(response, "PNG")
    return response

def qrl(request,key):
    url=get_object_or_404(URL,key=key)
    qr=makeQR(url.url)[-1].resize((128,128))
    response = HttpResponse(mimetype="image/png")
    qr.save(response, "PNG")
    return response
