import base64
from datetime import date, time, timedelta
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from dpi.models import (
    Antecedant,
    BilanBiologique,
    BilanBiologiqueLaborantin,
    BilanRadiologique,
    BilanRadiologiqueRadiologue,
    Certificat,
    Consultation,
    ConsultationMedecin,
    ConsultationOutil,
    ContactUrgence,
    Decompte,
    Dpi,
    DpiSoin,
    Examen,
    GraphiqueTendance,
    Hopital,
    HopitalUtilisateur,
    Hospitalisation,
    Medicament,
    Mutuelle,
    Outil,
    Ordonnance,
    Parametre,
    ParametreValeur,
    Prescription,
    Resume,
    ResumeMesuresPrises,
    ResumeSymptomes,
    Soin,
    SoinInfermier,
    TypeBilan,
)
from utilisateur.models import (
    Administratif,
    Infermier,
    Laborantin,
    Medecin,
    Patient,
    Radiologue,
    RoleEnum,
    Utilisateur,
)


class Command(BaseCommand):
    help = "Seed database with meaningful sample data."

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset",
            action="store_true",
            help="Delete existing data before seeding.",
        )
        parser.add_argument(
            "--password",
            default="Password123!",
            help="Default password for created users.",
        )

    def handle(self, *args, **options):
        reset = options["reset"]
        password = options["password"]

        with transaction.atomic():
            if reset:
                self._reset_data()

            seed_stats = self._seed(password)

        self.stdout.write(self.style.SUCCESS("Seeding complete."))
        for label, count in seed_stats.items():
            self.stdout.write(f"- {label}: {count}")

    def _reset_data(self):
        models_in_delete_order = [
            BilanBiologiqueLaborantin,
            BilanRadiologiqueRadiologue,
            ParametreValeur,
            GraphiqueTendance,
            BilanBiologique,
            BilanRadiologique,
            Examen,
            ConsultationOutil,
            Prescription,
            Ordonnance,
            ResumeSymptomes,
            ResumeMesuresPrises,
            Resume,
            ConsultationMedecin,
            Consultation,
            DpiSoin,
            SoinInfermier,
            Mutuelle,
            Antecedant,
            Certificat,
            Hospitalisation,
            Decompte,
            ContactUrgence,
            Dpi,
            HopitalUtilisateur,
            Soin,
            Medicament,
            Outil,
            Parametre,
            Hopital,
            Patient,
            Medecin,
            Infermier,
            Radiologue,
            Laborantin,
            Administratif,
            Utilisateur,
        ]

        for model in models_in_delete_order:
            model.objects.all().delete()

    def _seed(self, password):
        stats = {}
        today = timezone.now().date()

        hopitaux = [
            self._get_or_create(
                Hopital,
                nom="Hopital Central",
                defaults={
                    "lieu": "Centre Ville",
                    "date_debut_service": today - timedelta(days=3650),
                },
            ),
            self._get_or_create(
                Hopital,
                nom="Hopital Nord",
                defaults={
                    "lieu": "Quartier Nord",
                    "date_debut_service": today - timedelta(days=2800),
                },
            ),
            self._get_or_create(
                Hopital,
                nom="Clinique Sud",
                defaults={
                    "lieu": "Quartier Sud",
                    "date_debut_service": today - timedelta(days=2200),
                },
            ),
        ]
        stats["hopitaux"] = len(hopitaux)

        users_data = {
            "patients": [
                {
                    "username": "patient_amine",
                    "email": "amine.patient@example.com",
                    "nom": "Amine",
                    "prenom": "Benali",
                    "date_naissance": date(1995, 3, 12),
                    "telephone": "0550000001",
                    "adresse": "12 Rue Atlas",
                    "role": RoleEnum.PATIENT.value,
                },
                {
                    "username": "patient_sara",
                    "email": "sara.patient@example.com",
                    "nom": "Sara",
                    "prenom": "Ouali",
                    "date_naissance": date(1992, 7, 2),
                    "telephone": "0550000002",
                    "adresse": "8 Rue Sahra",
                    "role": RoleEnum.PATIENT.value,
                },
                {
                    "username": "patient_nadir",
                    "email": "nadir.patient@example.com",
                    "nom": "Nadir",
                    "prenom": "Hamdi",
                    "date_naissance": date(1988, 11, 19),
                    "telephone": "0550000003",
                    "adresse": "5 Rue Palma",
                    "role": RoleEnum.PATIENT.value,
                },
                {
                    "username": "patient_leila",
                    "email": "leila.patient@example.com",
                    "nom": "Leila",
                    "prenom": "Boussa",
                    "date_naissance": date(1999, 1, 8),
                    "telephone": "0550000004",
                    "adresse": "4 Rue Oasis",
                    "role": RoleEnum.PATIENT.value,
                },
            ],
            "medecins": [
                {
                    "username": "med_karim",
                    "email": "karim.medecin@example.com",
                    "nom": "Karim",
                    "prenom": "Haddad",
                    "date_naissance": date(1980, 5, 20),
                    "telephone": "0550000011",
                    "adresse": "1 Rue des Palmiers",
                    "role": RoleEnum.MEDECIN.value,
                    "specialite": "cardiologie",
                },
                {
                    "username": "med_maya",
                    "email": "maya.medecin@example.com",
                    "nom": "Maya",
                    "prenom": "Rahmani",
                    "date_naissance": date(1983, 9, 14),
                    "telephone": "0550000012",
                    "adresse": "2 Rue des Roses",
                    "role": RoleEnum.MEDECIN.value,
                    "specialite": "pediatrie",
                },
                {
                    "username": "med_yacine",
                    "email": "yacine.medecin@example.com",
                    "nom": "Yacine",
                    "prenom": "Bouzid",
                    "date_naissance": date(1978, 2, 6),
                    "telephone": "0550000013",
                    "adresse": "3 Rue des Pins",
                    "role": RoleEnum.MEDECIN.value,
                    "specialite": "dermatologie",
                },
            ],
            "infermiers": [
                {
                    "username": "inf_lina",
                    "email": "lina.infermier@example.com",
                    "nom": "Lina",
                    "prenom": "Cherif",
                    "date_naissance": date(1990, 4, 21),
                    "telephone": "0550000021",
                    "adresse": "7 Rue du Port",
                    "role": RoleEnum.INFERMIER.value,
                },
                {
                    "username": "inf_sofiane",
                    "email": "sofiane.infermier@example.com",
                    "nom": "Sofiane",
                    "prenom": "Kaci",
                    "date_naissance": date(1986, 12, 3),
                    "telephone": "0550000022",
                    "adresse": "9 Rue du Lac",
                    "role": RoleEnum.INFERMIER.value,
                },
                {
                    "username": "inf_hana",
                    "email": "hana.infermier@example.com",
                    "nom": "Hana",
                    "prenom": "Zerrouki",
                    "date_naissance": date(1993, 8, 27),
                    "telephone": "0550000023",
                    "adresse": "11 Rue du Soleil",
                    "role": RoleEnum.INFERMIER.value,
                },
            ],
            "radiologues": [
                {
                    "username": "rad_rachid",
                    "email": "rachid.radiologue@example.com",
                    "nom": "Rachid",
                    "prenom": "Bena",
                    "date_naissance": date(1982, 6, 30),
                    "telephone": "0550000031",
                    "adresse": "6 Rue des Vignes",
                    "role": RoleEnum.RADIOLOGUE.value,
                },
                {
                    "username": "rad_salma",
                    "email": "salma.radiologue@example.com",
                    "nom": "Salma",
                    "prenom": "Tounsi",
                    "date_naissance": date(1987, 10, 11),
                    "telephone": "0550000032",
                    "adresse": "14 Rue de la Mer",
                    "role": RoleEnum.RADIOLOGUE.value,
                },
            ],
            "laborantins": [
                {
                    "username": "lab_ines",
                    "email": "ines.laborantin@example.com",
                    "nom": "Ines",
                    "prenom": "Gharbi",
                    "date_naissance": date(1989, 3, 9),
                    "telephone": "0550000041",
                    "adresse": "20 Rue des Fleurs",
                    "role": RoleEnum.LABORANTIN.value,
                },
                {
                    "username": "lab_mourad",
                    "email": "mourad.laborantin@example.com",
                    "nom": "Mourad",
                    "prenom": "Saidi",
                    "date_naissance": date(1984, 7, 22),
                    "telephone": "0550000042",
                    "adresse": "22 Rue des Lilas",
                    "role": RoleEnum.LABORANTIN.value,
                },
            ],
            "administratifs": [
                {
                    "username": "adm_omar",
                    "email": "omar.admin@example.com",
                    "nom": "Omar",
                    "prenom": "Neffah",
                    "date_naissance": date(1979, 1, 16),
                    "telephone": "0550000051",
                    "adresse": "30 Rue de la Gare",
                    "role": RoleEnum.ADMINISTRATIF.value,
                },
                {
                    "username": "adm_nora",
                    "email": "nora.admin@example.com",
                    "nom": "Nora",
                    "prenom": "Khelifi",
                    "date_naissance": date(1985, 9, 5),
                    "telephone": "0550000052",
                    "adresse": "31 Rue de la Gare",
                    "role": RoleEnum.ADMINISTRATIF.value,
                },
            ],
        }

        patients = [
            self._ensure_user(password=password, **data) for data in users_data["patients"]
        ]
        medecins_users = []
        for data in users_data["medecins"]:
            user_data = dict(data)
            user_data.pop("specialite", None)
            medecins_users.append(self._ensure_user(password=password, **user_data))
        infermiers_users = [
            self._ensure_user(password=password, **data)
            for data in users_data["infermiers"]
        ]
        radiologues_users = [
            self._ensure_user(password=password, **data)
            for data in users_data["radiologues"]
        ]
        laborantins_users = [
            self._ensure_user(password=password, **data)
            for data in users_data["laborantins"]
        ]
        administratifs_users = [
            self._ensure_user(password=password, **data)
            for data in users_data["administratifs"]
        ]

        stats["utilisateurs"] = (
            len(patients)
            + len(medecins_users)
            + len(infermiers_users)
            + len(radiologues_users)
            + len(laborantins_users)
            + len(administratifs_users)
        )

        medecins = []
        for data, user in zip(users_data["medecins"], medecins_users):
            medecin, _ = Medecin.objects.get_or_create(
                user=user,
                defaults={"specialite": data["specialite"]},
            )
            medecins.append(medecin)
        stats["medecins"] = len(medecins)

        infermiers = []
        for user in infermiers_users:
            infermier, _ = Infermier.objects.get_or_create(user=user)
            infermiers.append(infermier)
        stats["infermiers"] = len(infermiers)

        radiologues = []
        for user in radiologues_users:
            radiologue, _ = Radiologue.objects.get_or_create(user=user)
            radiologues.append(radiologue)
        stats["radiologues"] = len(radiologues)

        laborantins = []
        for user in laborantins_users:
            laborantin, _ = Laborantin.objects.get_or_create(user=user)
            laborantins.append(laborantin)
        stats["laborantins"] = len(laborantins)

        administratifs = []
        for user in administratifs_users:
            administratif, _ = Administratif.objects.get_or_create(user=user)
            administratifs.append(administratif)
        stats["administratifs"] = len(administratifs)

        patients_profiles = []
        for idx, user in enumerate(patients, start=1):
            patient, _ = Patient.objects.get_or_create(
                user=user,
                defaults={"NSS": f"NSS{idx:04d}"},
            )
            patients_profiles.append(patient)
        stats["patients"] = len(patients_profiles)

        for idx, user in enumerate(medecins_users):
            HopitalUtilisateur.objects.get_or_create(
                utilisateur=user,
                hopital=hopitaux[idx % len(hopitaux)],
                defaults={"date_adhesion": today - timedelta(days=300)},
            )
        for idx, user in enumerate(infermiers_users):
            HopitalUtilisateur.objects.get_or_create(
                utilisateur=user,
                hopital=hopitaux[(idx + 1) % len(hopitaux)],
                defaults={"date_adhesion": today - timedelta(days=200)},
            )
        for idx, user in enumerate(radiologues_users):
            HopitalUtilisateur.objects.get_or_create(
                utilisateur=user,
                hopital=hopitaux[(idx + 2) % len(hopitaux)],
                defaults={"date_adhesion": today - timedelta(days=180)},
            )
        for idx, user in enumerate(laborantins_users):
            HopitalUtilisateur.objects.get_or_create(
                utilisateur=user,
                hopital=hopitaux[(idx + 1) % len(hopitaux)],
                defaults={"date_adhesion": today - timedelta(days=160)},
            )
        for idx, user in enumerate(administratifs_users):
            HopitalUtilisateur.objects.get_or_create(
                utilisateur=user,
                hopital=hopitaux[idx % len(hopitaux)],
                defaults={"date_adhesion": today - timedelta(days=140)},
            )
        stats["hopital_utilisateurs"] = HopitalUtilisateur.objects.count()

        contacts = []
        for idx, patient in enumerate(patients_profiles, start=1):
            contact, _ = ContactUrgence.objects.get_or_create(
                email=f"contact{idx}@example.com",
                defaults={
                    "nom": f"Contact{idx}",
                    "prenom": f"Famille{idx}",
                    "telephone": f"05600000{idx:02d}",
                },
            )
            contacts.append(contact)
        stats["contacts_urgence"] = len(contacts)

        dpis = []
        for idx, patient in enumerate(patients_profiles):
            dpi, _ = Dpi.objects.get_or_create(
                patient=patient,
                defaults={
                    "contact_urgence": contacts[idx],
                    "hopital_initial": hopitaux[idx % len(hopitaux)],
                    "date_creation": today - timedelta(days=120),
                    "qr_code": self._encode_qr_stub(
                        f"DPI-{patient.id}-{hopitaux[idx % len(hopitaux)].id}"
                    ),
                },
            )
            dpis.append(dpi)
        stats["dpis"] = len(dpis)

        soins = [
            self._get_or_create(Soin, nom="Pansement", defaults={"type": "soin"}),
            self._get_or_create(
                Soin, nom="Injection", defaults={"type": "urgence"}
            ),
            self._get_or_create(
                Soin, nom="Perfusion", defaults={"type": "hospitalisation"}
            ),
            self._get_or_create(
                Soin, nom="Vaccination", defaults={"type": "preventif"}
            ),
        ]
        stats["soins"] = len(soins)

        for infermier in infermiers:
            for soin in soins[:2]:
                SoinInfermier.objects.get_or_create(soin=soin, infermier=infermier)
        stats["soin_infermiers"] = SoinInfermier.objects.count()

        outils = [
            self._get_or_create(Outil, nom="Stethoscope"),
            self._get_or_create(Outil, nom="Thermometre"),
            self._get_or_create(Outil, nom="Tensiometre"),
        ]
        stats["outils"] = len(outils)

        medicaments = [
            self._get_or_create(Medicament, nom="Paracetamol"),
            self._get_or_create(Medicament, nom="Amoxicilline"),
            self._get_or_create(Medicament, nom="Ibuprofene"),
            self._get_or_create(Medicament, nom="Vitamine C"),
        ]
        stats["medicaments"] = len(medicaments)

        mutuelles = []
        for idx, patient in enumerate(patients_profiles, start=1):
            mutuelle, _ = Mutuelle.objects.get_or_create(
                nom=f"Mutuelle {idx}",
                patient=patient,
            )
            mutuelles.append(mutuelle)
        stats["mutuelles"] = len(mutuelles)

        dpis_soins = []
        for idx, dpi in enumerate(dpis):
            dpi_soin, _ = DpiSoin.objects.get_or_create(
                dpi=dpi,
                soin=soins[idx % len(soins)],
                hopital=hopitaux[idx % len(hopitaux)],
                infermier=infermiers[idx % len(infermiers)],
                defaults={"observation": "Observation standard."},
            )
            dpis_soins.append(dpi_soin)
        stats["dpis_soins"] = len(dpis_soins)

        consultations = []
        for idx, dpi in enumerate(dpis):
            for offset in range(2):
                consultation, _ = Consultation.objects.get_or_create(
                    dpi=dpi,
                    medecin_principal=medecins[(idx + offset) % len(medecins)],
                    hopital=hopitaux[(idx + offset) % len(hopitaux)],
                    date_de_consultation=today - timedelta(days=10 * (idx + offset)),
                    heure=time(9 + offset, 30),
                )
                consultations.append(consultation)
        stats["consultations"] = len(consultations)

        for idx, consultation in enumerate(consultations):
            ConsultationMedecin.objects.get_or_create(
                consultation=consultation,
                medecin=medecins[(idx + 1) % len(medecins)],
            )
            ConsultationOutil.objects.get_or_create(
                consultation=consultation,
                outil=outils[idx % len(outils)],
            )
        stats["consultation_medecins"] = ConsultationMedecin.objects.count()
        stats["consultation_outils"] = ConsultationOutil.objects.count()

        resumes = []
        for idx, consultation in enumerate(consultations[:4]):
            resume, _ = Resume.objects.get_or_create(
                consultation=consultation,
                defaults={
                    "diagnostic": "Etat stable avec suivi recommande.",
                    "date_prochaine_consultation": today + timedelta(days=30),
                },
            )
            resumes.append(resume)
        for resume in resumes:
            ResumeSymptomes.objects.get_or_create(
                resume=resume,
                symptome="Fatigue",
            )
            ResumeSymptomes.objects.get_or_create(
                resume=resume,
                symptome="Maux de tete",
            )
            ResumeMesuresPrises.objects.get_or_create(
                resume=resume,
                mesure="Hydratation reguliere",
            )
            ResumeMesuresPrises.objects.get_or_create(
                resume=resume,
                mesure="Repos",
            )
        stats["resumes"] = len(resumes)
        stats["resume_symptomes"] = ResumeSymptomes.objects.count()
        stats["resume_mesures"] = ResumeMesuresPrises.objects.count()

        ordonnances = []
        for idx, consultation in enumerate(consultations):
            ordonnance, _ = Ordonnance.objects.get_or_create(
                consultation=consultation,
                defaults={"date_de_creation": today - timedelta(days=idx)},
            )
            ordonnances.append(ordonnance)
        stats["ordonnances"] = len(ordonnances)

        prescriptions = []
        for idx, ordonnance in enumerate(ordonnances):
            medicament = medicaments[idx % len(medicaments)]
            prescription, _ = Prescription.objects.get_or_create(
                ordonnance=ordonnance,
                medicament=medicament,
                defaults={
                    "dose": "500mg",
                    "duree": Decimal("5.00"),
                    "heure": time(8, 0),
                    "nombre_de_prises": 3,
                },
            )
            prescriptions.append(prescription)
        stats["prescriptions"] = len(prescriptions)

        certificats = []
        for idx, dpi in enumerate(dpis[:2]):
            certificat, _ = Certificat.objects.get_or_create(
                dpi=dpi,
                medecin=medecins[idx % len(medecins)],
                defaults={
                    "contenu": "Certificat medical de suivi.",
                    "accorde": True,
                },
            )
            certificats.append(certificat)
        stats["certificats"] = len(certificats)

        examens = []
        for idx, consultation in enumerate(consultations):
            examen_type = (
                TypeBilan.BIOLOGIQUE.value
                if idx % 2 == 0
                else TypeBilan.RADIOLOGIQUE.value
            )
            examen, _ = Examen.objects.get_or_create(
                consultation=consultation,
                type=examen_type,
                defaults={
                    "note": "Examen de suivi",
                    "traite": idx % 3 == 0,
                    "resultats": "Resultats dans la norme",
                },
            )
            examens.append(examen)
        stats["examens"] = len(examens)

        bilans_bio = []
        bilans_radio = []
        for idx, examen in enumerate(examens):
            if examen.type == TypeBilan.BIOLOGIQUE.value:
                bilan, _ = BilanBiologique.objects.get_or_create(
                    examen=examen,
                    defaults={"laborantin": laborantins[idx % len(laborantins)]},
                )
                bilans_bio.append(bilan)
            else:
                bilan, _ = BilanRadiologique.objects.get_or_create(
                    examen=examen,
                    defaults={
                        "radiologue": radiologues[idx % len(radiologues)],
                        "images_radio": [
                            "https://example.com/radio/1.png",
                            "https://example.com/radio/2.png",
                        ],
                    },
                )
                bilans_radio.append(bilan)
        stats["bilans_biologiques"] = len(bilans_bio)
        stats["bilans_radiologiques"] = len(bilans_radio)

        for idx, bilan in enumerate(bilans_bio):
            BilanBiologiqueLaborantin.objects.get_or_create(
                laborantin=laborantins[idx % len(laborantins)],
                bilan_bio=bilan,
            )
        for idx, bilan in enumerate(bilans_radio):
            BilanRadiologiqueRadiologue.objects.get_or_create(
                radiologue=radiologues[idx % len(radiologues)],
                bilan_rad=bilan,
            )
        stats["bilan_bio_laborantins"] = BilanBiologiqueLaborantin.objects.count()
        stats["bilan_radio_radiologues"] = BilanRadiologiqueRadiologue.objects.count()

        params = [
            self._get_or_create(Parametre, nom="Hemoglobine"),
            self._get_or_create(Parametre, nom="Glycemie"),
            self._get_or_create(Parametre, nom="Cholesterol"),
        ]
        stats["parametres"] = len(params)

        for bilan in bilans_bio:
            for idx, param in enumerate(params):
                ParametreValeur.objects.get_or_create(
                    parametre=param,
                    bilan_biologique=bilan,
                    defaults={"valeur": f"{12 + idx} g/dL"},
                )
        stats["parametre_valeurs"] = ParametreValeur.objects.count()

        for idx, bilan in enumerate(bilans_bio):
            GraphiqueTendance.objects.get_or_create(
                bilan_biologique=bilan,
                titre=f"Evolution {idx + 1}",
                defaults={
                    "x_donnees": ["J1", "J2", "J3"],
                    "y_donnees": [1 + idx, 2 + idx, 3 + idx],
                },
            )
        stats["graphiques"] = GraphiqueTendance.objects.count()

        for idx, dpi in enumerate(dpis):
            for offset in range(2):
                Antecedant.objects.get_or_create(
                    dpi=dpi,
                    nom=f"Antecedant {offset + 1}",
                    defaults={"type": "medical"},
                )
        stats["antecedants"] = Antecedant.objects.count()

        for idx, patient in enumerate(patients_profiles[:2]):
            Hospitalisation.objects.get_or_create(
                patient=patient,
                hopital=hopitaux[idx % len(hopitaux)],
                cree_par=administratifs[idx % len(administratifs)],
                date_entree=today - timedelta(days=7 * (idx + 1)),
                date_sortie=today - timedelta(days=2 * (idx + 1)),
            )
        stats["hospitalisations"] = Hospitalisation.objects.count()

        for idx, patient in enumerate(patients_profiles):
            for offset in range(2):
                Decompte.objects.get_or_create(
                    patient=patient,
                    hopital=hopitaux[(idx + offset) % len(hopitaux)],
                    date=today - timedelta(days=offset * 5),
                    defaults={"tarif": Decimal("250.00") + Decimal(offset * 50)},
                )
        stats["decomptes"] = Decompte.objects.count()

        return stats

    def _ensure_user(self, *, username, email, role, password, **extra_fields):
        user = (
            Utilisateur.objects.filter(email=email).first()
            or Utilisateur.objects.filter(username=username).first()
        )
        if user:
            return user

        user = Utilisateur(
            username=username,
            email=email,
            role=role,
            **extra_fields,
        )
        user.set_password(password)
        user.save()
        return user

    def _get_or_create(self, model, **kwargs):
        defaults = kwargs.pop("defaults", {})
        instance, _ = model.objects.get_or_create(defaults=defaults, **kwargs)
        return instance

    def _encode_qr_stub(self, text):
        return base64.b64encode(text.encode("utf-8")).decode("ascii")
