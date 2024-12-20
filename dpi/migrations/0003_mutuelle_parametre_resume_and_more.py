# Generated by Django 5.1.4 on 2024-12-14 12:48

import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dpi', '0002_alter_hopital_date_debut_service'),
        ('utilisateur', '0002_alter_utilisateur_managers_alter_utilisateur_role'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mutuelle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Parametre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Resume',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('diagnostic', models.TextField(blank=True)),
                ('date_prochaine_consultation', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='ordonnancemedicament',
            name='medicament',
        ),
        migrations.RemoveField(
            model_name='ordonnancemedicament',
            name='ordonnance',
        ),
        migrations.RenameField(
            model_name='certificat',
            old_name='description',
            new_name='contenu',
        ),
        migrations.RemoveField(
            model_name='certificat',
            name='date_debut',
        ),
        migrations.RemoveField(
            model_name='certificat',
            name='date_fin',
        ),
        migrations.RemoveField(
            model_name='consultation',
            name='medecin_principal',
        ),
        migrations.RemoveField(
            model_name='consultation',
            name='notes',
        ),
        migrations.RemoveField(
            model_name='medicament',
            name='effets_secondaire',
        ),
        migrations.RemoveField(
            model_name='soin',
            name='type',
        ),
        migrations.AddField(
            model_name='certificat',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='consultation',
            name='heure',
            field=models.TimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='dpi',
            name='date_création',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='soin',
            name='type_soin',
            field=models.CharField(default=django.utils.timezone.now, max_length=32),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='consultation',
            name='date_de_consultation',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='decompte',
            name='date',
            field=models.DateField(verbose_name=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='graphiquetendance',
            name='bilan_biologique',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='graphiqus', to='dpi.bilanbiologique'),
        ),
        migrations.AlterField(
            model_name='hopital',
            name='lieu',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='hopital',
            name='nom',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='hopitalutilisateur',
            name='date_adhesion',
            field=models.DateField(verbose_name=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='ordonnance',
            name='date_de_creation',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.CreateModel(
            name='Hospitalisation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_entree', models.DateField(verbose_name=django.utils.timezone.now)),
                ('date_sortie', models.DateField(verbose_name=django.utils.timezone.now)),
                ('cree_par', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='utilisateur.administratif')),
                ('hopital', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dpi.hopital')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='utilisateur.patient')),
            ],
        ),
        migrations.CreateModel(
            name='ParametreValeur',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valeur', models.CharField(max_length=100)),
                ('bilan_biologique', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dpi.bilanbiologique')),
                ('parametre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dpi.parametre')),
            ],
        ),
        migrations.CreateModel(
            name='Prescription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dose', models.CharField(max_length=10)),
                ('duree', models.DecimalField(decimal_places=2, max_digits=5)),
                ('heure', models.TimeField(null=True)),
                ('nombre_de_prises', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('medicament', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dpi.medicament')),
            ],
        ),
migrations.AddField(
    model_name='ordonnance',
    name='prescription',
    field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dpi.prescription', null=True),  # Removed default
),
migrations.AddField(
    model_name='consultation',
    name='resume',
    field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='consultations', to='dpi.resume', null=True),  # Removed default
),

        migrations.CreateModel(
            name='ResumeMesuresPrises',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mesure', models.CharField(max_length=500)),
                ('resume', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mesures', to='dpi.resume')),
            ],
        ),
        migrations.CreateModel(
            name='ResumeSymptomes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symptome', models.CharField(max_length=500)),
                ('resume', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='symptomes', to='dpi.resume')),
            ],
        ),
        migrations.CreateModel(
            name='SoinInfermier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('infermier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='utilisateur.infermier')),
                ('soin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dpi.soin')),
            ],
        ),
        migrations.DeleteModel(
            name='Hospitazliation',
        ),
        migrations.DeleteModel(
            name='OrdonnanceMedicament',
        ),
    ]
