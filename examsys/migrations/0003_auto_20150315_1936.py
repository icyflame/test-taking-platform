# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('examsys', '0002_auto_20150315_1640'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TestToAnswer',
            new_name='TestToQuestion',
        ),
    ]
