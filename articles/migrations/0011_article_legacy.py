# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-02 05:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0010_article_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='legacy',
            field=models.BooleanField(default=False),
        ),
    ]
