# Generated by Django 4.1.1 on 2022-09-07 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('managing', '0004_followup_action_followup_date_followup_object_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='reply',
            name='body',
            field=models.TextField(null=True),
        ),
    ]
