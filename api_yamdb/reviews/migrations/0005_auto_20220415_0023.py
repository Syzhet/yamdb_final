# Generated by Django 2.2.16 on 2022-04-14 21:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0004_auto_20220415_0017'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comments',
            old_name='review_id',
            new_name='review',
        ),
        migrations.RenameField(
            model_name='review',
            old_name='title_id',
            new_name='title',
        ),
    ]
