# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainSite', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidates',
            name='contestingPost',
            field=models.CharField(default='', max_length=10),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='candidates',
            name='noOfVotes',
            field=models.IntegerField(default=0, max_length=6),
            preserve_default=True,
        ),
    ]
