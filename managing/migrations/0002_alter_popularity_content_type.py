# Generated by Django 4.1 on 2022-09-04 19:04

import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('managing', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='popularity',
            name='content_type',
            field=models.ForeignKey(limit_choices_to=models.Q(models.Q(('app_label', 'managing'), ('model', django.contrib.auth.models.User)), models.Q(('app_label', 'managing'), ('model', 'book')), _connector='OR'), on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s', to='contenttypes.contenttype', verbose_name='Action on model'),
        ),
    ]
