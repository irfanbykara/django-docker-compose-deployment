# Generated by Django 3.2.10 on 2022-01-02 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_profile_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='level',
            field=models.CharField(choices=[('beginner', 'BEGINNER'), ('intermediate', 'INTERMEDIATE'), ('expert', 'EXPERT')], max_length=200, null=True),
        ),
    ]