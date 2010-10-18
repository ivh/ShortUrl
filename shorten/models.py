from django.db import models as m
from django.core.exceptions import ValidationError

import re
import string as s
from random import choice
def newKey(length=4, chars=s.letters + s.digits):
    return ''.join([choice(chars) for i in xrange(length)])

from urlparse import urlparse

FORBIDDENKEYS=['api','tmp','piwik','pipermail','listarkiv','mailman','admin']

class URL(m.Model):
    key=m.CharField(max_length=16,primary_key=True,unique=True,db_index=True,blank=False)
    url=m.CharField(max_length=1024,null=False,blank=False)

    def get_absolute_url(self):
        return "/%s/view" % self.key
    def __unicode__(self):
        return u"%s -> %s"%(self.key,self.url)

    
    def clean(self):
        if not urlparse(self.url).scheme: self.url='http://'+self.url
        if not urlparse(self.url).netloc:
            raise ValidationError('This seems not to be a real URL.')
        if urlparse(self.url).netloc == 'tmy.se':
            raise ValidationError('No redirects to tmy.se are allowed.')

        if self.key in FORBIDDENKEYS:
            raise ValidationError('This is a reserved key.')
        if not re.match(r'[\w]+$', self.key):
            raise ValidationError('Only letters and numbers for the short key, please.')
        if len(self.key) < 3:
            raise ValidationError('The short key must at least be 3 letters or digits long.')
