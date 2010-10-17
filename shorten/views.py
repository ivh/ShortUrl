from django.shortcuts import render_to_response,get_object_or_404,redirect
from django.template import RequestContext
from django.http import HttpResponsePermanentRedirect,HttpResponse
from django import forms
from django.utils.datastructures import MergeDict

from qrencode import encode as makeQR
from simplejson import dump as json

from models import URL,newKey
def safeNewKey(length=3,key=None):
    if not key: key=newKey(length)
    try:
        #if len(key)>6: raise Exception # for testing
        URL.objects.get(pk=key)
    except: return key
    else:
        return safeNewKey(key=key+newKey(1))

class UrlForm(forms.ModelForm):
    class Meta:
        model=URL
        widgets = {
            'key': forms.TextInput(attrs={'size':'4'}),
            'url': forms.TextInput(attrs={'size':'64'}),
        }

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
        key=safeNewKey()
        url=UrlForm(initial={'key':key})
        
    c=RequestContext(request,{'url':url})
    return render_to_response('shorten.html', c)

def api(request):
    if not request.REQUEST.has_key('key'):
        url=UrlForm(MergeDict(request.REQUEST,{'key':safeNewKey()}))
    else: url=UrlForm(request.REQUEST)

    if url.is_valid():
        url.save()
        retdict=url.cleaned_data.copy()
        retdict['lurl']=retdict['url']
        del retdict['url']
        retdict['surl']='http://tmy.se/'+retdict['key']
        del retdict['key'] 
        retdict['view']=retdict['surl']+'/view/'
        retdict['qrl']=retdict['surl']+'/qrl/'
        retdict['qrs']=retdict['surl']+'/qrs/'

        response = HttpResponse(mimetype="application/json",status=201)
        json(retdict,response)

    else:
        response = HttpResponse(mimetype="application/json",status=409)
        json({'error':'Something went wrong, most probably, the short key you wanted was already taken'},response)

    return response
    

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
