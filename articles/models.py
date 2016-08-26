from django.db import models
from django.contrib.auth.models import User
from django.dispatch.dispatcher import receiver
from django.utils import timezone
from transliterate import slugify
from django.core.urlresolvers import reverse

import os


class Article(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User)
    preview_text = models.TextField()
    text = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    published_date = models.DateTimeField(blank=True, null=True)
    is_published = models.BooleanField(default=False)
    url_alias = models.SlugField(unique=True, blank=True)
    teaser_image = models.ImageField(upload_to="teaser-images",
                                     blank=True)
    category = models.ForeignKey('Category', on_delete=None)
    legacy = models.BooleanField(default=False)
    tags = models.ManyToManyField('Tag', blank=True)

    def save(self, *args, **kwargs):
        if self.id:
            if self.published_date is None:
                orig = Article.objects.get(id=self.id)
                if (orig.is_published != self.is_published) and self.is_published is True:
                    self.published_date = timezone.now()
        else:
            if not self.url_alias:
                self.url_alias = slugify(self.title, language_code='ru')[0:50]

            if self.published_date is None and self.is_published is True:
                self.published_date = timezone.now()

        super(Article, self).save(*args, **kwargs)

    def __str__(self):
        return self.title + ' ' + self.category.name

    def get_absolute_url(self):
        return reverse('article-view', args=[self.url_alias])


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    url_alias = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        if not self.id and not self.url_alias:
            # Only set the slug when the object is created.
            self.url_alias = slugify(self.name, language_code='ru')
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


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
