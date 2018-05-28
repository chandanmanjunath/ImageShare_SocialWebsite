# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0003_auto_20180513_0103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='total_likes',
            field=models.PositiveIntegerField(default=0, db_index=True),
        ),
    ]
