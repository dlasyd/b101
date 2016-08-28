# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0020_auto_20160826_0908'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='url_alias',
            new_name='slug',
        ),
        migrations.AlterField(
            model_name='article',
            name='author',
            field=models.ForeignKey(editable=False, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='article',
            name='category',
            field=models.ForeignKey(on_delete=None, to='articles.Category'),
        ),
    ]
