from django.conf.urls.defaults import *

from models import URL

urlpatterns = patterns('',
    url(r'^shorten/$','shorten.views.new',name='new'),
    url(r'^api$','shorten.views.api',name='api'),
    url(r'^(?P<object_id>\w+)/view/$', 'django.views.generic.list_detail.object_detail', {'queryset': URL.objects.all(),'template_name':'view.html'}),
    url(r'^^(?P<key>\w+)/qrs/$','shorten.views.qrs',name='qrs'),
    url(r'^^(?P<key>\w+)/qrl/$','shorten.views.qrl',name='qrl'),
    url(r'^(?P<key>\w+)/$', 'shorten.views.redir',name='redirect'),
)
