# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-26 18:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0006_article_is_published'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='teaser_image',
            field=models.ImageField(blank=True, upload_to='/Users/Andrey/IdeaProjects/b111/files/images/'),
        ),
    ]
