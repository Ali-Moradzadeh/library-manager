# Generated by Django 4.1.1 on 2022-09-11 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('managing', '0007_alter_reply_quotes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='title',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
