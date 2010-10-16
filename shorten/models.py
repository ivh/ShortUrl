from django.db import models as m

class URL(m.Model):
    key=m.CharField(max_length=16,primary_key=True,unique=True,db_index=True,blank=True)
    url=m.CharField(max_length=1024,null=False,blank=False)

    def get_absolute_url(self):
        return "/%s/view" % self.key
    def __unicode__(self):
        return u"%s -> %s"%(self.key,self.url)

