# Generated by Django 5.0 on 2024-12-31 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dpi', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='consultation',
            name='diagnostic',
            field=models.TextField(blank=True, null=True),
        ),
    ]
