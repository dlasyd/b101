# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-08 06:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0007_article_teaser_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='url_alias',
            field=models.SlugField(default='123'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='article',
            name='creation_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='teaser_image',
            field=models.ImageField(blank=True, upload_to='teaser-images'),
        ),
    ]
