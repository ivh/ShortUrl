from django.conf.urls import *
from django.views.generic import DetailView
from models import URL


class UrlDetailView(DetailView):
    model = URL


urlpatterns = patterns('',
    url(r'^shorten/$','shorten.views.new',name='new'),
    url(r'^api/$','shorten.views.api',name='api'),
    url(r'^(?P<pk>\w+)/view/$', UrlDetailView.as_view(template_name="view.html")),
    url(r'^^(?P<key>\w+)/qrs/$','shorten.views.qrs',name='qrs'),
    url(r'^^(?P<key>\w+)/qrl/$','shorten.views.qrl',name='qrl'),
    url(r'^(?P<key>\w+)(.html)?$', 'shorten.views.redir',name='redirect'),
)
