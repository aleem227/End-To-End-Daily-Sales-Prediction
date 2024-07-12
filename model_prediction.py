from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, conint
import pandas as pd
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import load_model
import numpy as np
from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI
app = FastAPI()

# CORS settings to allow all origins, methods, and headers
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Load the trained model
model = load_model('daily_sales_count_model.h5')

# Input data model with constraints
class PredictionInput(BaseModel):
    month: conint(ge=0, le=11)  # Constrained to 0-11
    day_of_week: conint(ge=0, le=6)  # Constrained to 0-6
    product_category_name: str

# List of available product categories
available_products = [
    'moveis_quarto', 'pet_shop', 'brinquedos', 'automotivo', 'papelaria', 'ferramentas_jardim',
    'bebes', 'musica', 'fashion_bolsas_e_acessorios', 'consoles_games', 'telefonia_fixa', 'beleza_saude',
    'relogios_presentes', 'moveis_decoracao', 'cool_stuff', 'cama_mesa_banho', 'esporte_lazer',
    'eletroportateis', 'informatica_acessorios', 'utilidades_domesticas', 'telefonia', 'eletronicos',
    'perfumaria', 'market_place', 'eletrodomesticos_2', 'fashion_calcados', 'fashion_roupa_masculina',
    'fashion_underwear_e_moda_praia', 'agro_industria_e_comercio', 'climatizacao', 'fashion_roupa_feminina',
    'casa_conforto_2', 'seguros_e_servicos', 'malas_acessorios', 'moveis_cozinha_area_de_servico_jantar_e_jardim',
    'moveis_sala', 'instrumentos_musicais', 'moveis_escritorio', 'livros_interesse_geral', 'alimentos', 'pcs',
    'dvds_blu_ray', 'tablets_impressao_imagem', 'audio', 'construcao_ferramentas_construcao', 'casa_conforto',
    'construcao_ferramentas_jardim', 'casa_construcao', 'eletrodomesticos', 'livros_tecnicos', 'cine_foto',
    'construcao_ferramentas_seguranca', 'industria_comercio_e_negocios', 'artes', 'bebidas', 'fashion_esporte',
    'alimentos_bebidas', 'sinalizacao_e_seguranca', 'la_cuisine', 'construcao_ferramentas_ferramentas', 'pc_gamer',
    'livros_importados', 'artigos_de_natal', 'moveis_colchao_e_estofado', 'artes_e_artesanato',
    'fashion_roupa_infanto_juvenil', 'portateis_casa_forno_e_cafe', 'cds_dvds_musicais',
    'construcao_ferramentas_iluminacao', 'artigos_de_festas', 'flores', 'fraldas_higiene',
    'portateis_cozinha_e_preparadores_de_alimentos'
]

@app.get("/")
def read_root():
    return {"message": "App is working"}

# Predict endpoint
@app.post("/")
def predict_sales(item: PredictionInput):
    try:
        # Create a DataFrame for prediction
        input_data = {
            'month': [item.month],
            'day_of_week': [item.day_of_week],
            'product_category_name': [item.product_category_name]
        }

        # Load your original dataset to get the columns for X
        df = pd.read_csv('df.csv')

        # Features: Selecting relevant columns for prediction
        X = df[['month', 'day_of_week', 'product_category_name']]

        # One-hot encode product_category_name if needed
        X = pd.get_dummies(X, columns=['product_category_name'])

        # Create X_pred with correct columns and one-hot encoding
        X_pred = pd.DataFrame(input_data, columns=['month', 'day_of_week', 'product_category_name'])
        X_pred = pd.get_dummies(X_pred, columns=['product_category_name'])

        # Ensure X_pred has the same columns as X
        missing_cols = set(X.columns) - set(X_pred.columns)
        for col in missing_cols:
            X_pred[col] = 0

        # Reorder columns to match the order of X
        X_pred = X_pred[X.columns]

        # Scale the input features using the same scaler used during training
        scaler = StandardScaler()
        X_pred_scaled = scaler.fit_transform(X_pred)

        # Make predictions
        y_pred = model.predict(X_pred_scaled).flatten()

        # Round the predicted daily sales count based on the condition
        predicted_sales_count = y_pred[0]

        # Return the predicted daily sales count as JSON
        return {"predicted_sales_count": float(predicted_sales_count)}  # Ensure it's serializable as JSON

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Run the FastAPI server with Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app=app, port=8080)
