from django.db import models

class Lenta (models.Model):
    url = models.CharField(max_length=200)
