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

def getRetDict(key,lurl=None):
    if not lurl: lurl=URL.objects.get(pk=key).url
    retdict={'lurl':lurl,'surl':'http://tmy.se/'+key}
    retdict['view']=retdict['surl']+'/view/'
    retdict['qrl']=retdict['surl']+'/qrl/'
    retdict['qrs']=retdict['surl']+'/qrs/'
    return retdict

def api(request):
    if request.REQUEST.has_key('key') and request.REQUEST.has_key('url') :
        url=UrlForm(request.REQUEST)
    elif request.REQUEST.has_key('key'):
        urlinst=get_object_or_404(URL,key=request.REQUEST['key'])
        url=UrlForm({'key':urlinst.key,'url':urlinst.url},instance=urlinst)
    elif request.REQUEST.has_key('url'):
        url=UrlForm(MergeDict(request.REQUEST,{'key':safeNewKey()}))

    else: url=UrlForm()

    if url.is_valid():
        url.save()
        retdict=getRetDict(url.cleaned_data['key'],url.cleaned_data['url'],)
        
        response = HttpResponse(mimetype="application/json",status=201)
        json(retdict,response)

    else:
        response = HttpResponse(mimetype="application/json",status=409)
        json({'error':'Something went wrong, most probably, the short key you wanted was already taken or invalid.'},response)

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
