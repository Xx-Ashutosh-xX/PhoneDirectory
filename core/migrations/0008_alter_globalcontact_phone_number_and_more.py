# Generated by Django 5.0.3 on 2024-08-10 23:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_alter_globalcontact_phone_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='globalcontact',
            name='phone_number',
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name='spamreport',
            name='phone_number',
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(max_length=15, unique=True),
        ),
    ]
