# Generated by Django 3.2.10 on 2022-03-02 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0017_auto_20220228_2142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workout',
            name='user_bmi',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='workout',
            name='user_height',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='workout',
            name='user_weight',
            field=models.IntegerField(null=True),
        ),
    ]
