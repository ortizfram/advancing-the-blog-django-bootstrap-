from django.db import models
from django.conf import settings
from apps.posts.models import Post


# Create your models here.
class Comment(models.Model):
    user        = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.PROTECT) #superadmin default
    post        = models.ForeignKey(Post,  on_delete=models.CASCADE)
    content     = models.TextField()
    timestamp   = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return str(self.user.username)
    
    def __str__(self):
        return str(self.user.username)