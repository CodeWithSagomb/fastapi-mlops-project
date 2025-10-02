from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any

# Simule la base de données ou le registre de modèles ML
ml_models: Dict[str, Any] = {
    "logistic_model": "LOADED_LOGISTIC_REGRESSION_MODEL",
    "rf_model": "LOADED_RANDOM_FOREST_MODEL"
}

app = FastAPI(title="MLOps FastAPI Service")

# 1. Schéma de données pour la prédiction
class IrisData(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

# 2. Route de base
@app.get("/")
def read_root():
    return {"message": "Hello World"}

# 3. Route de vérification de santé (Health Check)
@app.get("/health")
def health_check():
    # En production, vous pourriez vérifier la connexion à une BDD ou à un registre de modèles.
    return {"status": "healthy"}

# 4. Route pour lister les modèles disponibles
@app.get("/models")
def list_models():
    return {"available_models": list(ml_models.keys())}


# 5. Route de prédiction (corrigée pour appeler le modèle)
@app.post("/predict/{model_name}")
def predict(model_name: str, data: IrisData):
    if model_name not in ml_models:
        raise HTTPException(status_code=404, detail=f"Model '{model_name}' not found.")
    
    # Récupérer le modèle (qui sera un MagicMock durant le test)
    model = ml_models[model_name]
    
    # Préparer les données pour la prédiction
    # Dans un vrai cas, vous pourriez avoir besoin de transformer les données
    # Ici, nous utilisons les valeurs du Pydantic model dans une liste 2D pour simuler un appel à Scikit-learn
    features = [[data.sepal_length, data.sepal_width, data.petal_length, data.petal_width]]
    
    # C'EST LA LIGNE CRUCIALE : Appeler la méthode .predict() du modèle
    # Durant le test, model.predict() retournera la valeur que vous avez définie dans le mock ([-1])
    prediction_result = model.predict(features)[0] # [0] pour prendre la première valeur

    return {"model": model_name, "prediction": prediction_result}