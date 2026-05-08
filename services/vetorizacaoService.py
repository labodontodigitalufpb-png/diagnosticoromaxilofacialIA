from sklearn.feature_extraction.text import TfidfVectorizer
from services.datasetService import dataset_completo
from services.config import COL_CLASSE, COL_TEXTO
from sklearn.preprocessing import LabelEncoder



# 1 - chamar o framework que tem o TF-IDF - ok
# 2 - instanciar o modelo de vetorização - ok
# 3 - Pegar os dados e vetorizar


# Vetorizador
def vetorizador():
    """
    Funcao que cria um vetorizador TF-IDF e o ajusta aos dados de entrada.

    Returns:
        Vetorizador ajustado com os dados pronto para ser usado.
    """
    tfidf = TfidfVectorizer(ngram_range=(1, 2), sublinear_tf=True)

    df = dataset_completo()
    
    X = df[COL_TEXTO].astype(str)

    tfidf.fit(X)
    
    return tfidf

#Vetorizador vetorizando os Dados
# retorno Dados Vetorizados
def vetorizacao():
    tfidf = TfidfVectorizer(ngram_range=(1, 2), sublinear_tf=True)

    df = dataset_completo()
    X = df[COL_TEXTO].astype(str)

    tfidf.fit(X)

    X_tfidf = tfidf.transform(X)

    return X_tfidf

def encoder_Y():
    """
    Função para ajustar o encoder da variável alvo (Y).

    Return:
    label_encoder: LabelEncoder
        Encoder ajustado com os rótulos do dataset.
    """
    label_encoder = LabelEncoder()
    df = dataset_completo()

    Y = df[COL_CLASSE].astype(str)

    label_encoder.fit(Y)

    return label_encoder


def encode_Y():
    """
    Função para codificar a variável alvo (Y) usando Label Encoding.

    Return:
    Y_encoded: array
        Array com os rótulos codificados.
    """
    df = dataset_completo()
    Y = df[COL_CLASSE].astype(str)

    return encoder_Y().transform(Y)










