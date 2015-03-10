# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bandmatch', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='band',
            name='image',
            field=models.ImageField(upload_to=b'band_images', blank=True),
        ),
    ]
