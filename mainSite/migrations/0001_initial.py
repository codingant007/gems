# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Candidates',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('username', models.CharField(max_length=50)),
                ('details', models.CharField(max_length=10000)),
                ('photo', models.CharField(max_length=100)),
                ('approved', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ChallengeStrings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('challengeStr', models.CharField(max_length=2048)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='New_Candidate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('post', models.CharField(max_length=4, default='')),
                ('roll', models.IntegerField(max_length=10, default=0)),
                ('department', models.CharField(max_length=100, default='')),
                ('cpi', models.FloatField(max_length=4, default=0)),
                ('sem', models.IntegerField(max_length=1, default=0)),
                ('backlogs', models.CharField(max_length=50, default='')),
                ('email', models.CharField(max_length=50, default='')),
                ('contact', models.IntegerField(max_length=10, default=0)),
                ('hostel', models.CharField(max_length=10, default='')),
                ('room', models.CharField(max_length=10, default='')),
                ('agenda', models.CharField(max_length=100000, default='')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Posts',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('postName', models.CharField(max_length=50)),
                ('postCount', models.IntegerField(max_length=3, default=0)),
                ('voterGender', models.CharField(max_length=1)),
                ('voterCourse', models.CharField(max_length=2)),
                ('eligibleGender', models.CharField(max_length=1)),
                ('eligibleCourse', models.CharField(max_length=2)),
                ('eligibleYear', models.CharField(max_length=2)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PublicKeys',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('publicKey', models.CharField(max_length=2048)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('username', models.CharField(max_length=50)),
                ('voted', models.BooleanField(default=False)),
                ('department', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=50)),
                ('gender', models.CharField(max_length=1)),
                ('course', models.CharField(max_length=30)),
                ('hostel', models.CharField(max_length=30)),
                ('encryptedPrivateKey', models.CharField(max_length=4096)),
                ('plaintextPrivatekey', models.CharField(max_length=2048)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Votes',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('plainText', models.CharField(max_length=50)),
                ('certificate', models.CharField(max_length=60)),
                ('challengeStr', models.ForeignKey(to='mainSite.ChallengeStrings')),
                ('publicKey', models.ForeignKey(to='mainSite.PublicKeys')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
