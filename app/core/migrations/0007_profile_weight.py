# Generated by Django 3.2.10 on 2022-02-24 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_customexcercise'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='weight',
            field=models.IntegerField(null=True),
        ),
    ]