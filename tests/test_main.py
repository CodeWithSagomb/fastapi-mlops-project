from unittest.mock import MagicMock
import pytest
from fastapi.testclient import TestClient

# Importer l'objet app de notre application
from app.main import app 

# --- Tests des routes simples ---

def test_root():
    with TestClient(app) as client:
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Hello World"}


def test_health_check():
    with TestClient(app) as client:
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}


def test_list_models():
    with TestClient(app) as client:
        response = client.get("/models")
        assert response.status_code == 200
        assert response.json() == {"available_models": ["logistic_model", "rf_model"]}


# --- Tests de prédiction avec Mocking ---

@pytest.fixture
def mock_models_in_app(mocker):
    """
    Fixture qui moque le dictionnaire 'ml_models' dans app/main.py.
    Ceci remplace les vrais modèles par des objets MagicMock avant les tests.
    """
    mock_dict = {
        "logistic_model": MagicMock(), 
        "rf_model": MagicMock()
    }
    mocker.patch(
        "app.main.ml_models", # Le chemin vers la variable à remplacer
        new=mock_dict,       # La nouvelle valeur
    )
    return mock_dict # Retourne le dictionnaire moqué si on veut interagir avec

def test_predict_model_not_found(mock_models_in_app):
    with TestClient(app) as client:
        response = client.post(
            "/predict/invalid_model",
            json={
                "sepal_length": 5.1,
                "sepal_width": 3.5,
                "petal_length": 1.4,
                "petal_width": 0.2,
            },
        )
        assert response.status_code == 404
        assert response.json()["detail"] == "Model 'invalid_model' not found."


def test_predict_mocked(mock_models_in_app):
    # Simuler le résultat de la fonction predict() du modèle
    mock_models_in_app["logistic_model"].predict.return_value = [-1]

    with TestClient(app) as client:
        response = client.post(
            "/predict/logistic_model",
            json={
                "sepal_length": 5.1,
                "sepal_width": 3.5,
                "petal_length": 1.4,
                "petal_width": 0.2,
            },
        )

        assert response.status_code == 200
        assert response.json() == {"model": "logistic_model", "prediction": -1}
        
        # Vérifie que la fonction .predict() a été appelée une fois
        mock_models_in_app["logistic_model"].predict.assert_called_once()