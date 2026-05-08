from services.config import ENCODER_PATH, MODEL_DIR, MODEL_PATH, VECTORIZER_PATH
from services.vetorizacaoService import encoder_Y, vetorizador
from services.treinamentoService import treinar_modelo
import joblib


# Salvar o vetorizador
# Salvar o Encoder (Label Y)
# Salvar o modelo treinado



def salvar_vetorizador():
    """
    Salvar o vetorizador como arquivo no diretorio model      
    
    """
    vetorizador_criado = vetorizador()
    MODEL_DIR.mkdir(parents=True, exist_ok=True)

    joblib.dump(vetorizador_criado, VECTORIZER_PATH)
    print("Vetorizador salvo com sucesso!")


def salvar_encoderY():
    """
    Salvar o encoder Y como arquivo no diretorio model
    """
    encoderY_criado = encoder_Y()
    MODEL_DIR.mkdir(parents=True, exist_ok=True)

    joblib.dump(encoderY_criado, ENCODER_PATH)
    print("Encoder Y salvo com sucesso!")

def salvar_modelo():

    """
    Salvar o modelo treinado como arquivo no diretorio model
    """
    HealthIA = treinar_modelo()
    MODEL_DIR.mkdir(parents=True, exist_ok=True)

    joblib.dump(HealthIA, MODEL_PATH)
    print("Modelo salvo com sucesso!")
