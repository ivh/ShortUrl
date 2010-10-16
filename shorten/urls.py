from django.conf.urls.defaults import *

from models import URL

urlpatterns = patterns('',
    url(r'^(?P<object_id>\w+)/view/$', 'django.views.generic.list_detail.object_detail', {'queryset': URL.objects.all(),'template_name':'view.html'}),
    url(r'^(?P<key>\w+)$', 'shorten.views.redirect',name='redirect'),
)
