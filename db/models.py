"""
SQLAlchemy ORM models for the TechNova Attrition database.

Tables:
    - employees: Stores the full employee dataset from the CSV.
    - predictions: Logs every ML prediction with input data and results.
"""

from datetime import datetime, timezone

from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from db.database import Base


class Employee(Base):
    """Employee table — mirrors the combined_df.csv dataset."""

    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, autoincrement=True)
    employee_id = Column(Integer, unique=True, nullable=False, index=True)

    # Target variable
    a_quitte_l_entreprise = Column(String(10))
    attrition_numeric = Column(Integer)

    # Numerical features
    nombre_participation_pee = Column(Integer)
    nb_formations_suivies = Column(Integer)
    nombre_employee_sous_responsabilite = Column(Integer)
    distance_domicile_travail = Column(Integer)
    niveau_education = Column(Integer)
    annees_depuis_la_derniere_promotion = Column(Integer)
    annes_sous_responsable_actuel = Column(Integer)
    age = Column(Integer)
    revenu_mensuel = Column(Integer)
    nombre_experiences_precedentes = Column(Integer)
    nombre_heures_travailless = Column(Integer)
    annee_experience_totale = Column(Integer)
    annees_dans_l_entreprise = Column(Integer)
    annees_dans_le_poste_actuel = Column(Integer)
    satisfaction_employee_environnement = Column(Integer)
    note_evaluation_precedente = Column(Integer)
    niveau_hierarchique_poste = Column(Integer)
    satisfaction_employee_nature_travail = Column(Integer)
    satisfaction_employee_equipe = Column(Integer)
    satisfaction_employee_equilibre_pro_perso = Column(Integer)
    note_evaluation_actuelle = Column(Integer)
    heure_supplementaires = Column(String(10))

    # Categorical features
    domaine_etude = Column(String(100))
    ayant_enfants = Column(String(5))
    frequence_deplacement = Column(String(50))
    genre = Column(String(5))
    statut_marital = Column(String(50))
    departement = Column(String(100))
    poste = Column(String(100))
    augementation_salaire_precedente = Column(String(20))

    # Relationship
    predictions = relationship("Prediction", back_populates="employee")

    def __repr__(self):
        return f"<Employee(employee_id={self.employee_id}, age={self.age})>"


class Prediction(Base):
    """Prediction log table — records every ML model interaction."""

    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    employee_id = Column(
        Integer, ForeignKey("employees.employee_id"), nullable=True, index=True
    )
    input_data = Column(Text, nullable=False)  # JSON string of the input features
    prediction = Column(Integer, nullable=False)  # 0 = stays, 1 = leaves
    probability = Column(Float, nullable=False)  # probability of attrition
    created_at = Column(
        DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )

    # Relationship
    employee = relationship("Employee", back_populates="predictions")

    def __repr__(self):
        return (
            f"<Prediction(id={self.id}, employee_id={self.employee_id}, "
            f"prediction={self.prediction}, probability={self.probability:.2f})>"
        )
