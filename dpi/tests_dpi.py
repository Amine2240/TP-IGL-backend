import pytest
from datetime import date
from django.utils import timezone
from utilisateur.models import (
    Administratif,
    Laborantin,
    Medecin,
    Patient,
    Radiologue,
    Utilisateur,
    RoleEnum, 
)
from .models import *

@pytest.mark.django_db
def init1(name):
    utilisateur = Utilisateur.objects.create(
        username=name,
        nom="Doe",
        prenom="John",
        date_naissance=timezone.now().date(),
        telephone="0123456789",
        role=RoleEnum.PATIENT.value,  
    )
    return utilisateur
 

@pytest.mark.django_db
def init2():
    utilisateur = init1("Doe")
    patient = Patient.objects.create(
        user=utilisateur,
        NSS="12345678901245",
        mutuelle=None,
        contact_urgence=None,
    )
    return patient

@pytest.mark.django_db
def init3():
    utilisateur=init1("House")
    medecin = Medecin.objects.create(
        user=utilisateur,
        specialite="Generalist"
    )
    return medecin

@pytest.mark.django_db
def test_creation_instance_dpi():
    hopital = Hopital.objects.create(id=1, nom="Hopital A", lieu="Lieu A", date_debut_service=date.today())
    patient = init2()
    dpi = Dpi.objects.create(id=1, patient=patient, hopital_initial=hopital)
    assert dpi.patient == patient
    assert dpi.hopital_initial == hopital

@pytest.mark.django_db
def test_creation_instance_mutuelle():
    mutuelle = Mutuelle.objects.create(nom="CAAT")
    assert mutuelle.nom == "CAAT"

@pytest.mark.django_db
def test_creation_instance_soin():
    hopital = Hopital.objects.create(nom="Hopital A", lieu="Lieu A", date_debut_service=date.today())
    patient = init2()
    dpi = Dpi.objects.create(patient=patient, hopital_initial=hopital)
    soin = Soin.objects.create(dpi=dpi, type_soin="Consultation", coup=150.00)
    assert soin.dpi == dpi
    assert soin.type_soin == "Consultation"

@pytest.mark.django_db
def test_creation_instance_outil():
    outil = Outil.objects.create(nom="Stethoscope")
    assert outil.nom == "Stethoscope"

@pytest.mark.django_db
def test_creation_instance_consultation():
    hopital = Hopital.objects.create(nom="Hopital A", lieu="Lieu A", date_debut_service=date.today())
    patient = init2()
    dpi = Dpi.objects.create(patient=patient, hopital_initial=hopital)
    consultation = Consultation.objects.create(dpi=dpi, hopital=hopital, date_de_consultation=date.today())
    assert consultation.dpi == dpi
    assert consultation.hopital == hopital

@pytest.mark.django_db
def test_creation_instance_medicament():
    medicament = Medicament.objects.create(nom="Ibuprofen")
    assert medicament.nom == "Ibuprofen"

@pytest.mark.django_db
def test_creation_instance_ordonnance():
    hopital = Hopital.objects.create(nom="Hopital A", lieu="Lieu A", date_debut_service=date.today())
    patient = init2()
    dpi = Dpi.objects.create(patient=patient, hopital_initial=hopital)
    consultation = Consultation.objects.create(dpi=dpi, hopital=hopital, date_de_consultation=date.today())
    medicament = Medicament.objects.create(nom="Ibuprofen")
    prescription = Prescription.objects.create(medicament=medicament, dose="500mg")
    ordonnance = Ordonnance.objects.create(consultation=consultation, prescription=prescription)
    assert ordonnance.consultation == consultation
    assert ordonnance.prescription == prescription

@pytest.mark.django_db
def test_creation_instance_certificat():
    hopital = Hopital.objects.create(nom="Hopital A", lieu="Lieu A", date_debut_service=date.today())
    patient = init2()
    dpi = Dpi.objects.create(patient=patient, hopital_initial=hopital)
    medecin = init3()
    certificat = Certificat.objects.create(dpi=dpi, medecin=medecin, contenu="Certificat médical valide.")
    assert certificat.dpi == dpi
    assert certificat.medecin == medecin

@pytest.mark.django_db
def test_creation_instance_examen():
    hopital = Hopital.objects.create(nom="Hopital A", lieu="Lieu A", date_debut_service=date.today())
    patient = init2()
    dpi = Dpi.objects.create(patient=patient, hopital_initial=hopital)
    consultation = Consultation.objects.create(dpi=dpi, hopital=hopital, date_de_consultation=date.today())
    examen = Examen.objects.create(consultation=consultation, note="Observation médicale importante.")
    assert examen.consultation == consultation

@pytest.mark.django_db
def test_creation_instance_bilan():
    hopital = Hopital.objects.create(nom="Hopital A", lieu="Lieu A", date_debut_service=date.today())
    patient = init2()
    dpi = Dpi.objects.create(patient=patient, hopital_initial=hopital)
    consultation = Consultation.objects.create(dpi=dpi, hopital=hopital, date_de_consultation=date.today())
    examen = Examen.objects.create(consultation=consultation, note="Observation.")
    bilan = Bilan.objects.create(examen=examen, type="biologique", resultats="Normaux")
    assert bilan.examen == examen
