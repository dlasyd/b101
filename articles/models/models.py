import os

from transliterate import slugify

from django.db import models
from django.contrib.auth.models import User
from django.dispatch.dispatcher import receiver
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.db import IntegrityError

from .managers import ArticleManager


class Article(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, editable=False)
    preview_text = models.TextField()
    text = models.TextField()
    teaser_image = models.ImageField(upload_to="teaser-images", blank=True)

    creation_date = models.DateTimeField(auto_now_add=True)
    published_date = models.DateTimeField(blank=True, null=True)

    category = models.ForeignKey('Category', on_delete=None)
    tags = models.ManyToManyField('Tag', blank=True)

    slug = models.SlugField(unique=True, blank=True)
    legacy = models.BooleanField(default=False)

    state = models.CharField(default=1,
                             choices=(('1', "Not Published"), ('2', "Staged for publication"), ('3', "Published")),
                             max_length=1,)

    objects = ArticleManager()

    def save(self, *args, **kwargs):
        if self.id and self.published_date is None and self.state == '3':
            self.published_date = timezone.now()
        else:
            if not self.slug:
                self.slug = slugify(self.title, language_code='ru')[0:50]

            if self.published_date is None and self.state == '3':
                self.published_date = timezone.now()

        super(Article, self).save(*args, **kwargs)

    def __str__(self):
        return self.title + ' ' + self.category.name

    def get_absolute_url(self):
        return reverse('article-view', args=[self.slug])


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        if self.name == '':
            raise IntegrityError('Category name cannot be blank')
        if not self.id and not self.slug:
            # Only set the slug when the object is created.
            self.slug = slugify(self.name, language_code='ru')
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
