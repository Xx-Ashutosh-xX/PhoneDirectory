# Generated by Django 5.0.3 on 2024-08-10 22:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_user_options_alter_user_managers_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='GlobalContact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('phone_number', models.CharField(max_length=15)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='spamreport',
            name='is_spam',
        ),
        migrations.RemoveField(
            model_name='spamreport',
            name='reporter',
        ),
        migrations.AddField(
            model_name='spamreport',
            name='spamCount',
            field=models.IntegerField(default=0),
        ),
        migrations.DeleteModel(
            name='Contact',
        ),
    ]