"""
Tests for the API endpoints.
Tests database interactions and prediction logging.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from api.main import MODEL, PREPROCESSOR, app
from db.database import Base, get_db

# SQLite for testing (CI friendly)
engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

# Flag: some tests require the model to be loaded
model_available = MODEL is not None and PREPROCESSOR is not None


def test_read_main():
    """Test the root health check endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert "status" in response.json()


def test_predict_invalid_data():
    """Test that incomplete data returns a 422 validation error."""
    response = client.post("/predict", json={"age": 30})
    assert response.status_code == 422  # Pydantic validation error


@pytest.mark.skipif(not model_available, reason="Model not loaded in test environment")
def test_predict_employee_not_found():
    """Test that a non-existent employee ID returns a 404."""
    response = client.get("/predict/999999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


@pytest.mark.skipif(not model_available, reason="Model not loaded in test environment")
def test_predict_by_id_success():
    """Test successful prediction by employee ID (employee 1 must exist in DB)."""
    response = client.get("/predict/1")
    assert response.status_code == 200
    data = response.json()
    assert "prediction" in data
    assert "probability" in data
    assert data["prediction"] in [0, 1]
    assert 0.0 <= data["probability"] <= 1.0
    assert data["status"] == "success"


@pytest.mark.skipif(not model_available, reason="Model not loaded in test environment")
def test_predict_post_success():
    """Test successful prediction via POST with complete employee data."""
    payload = {
        "nombre_participation_pee": 0,
        "nb_formations_suivies": 0,
        "nombre_employee_sous_responsabilite": 1,
        "employee_id": 1,
        "distance_domicile_travail": 1,
        "niveau_education": 2,
        "annees_depuis_la_derniere_promotion": 0,
        "annes_sous_responsable_actuel": 5,
        "age": 41,
        "revenu_mensuel": 5993,
        "nombre_experiences_precedentes": 8,
        "nombre_heures_travailless": 80,
        "annee_experience_totale": 8,
        "annees_dans_l_entreprise": 6,
        "annees_dans_le_poste_actuel": 4,
        "satisfaction_employee_environnement": 2,
        "note_evaluation_precedente": 3,
        "niveau_hierarchique_poste": 2,
        "satisfaction_employee_nature_travail": 4,
        "satisfaction_employee_equipe": 1,
        "satisfaction_employee_equilibre_pro_perso": 1,
        "note_evaluation_actuelle": 3,
        "heure_supplementaires": 1,
        "domaine_etude": "Infra & Cloud",
        "ayant_enfants": "Y",
        "frequence_deplacement": "Occasionnel",
        "genre": "F",
        "statut_marital": "Célibataire",
        "departement": "Commercial",
        "poste": "Cadre Commercial",
        "augementation_salaire_precedente": "11 %",
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["prediction"] in [0, 1]
    assert 0.0 <= data["probability"] <= 1.0
    assert data["status"] == "success"


def test_get_predictions_log():
    """Test the predictions log endpoint returns a list."""
    response = client.get("/predictions")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if len(data) > 0:
        entry = data[0]
        assert "id" in entry
        assert "prediction" in entry
        assert "probability" in entry
        assert "created_at" in entry
        assert "input_data" in entry
