# Generated by Django 5.0 on 2024-12-27 08:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dpi', '0005_alter_consultation_medecin_principal_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prescription',
            name='medicament',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prescriptions', to='dpi.medicament'),
        ),
        migrations.AlterField(
            model_name='prescription',
            name='ordonnance',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prescriptions', to='dpi.ordonnance'),
        ),
    ]
