from pydantic import BaseModel, Field


class EmployeeData(BaseModel):
    # Numerical features
    nombre_participation_pee: float
    nb_formations_suivies: float
    nombre_employee_sous_responsabilite: float
    employee_id: float
    distance_domicile_travail: float
    niveau_education: float
    annees_depuis_la_derniere_promotion: float
    annes_sous_responsable_actuel: float
    age: float
    revenu_mensuel: float
    nombre_experiences_precedentes: float
    nombre_heures_travailless: float
    annee_experience_totale: float
    annees_dans_l_entreprise: float
    annees_dans_le_poste_actuel: float
    satisfaction_employee_environnement: float
    note_evaluation_precedente: float
    niveau_hierarchique_poste: float
    satisfaction_employee_nature_travail: float
    satisfaction_employee_equipe: float
    satisfaction_employee_equilibre_pro_perso: float
    note_evaluation_actuelle: float
    heure_supplementaires: int = Field(..., description="0 for No, 1 for Yes")

    # Categorical features
    domaine_etude: str
    ayant_enfants: str
    frequence_deplacement: str
    genre: str
    statut_marital: str
    departement: str
    poste: str
    augementation_salaire_precedente: str

class PredictionResponse(BaseModel):
    prediction: int
    probability: float
    status: str = "success"
