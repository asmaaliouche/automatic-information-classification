"""
Tests for the API endpoints.
Tests database interactions and prediction logging.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from api.main import app
from db.database import Base, get_db
from db.models import Employee

# SQLite for testing (Single connection pool for :memory:)
engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

# Override database dependency
@pytest.fixture(scope="module")
def db_session():
    """Fixture to provide a clean in-memory database per test module."""
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    
    # 1. Seed the database with a test employee (Employee 1)
    # This is necessary for test_predict_by_id_success
    test_employee = Employee(
        employee_id=1,
        age=41,
        distance_domicile_travail=1,
        niveau_education=2,
        revenu_mensuel=5993,
        nombre_experiences_precedentes=8,
        annee_experience_totale=8,
        annees_dans_l_entreprise=6,
        annees_dans_le_poste_actuel=4,
        annees_depuis_la_derniere_promotion=0,
        annes_sous_responsable_actuel=5,
        satisfaction_employee_environnement=2,
        satisfaction_employee_nature_travail=4,
        satisfaction_employee_equilibre_pro_perso=1,
        heure_supplementaires="Oui",
        statut_marital="Célibataire",
        genre="F",
        poste="Cadre Commercial"
        # ... include rest if needed, but these often suffice for tests
    )
    session.add(test_employee)
    session.commit()
    
    yield session
    
    session.close()
    Base.metadata.drop_all(bind=engine)
    engine.dispose()

@pytest.fixture(scope="module")
def client():
    """Fixture to provide a TestClient that triggers the lifespan (model loading)."""
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c

# Test credentials
HEADERS = {"access_token": "futurisys-token-debug"}

def test_read_main(client):
    """Test the root health check endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert "status" in response.json()

def test_predict_invalid_data(client):
    """Test that incomplete data returns a 422 validation error."""
    # Note: validation happens AFTER security check in FastAPI dependencies
    response = client.post("/predict", json={"age": 30}, headers=HEADERS)
    assert response.status_code == 422

def test_predict_employee_not_found(client):
    """Test that a non-existent employee ID returns a 404."""
    response = client.get("/predict/999999", headers=HEADERS)
    assert response.status_code == 404

def test_predict_by_id_success(client, db_session):
    """Test successful prediction by employee ID."""
    # Ensure Employee 1 exists (seeded in db_session fixture)
    response = client.get("/predict/1", headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert "prediction" in data
    assert "probability" in data
    assert data["status"] == "success"

def test_predict_post_success(client):
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
    response = client.post("/predict", json=payload, headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"

def test_get_predictions_log(client, db_session):
    """Test the predictions log endpoint returns a list."""
    response = client.get("/predictions", headers=HEADERS)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
