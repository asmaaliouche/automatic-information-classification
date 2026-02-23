import json

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from db.database import Base
from db.models import Employee, Prediction

# Use an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"



@pytest.fixture
def db_session():
    """Fixture to provide a clean in-memory database for each test."""
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, 
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)
        engine.dispose()

def test_create_employee(db_session):
    """Test creating an employee in the database."""
    employee = Employee(
        employee_id=123,
        age=30,
        genre="M",
        revenu_mensuel=5000,
        attrition_numeric=0
    )
    db_session.add(employee)
    db_session.commit()
    
    retrieved = db_session.query(Employee).filter(Employee.employee_id == 123).first()
    assert retrieved is not None
    assert retrieved.age == 30

def test_log_prediction(db_session):
    """Test logging a prediction."""
    # First create an employee to link to
    employee = Employee(employee_id=1, age=20, genre="F")
    db_session.add(employee)
    db_session.commit()
    
    prediction = Prediction(
        employee_id=1,
        input_data=json.dumps({"age": 20, "genre": "F"}),
        prediction=0,
        probability=0.2
    )
    db_session.add(prediction)
    db_session.commit()
    
    retrieved = db_session.query(Prediction).first()
    assert retrieved is not None
    assert retrieved.prediction == 0
    assert retrieved.probability == 0.2
    assert json.loads(retrieved.input_data)["age"] == 20
