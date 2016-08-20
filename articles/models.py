from django.db import models
from django.contrib.auth.models import User
from django.dispatch.dispatcher import receiver
from transliterate import slugify

import os


class Article(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    preview_text = models.TextField()
    author = models.ForeignKey(User)
    creation_date = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False)
    url_alias = models.SlugField()
    teaser_image = models.ImageField(upload_to="teaser-images",
                                     blank=True)
    category = models.ForeignKey('Category', on_delete=None)
    legacy = models.BooleanField(default=False)
    tags = models.ManyToManyField('Tag', blank=True)

    def save(self, *args, **kwargs):
        if not self.id:
            # Only set the slug when the object is created.
            self.url_alias = slugify(self.title, language_code='ru')
        super(Article, self).save(*args, **kwargs)


class Category(models.Model):
    name = models.CharField(max_length=50)
    url_alias = models.SlugField()

    def save(self, *args, **kwargs):
        if not self.id:
            # Only set the slug when the object is created.
            self.url_alias = slugify(self.name, language_code='ru')
        super(Category, self).save(*args, **kwargs)


class Tag(models.Model):
    name = models.CharField(max_length=50)


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
