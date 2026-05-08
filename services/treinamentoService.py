from services.datasetService import dataset_completo
from services.config import COL_CLASSE, COL_TEXTO
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import ComplementNB
from sklearn.pipeline import Pipeline



#Passo 1 - 
# Buscar os dados - X, Y

#Passo 2 - 
# Separar os dados em treino (75%) (X_treino, Y_treino) e teste (25%) (X_teste, Y_teste)


#Passo 3 - 
# Treinar o modelo com os dados de treino

#Passo 4 - 
# Avaliar o modelo com os dados de teste (Acurácia)

def buscar_dados():
    df = dataset_completo()
    X = df[COL_TEXTO].astype(str)
    Y = df[COL_CLASSE].astype(str)
    return X, Y

def separar_dados():
    
    #buscando os dadps
    X, Y = buscar_dados()

    # Separar os dados em treino (70%) e teste (30%)
    X_treino, X_teste, Y_treino, Y_teste = train_test_split(
        X,
        Y,
        test_size=0.3,
        random_state=42,
        stratify=Y,
    )
    return X_treino, X_teste, Y_treino, Y_teste

def treinar_modelo():
    """
    Função para treinar o modelo de Machine Learning, com o algoritmo XGBoost.

    Return:
    model: XGBClassifier
        O modelo treinado - que se chama HealthIA.
    """
    # Implementar a lógica para treinar o modelo

    X_treino, _, Y_treino, _ = separar_dados()
    
    HealthIA = Pipeline(
        steps=[
            ("tfidf", TfidfVectorizer(ngram_range=(1, 2), sublinear_tf=True)),
            ("classifier", ComplementNB()),
        ]
    )
    HealthIA.fit(X_treino, Y_treino)

    return HealthIA

def acuracia_modelo():

    HealthIA = treinar_modelo()
    _, X_teste, _, Y_teste = separar_dados()

   
    Y_pred = HealthIA.predict(X_teste)
    acuracia = accuracy_score(Y_teste, Y_pred)

    porcentagem = acuracia * 100

    return porcentagem 
