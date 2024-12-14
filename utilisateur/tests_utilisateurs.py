import pytest
from django.contrib.auth import get_user_model
from utilisateur.models import Medecin, Patient, Administratif, Infermier, Radiologue, Laborantin

@pytest.mark.django_db
def test_creation_instance_utilisateur():
    utilisateur = get_user_model().objects.create_user(
        username="Nazim0710",
        email="mn_aouni@esi.dz",
        password="nazimaouninazim",
        nom="Nazim",
        prenom="Aouni",
        date_naissance="2004-07-10",
        telephone="0776967572",
    )
    assert utilisateur.nom == "Nazim"
    assert utilisateur.prenom == "Aouni"
    assert utilisateur.date_naissance == "2004-07-10"
    assert utilisateur.telephone == "0776967572"
    assert utilisateur.email == "mn_aouni@esi.dz"

@pytest.mark.django_db
def test_creation_instance_medecin():
    utilisateur = get_user_model().objects.create_user(
        username="Nazim0710",
        email="mn_aouni@esi.dz",
        password="nazimaouninazim",
        nom="Nazim",
        prenom="Aouni",
        date_naissance="2004-07-10",
        telephone="0776967572",
    )
    medecin = Medecin.objects.create(user=utilisateur, specialite="Cardiologie")
    assert medecin.user.nom == "Nazim"
    assert medecin.specialite == "Cardiologie"

@pytest.mark.django_db
def test_creation_instance_patient():
    utilisateur = get_user_model().objects.create_user(
        username="Nazim0710",
        email="mn_aouni@esi.dz",
        password="nazimaouninazim",
        nom="Nazim",
        prenom="Aouni",
        date_naissance="2004-07-10",
        telephone="0776967572",
    )
    patient = Patient.objects.create(
        user=utilisateur,
        NSS="123456789",
        mutuelle="Yes",
        contact_urgence="0987654321",
    )
    assert patient.user.nom == "Nazim"
    assert patient.NSS == "123456789"
    assert patient.contact_urgence == "0987654321"

@pytest.mark.django_db
def test_creation_instance_administratif():
    utilisateur = get_user_model().objects.create_user(
        username="Nazim0710",
        email="mn_aouni@esi.dz",
        password="nazimaouninazim",
        nom="Nazim",
        prenom="Aouni",
        date_naissance="2004-07-10",
        telephone="0776967572",
    )
    administratif = Administratif.objects.create(user=utilisateur)
    assert administratif.user.nom == "Nazim"

@pytest.mark.django_db
def test_creation_instance_infermier():
    utilisateur = get_user_model().objects.create_user(
        username="Nazim0710",
        email="mn_aouni@esi.dz",
        password="nazimaouninazim",
        nom="Nazim",
        prenom="Aouni",
        date_naissance="2004-07-10",
        telephone="0776967572",
    )
    infermier = Infermier.objects.create(user=utilisateur)
    assert infermier.user.nom == "Nazim"

@pytest.mark.django_db
def test_creation_instance_radiologue():
    utilisateur = get_user_model().objects.create_user(
        username="Nazim0710",
        email="mn_aouni@esi.dz",
        password="nazimaouninazim",
        nom="Nazim",
        prenom="Aouni",
        date_naissance="2004-07-10",
        telephone="0776967572",
    )
    radiologue = Radiologue.objects.create(user=utilisateur)
    assert radiologue.user.nom == "Nazim"

@pytest.mark.django_db
def test_creation_instance_laborantin():
    utilisateur = get_user_model().objects.create_user(
        username="Nazim0710",
        email="mn_aouni@esi.dz",
        password="nazimaouninazim",
        nom="Nazim",
        prenom="Aouni",
        date_naissance="2004-07-10",
        telephone="0776967572",
    )
    laborantin = Laborantin.objects.create(user=utilisateur)
    assert laborantin.user.nom == "Nazim"
