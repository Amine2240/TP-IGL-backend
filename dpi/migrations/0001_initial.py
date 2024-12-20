# Generated by Django 5.0 on 2024-12-19 22:36

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('utilisateur', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bilan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('biologique', 'Biologique'), ('radiologique', 'Radiologique')], max_length=32)),
                ('resultats', models.TextField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='ContactUrgence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=32)),
                ('prenom', models.CharField(max_length=32)),
                ('email', models.EmailField(max_length=254)),
                ('telephone', models.CharField(max_length=10, validators=[django.core.validators.RegexValidator(message='Numero de telephone invalide', regex='^\\d{10}$')])),
            ],
        ),
        migrations.CreateModel(
            name='Hopital',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=64)),
                ('lieu', models.CharField(max_length=64)),
                ('date_debut_service', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Medicament',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=32)),
                ('effets_secondaire', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Outil',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Soin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('type_1', 'Type_1'), ('type_2', 'Type_2'), ('type_3', 'Type_3')], default='type_1', max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='BilanBiologique',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bilan', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='bilan_biologique', to='dpi.bilan')),
                ('laborantin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bilans', to='utilisateur.laborantin')),
            ],
        ),
        migrations.CreateModel(
            name='BilanBiologiqueLaborantin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bilan_bio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dpi.bilanbiologique')),
                ('laborantin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='utilisateur.laborantin')),
            ],
        ),
        migrations.CreateModel(
            name='BilanRadiologique',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('images_radio', models.JSONField()),
                ('bilan', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='bilan_radiologique', to='dpi.bilan')),
                ('radiologue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bilans', to='utilisateur.radiologue')),
            ],
        ),
        migrations.CreateModel(
            name='BilanRadiologiqueRadiologue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bilan_rad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dpi.bilanradiologique')),
                ('radiologue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='utilisateur.radiologue')),
            ],
        ),
        migrations.CreateModel(
            name='Consultation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_de_consultation', models.DateField(auto_now_add=True)),
                ('notes', models.TextField(blank=True)),
                ('medecin_principal', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='consultations', to='utilisateur.medecin')),
            ],
        ),
        migrations.CreateModel(
            name='ConsultationMedecin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('consultation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dpi.consultation')),
                ('medecin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='utilisateur.medecin')),
            ],
        ),
        migrations.CreateModel(
            name='Dpi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qr_code', models.TextField(blank=True, max_length=500)),
                ('contact_urgence', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='dpis', to='dpi.contacturgence')),
                ('patient', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='dossier_patient', to='utilisateur.patient')),
                ('hopital_initial', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='dpi.hopital')),
            ],
        ),
        migrations.AddField(
            model_name='consultation',
            name='dpi',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='consultations', to='dpi.dpi'),
        ),
        migrations.CreateModel(
            name='Certificat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_debut', models.DateField(auto_now_add=True)),
                ('date_fin', models.DateField()),
                ('description', models.TextField(blank=True)),
                ('accorde', models.BooleanField(default=False)),
                ('medecin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='certificats', to='utilisateur.medecin')),
                ('dpi', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='certificats', to='dpi.dpi')),
            ],
        ),
        migrations.CreateModel(
            name='Antecedant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=64)),
                ('type', models.CharField(max_length=64)),
                ('dpi', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dpi.dpi')),
            ],
        ),
        migrations.CreateModel(
            name='Examen',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note', models.TextField()),
                ('traite', models.BooleanField(default=False)),
                ('consultation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dpi.consultation')),
            ],
        ),
        migrations.AddField(
            model_name='bilan',
            name='examen',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='bilan', to='dpi.examen'),
        ),
        migrations.CreateModel(
            name='GraphiqueTendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=50)),
                ('x_donnees', models.JSONField()),
                ('y_donnees', models.JSONField()),
                ('bilan_biologique', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='graphique_tendance', to='dpi.bilanbiologique')),
            ],
        ),
        migrations.CreateModel(
            name='Decompte',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tarif', models.DecimalField(decimal_places=2, max_digits=6)),
                ('date', models.DateField(auto_now_add=True)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='utilisateur.patient')),
                ('hopital', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dpi.hopital')),
            ],
        ),
        migrations.AddField(
            model_name='consultation',
            name='hopital',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dpi.hopital'),
        ),
        migrations.CreateModel(
            name='HopitalUtilisateur',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_adhesion', models.DateField(auto_now_add=True)),
                ('hopital', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dpi.hopital')),
                ('utilisateur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Hospitazliation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_entree', models.DateField()),
                ('date_sortie', models.DateField(auto_now_add=True)),
                ('cree_par', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='utilisateur.administratif')),
                ('hopital', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dpi.hopital')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='utilisateur.patient')),
            ],
        ),
        migrations.CreateModel(
            name='Ordonnance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_de_creation', models.DateField(auto_now_add=True)),
                ('consultation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ordonnances', to='dpi.consultation')),
            ],
        ),
        migrations.CreateModel(
            name='OrdonnanceMedicament',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dose', models.CharField(max_length=10)),
                ('duree', models.DecimalField(decimal_places=2, max_digits=5)),
                ('heure', models.CharField(max_length=10)),
                ('nombre_de_prises', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('medicament', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dpi.medicament')),
                ('ordonnance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dpi.ordonnance')),
            ],
        ),
        migrations.CreateModel(
            name='ConsultationOutil',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('consultation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dpi.consultation')),
                ('outil', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dpi.outil')),
            ],
        ),
        migrations.CreateModel(
            name='DpiSoin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('observation', models.TextField(blank=True)),
                ('dpi', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dpi.dpi')),
                ('soin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dpi.soin')),
            ],
        ),
    ]
