

from services.datasetService import dataset_completo
from services.vetorizacaoService import vetorizacao, encode_Y
from services.treinamentoService import acuracia_modelo
from services.treinamentoMsgService import acuracia_modelo_with_msg

from services.salvarmodelService import salvar_vetorizador, salvar_encoderY, salvar_modelo


def salvar_modelo_oromaxillofacialIA():
    salvar_modelo()

def salvar_vetorizador_oromaxillofacialIA():
    salvar_vetorizador()

def salvar_encoderY_oromaxillofacialIA():
    salvar_encoderY()


def salvar_todos_artefatos():
    salvar_vetorizador()
    salvar_encoderY()
    salvar_modelo()

def prints_dataset():
    df = dataset_completo()
    return df




def prints_vetorizacao():
    X_tfidf = vetorizacao()
    print(X_tfidf)

def print_encodeY():
    Y_encoded = encode_Y()
    print(Y_encoded)

def acuracia_modelo_print():

    acuracia = acuracia_modelo()
    print(f"Acurácia do modelo: {acuracia:.2f}%")

def acuracia_modelo_commsg_print():
    acuracia = acuracia_modelo_with_msg()
    print(f"Acurácia do modelo: {acuracia:.2f}%")

if __name__ == "__main__":
    #prints_vetorizacao()
    #print_encodeY()
    #acuracia_modelo_print()
    #acuracia_modelo_commsg_print()
    salvar_todos_artefatos()
