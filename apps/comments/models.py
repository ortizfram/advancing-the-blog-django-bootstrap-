from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse



# Create your models here.
class CommentManager(models.Manager):
    def all(self):
        qs = super(CommentManager, self).filter(parent=None)
        return qs
    

    def filter_by_instance(self, instance):
        content_type = ContentType.objects.get_for_model(instance.__class__)
        obj_id       = instance.id
        qs           = super(CommentManager, self).filter(content_type=content_type, object_id=obj_id).filter(parent=None)
        return qs


class Comment(models.Model):
    user        = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.PROTECT) #superadmin default
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE)

    content     = models.TextField()
    timestamp   = models.DateTimeField(auto_now_add=True)

    objects     = CommentManager()

    class Meta:
        ordering = ['-timestamp'] # -timestamp = newest || timestamp=oldest

    def __unicode__(self):
        return str(self.user.username)
    
    def __str__(self):
        return str(self.user.username)

    def get_absolute_url(self):
        # If it's a parent comment, return the URL for its comment thread
        if self.is_parent:
        # If it's a parent comment, return the URL for the post detail page
            return reverse("posts:post_detail", kwargs={"slug": self.content_object.slug})
        elif self.parent:
            # If it's a child comment, return the URL for the parent comment's thread
            return reverse("comments:thread", kwargs={"id": self.parent.id})
        else:
            # Handle the case where neither self.parent nor self.is_parent is True
            return reverse("comments:thread", kwargs={"id": self.id})

    def get_delete_url(self):
        return reverse("comments:delete", kwargs={"id": self.id})
    
    
    def children(self): # replies
        return Comment.objects.filter(parent=self)
    
    @property
    def is_parent(self):
        return self.parent is None
