# Generated by Django 4.1.1 on 2022-09-07 15:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
        ('managing', '0003_alter_followup_unique_together_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='followup',
            name='action',
            field=models.CharField(choices=[('F', 'Follow')], max_length=1, null=True),
        ),
        migrations.AddField(
            model_name='followup',
            name='date',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='followup',
            name='object_id',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='followup',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='prevention',
            name='action',
            field=models.CharField(choices=[('B', 'Bann'), ('R', 'Report')], max_length=1, null=True),
        ),
        migrations.AddField(
            model_name='prevention',
            name='date',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='prevention',
            name='object_id',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='prevention',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='suggestion',
            name='date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='suggestion',
            name='info',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='address',
            name='object_id',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='author',
            name='last_name',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='author',
            name='name',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='author',
            name='nationality',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='book', to='managing.author'),
        ),
        migrations.AlterField(
            model_name='book',
            name='title',
            field=models.CharField(max_length=100, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='body',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='book',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comment', to='managing.book'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='date_published',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='date_updated',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comment', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='loan',
            name='book',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='req_loan', to='managing.book'),
        ),
        migrations.AlterField(
            model_name='loan',
            name='date_requested',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='loan',
            name='last_request_state_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='loan',
            name='request_state',
            field=models.CharField(choices=[('R', 'Requested'), ('C', 'Checking'), ('RC', 'request confirmed'), ('S', 'Sent'), ('D', 'Delivered')], max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='loan',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='req_loan', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='popularity',
            name='content_type',
            field=models.ForeignKey(limit_choices_to=models.Q(models.Q(('app_label', 'managing'), ('model', 'author')), models.Q(('app_label', 'managing'), ('model', 'publisher')), models.Q(('app_label', 'managing'), ('model', 'book')), models.Q(('app_label', 'managing'), ('model', 'comment')), models.Q(('app_label', 'managing'), ('model', 'reply')), models.Q(('app_label', 'taggit'), ('model', 'tag')), _connector='OR'), null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype', verbose_name='Action on model'),
        ),
        migrations.AlterField(
            model_name='popularity',
            name='date',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='popularity',
            name='object_id',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='popularity',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='publisher',
            name='register_code',
            field=models.PositiveIntegerField(null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='reply',
            name='comment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reply', to='managing.comment'),
        ),
        migrations.AlterField(
            model_name='reply',
            name='date_published',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='reply',
            name='date_updated',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='reply',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reply', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='suggestion',
            name='Author',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='suggestion',
            name='book',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='suggestion',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ssuggestions', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='followup',
            unique_together={('action', 'content_type', 'object_id')},
        ),
        migrations.AlterUniqueTogether(
            name='prevention',
            unique_together={('action', 'content_type', 'object_id')},
        ),
    ]
