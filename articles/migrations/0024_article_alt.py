# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0023_auto_20160904_2315'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='alt',
            field=models.CharField(max_length=200, blank=True),
        ),
    ]
