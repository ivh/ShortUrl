from django.db import models as m
from django.core.exceptions import ValidationError

import string as s
from random import choice
def newKey(length=4, chars=s.letters + s.digits):
    return ''.join([choice(chars) for i in xrange(length)])

from urlparse import urlparse

class URL(m.Model):
    key=m.CharField(max_length=16,primary_key=True,unique=True,db_index=True,blank=True)
    url=m.CharField(max_length=1024,null=False,blank=False)

    def get_absolute_url(self):
        return "/%s/view" % self.key
    def __unicode__(self):
        return u"%s -> %s"%(self.key,self.url)

    def fixKey(self):
        if not self.key: self.key=newKey()

    def clean(self):
        if not self.key: self.fixKey()
        if not urlparse(self.url).scheme: self.url='http://'+self.url
        if not urlparse(self.url).netloc:
            raise ValidationError('Not a real URL')
