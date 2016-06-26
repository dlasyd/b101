from django.db import models
from django.contrib.auth.models import User


class Article(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    preview_text = models.TextField()
    author = models.ForeignKey(User)
    creation_date = models.DateTimeField()
    is_published = models.BooleanField(default=False)
    teaser_image = models.ImageField(upload_to="/Users/Andrey/IdeaProjects/b111/files/images/",
                                     blank=True)