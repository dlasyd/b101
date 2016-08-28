# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0021_auto_20160828_1203'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='url_alias',
            new_name='slug',
        ),
    ]
