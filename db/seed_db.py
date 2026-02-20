"""
Script to seed the PostgreSQL database with the employee dataset.

Usage:
    poetry run python -m db.seed_db

This script:
    1. Reads the combined_df.csv file.
    2. Inserts all employee records into the 'employees' table.
    3. Skips any employees that already exist (based on employee_id).
"""

import pandas as pd

from db.database import SessionLocal
from db.models import Employee


DATA_PATH = "data/combined_df.csv"


def seed_employees():
    """Load the CSV dataset and insert all employees into the database."""
    print(f"📂 Reading dataset from {DATA_PATH}...")
    df = pd.read_csv(DATA_PATH)
    print(f"  Found {len(df)} records.")

    db = SessionLocal()
    inserted = 0
    skipped = 0

    try:
        for _, row in df.iterrows():
            # Check if employee already exists
            existing = (
                db.query(Employee)
                .filter(Employee.employee_id == int(row["employee_id"]))
                .first()
            )
            if existing:
                skipped += 1
                continue

            employee = Employee(
                employee_id=int(row["employee_id"]),
                a_quitte_l_entreprise=row["a_quitte_l_entreprise"],
                attrition_numeric=int(row["attrition_numeric"]),
                nombre_participation_pee=int(row["nombre_participation_pee"]),
                nb_formations_suivies=int(row["nb_formations_suivies"]),
                nombre_employee_sous_responsabilite=int(row["nombre_employee_sous_responsabilite"]),
                distance_domicile_travail=int(row["distance_domicile_travail"]),
                niveau_education=int(row["niveau_education"]),
                annees_depuis_la_derniere_promotion=int(
                    row["annees_depuis_la_derniere_promotion"]
                ),
                annes_sous_responsable_actuel=int(row["annes_sous_responsable_actuel"]),
                age=int(row["age"]),
                revenu_mensuel=int(row["revenu_mensuel"]),
                nombre_experiences_precedentes=int(row["nombre_experiences_precedentes"]),
                nombre_heures_travailless=int(row["nombre_heures_travailless"]),
                annee_experience_totale=int(row["annee_experience_totale"]),
                annees_dans_l_entreprise=int(row["annees_dans_l_entreprise"]),
                annees_dans_le_poste_actuel=int(row["annees_dans_le_poste_actuel"]),
                satisfaction_employee_environnement=int(
                    row["satisfaction_employee_environnement"]
                ),
                note_evaluation_precedente=int(row["note_evaluation_precedente"]),
                niveau_hierarchique_poste=int(row["niveau_hierarchique_poste"]),
                satisfaction_employee_nature_travail=int(
                    row["satisfaction_employee_nature_travail"]
                ),
                satisfaction_employee_equipe=int(row["satisfaction_employee_equipe"]),
                satisfaction_employee_equilibre_pro_perso=int(
                    row["satisfaction_employee_equilibre_pro_perso"]
                ),
                note_evaluation_actuelle=int(row["note_evaluation_actuelle"]),
                heure_supplementaires=row["heure_supplementaires"],
                domaine_etude=row["domaine_etude"],
                ayant_enfants=row["ayant_enfants"],
                frequence_deplacement=row["frequence_deplacement"],
                genre=row["genre"],
                statut_marital=row["statut_marital"],
                departement=row["departement"],
                poste=row["poste"],
                augementation_salaire_precedente=row["augementation_salaire_precedente"],
            )
            db.add(employee)
            inserted += 1

        db.commit()
        print(f"\n✅ Seeding complete: {inserted} inserted, {skipped} skipped (already exist).")

    except Exception as e:
        db.rollback()
        print(f"❌ Error during seeding: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_employees()
