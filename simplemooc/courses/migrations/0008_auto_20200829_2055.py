# Generated by Django 3.0.8 on 2020-08-29 23:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0007_auto_20200829_1958'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lesson',
            old_name='descrition',
            new_name='description',
        ),
    ]
