from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
import os


class Article(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    preview_text = models.TextField()
    author = models.ForeignKey(User)
    creation_date = models.DateTimeField()
    is_published = models.BooleanField(default=False)

    teaser_image = models.ImageField(upload_to="teaser-images",
                                     blank=True)


# @receiver(pre_delete, sender=Article)
# def article_delete(sender, instance, **kwargs):
#     # Pass false so FileField doesn't save the model.
#     instance.file.delete(False)
#

@receiver(models.signals.post_delete, sender=Article)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    print("File should be deleted now")
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)
