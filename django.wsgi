import os
import sys
sys.path.append('/home/tom/py/')
sys.path.append('/home/tom/sites/')

os.environ['DJANGO_SETTINGS_MODULE'] = 'ShortUrl.settings'


import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
