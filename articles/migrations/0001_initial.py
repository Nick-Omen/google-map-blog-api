# Generated by Django 2.0.6 on 2018-06-27 12:22

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('places', '0002_auto_20180627_1222'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Title')),
                ('slug', models.CharField(db_index=True, default='', help_text='This field will be filled automatically.', max_length=32, verbose_name='Slug')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('date', models.DateTimeField(blank=True, default=datetime.datetime.now, verbose_name='Date')),
                ('content', models.TextField(blank=True, default='', verbose_name='Content')),
                ('content_short', models.CharField(blank=True, default='', max_length=155, verbose_name='Content short')),
                ('place', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='places.Place', verbose_name='Place')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
