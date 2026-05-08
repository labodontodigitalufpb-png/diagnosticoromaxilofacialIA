from services.vetorizacaoService import vetorizacao, encode_Y
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
# buscar o modelo XGBoost
from xgboost import XGBClassifier as XGBoost
import time

# Função auxiliar para exibir mensagens de progresso
def exibir_progresso(mensagem, fim='\n'):
    print(f"\033[1;34m[HealthIA]\033[0m {mensagem}", end=fim)
    # Garante que a mensagem seja exibida imediatamente
    import sys
    sys.stdout.flush()

#Passo 1 - 
# Buscar os dados - X, Y

#Passo 2 - 
# Separar os dados em treino (75%) (X_treino, Y_treino) e teste (25%) (X_teste, Y_teste)

#Passo 3 - 
# Treinar o modelo com os dados de treino

#Passo 4 - 
# Avaliar o modelo com os dados de teste (Acurácia)

def buscar_dados():
    # Implementar a lógica para buscar os dados - X, Y
    exibir_progresso("\n" + "=" * 70)
    exibir_progresso("\033[1;35mIniciando o fluxo de processamento do HealthIA\033[0m")
    exibir_progresso("Este processo pode levar alguns momentos, por favor aguarde...")
    exibir_progresso("=" * 70 + "\n")
    
    exibir_progresso("Iniciando processamento dos dados...")
    exibir_progresso("Carregando e vetorizando dados de texto...", fim=' ')
    X = vetorizacao()
    print("\033[92m✓\033[0m")
    
    exibir_progresso("Codificando variáveis de diagnóstico...", fim=' ')
    Y = encode_Y()
    print("\033[92m✓\033[0m")
    
    exibir_progresso(f"Dados carregados com sucesso: {X.shape[0]} amostras com {X.shape[1]} características")
    return X, Y

def separar_dados():
    exibir_progresso("Preparando divisão dos dados para treinamento e teste...")
    
    #buscando os dados
    X, Y = buscar_dados()

    # Separar os dados em treino (70%) e teste (30%)
    exibir_progresso("Dividindo conjunto de dados: 70% para treino e 30 % para teste...", fim=' ')
    X_treino, X_teste, Y_treino, Y_teste = train_test_split(X, Y, test_size=0.3, random_state=42)
    print("\033[92m✓\033[0m")
    
    exibir_progresso(f"Conjunto de treino: {X_treino.shape[0]} amostras | Conjunto de teste: {X_teste.shape[0]} amostras")
    return X_treino, X_teste, Y_treino, Y_teste

def treinar_modelo():
    # Implementar a lógica para treinar o modelo
    exibir_progresso("Iniciando treinamento do modelo HealthIA...")
    
    # Armazenamos os dados separados para não ter que separar novamente
    dados = separar_dados()
    X_treino, X_teste, Y_treino, Y_teste = dados
    
    # Mostrar progresso de treinamento
    exibir_progresso("Configurando o modelo XGBoost...", fim=' ')
    HealthIA = XGBoost(n_estimators=150, learning_rate=0.03, max_depth=3, min_child_weight=1, random_state=42)
    print("\033[92m✓\033[0m")
    
    exibir_progresso("Treinando modelo com dados de treinamento...", fim=' ')
    inicio = time.time()
    HealthIA.fit(X_treino, Y_treino)
    tempo_treino = time.time() - inicio
    print("\033[92m✓\033[0m")
    
    exibir_progresso(f"Treinamento concluído em {tempo_treino:.2f} segundos")
    return HealthIA, X_teste, Y_teste  # Retornando também os dados de teste

def acuracia_modelo_with_msg():
    exibir_progresso("Avaliando desempenho do modelo...")
    
    # Obter o modelo treinado e os dados de teste que já foram separados
    HealthIA, X_teste, Y_teste = treinar_modelo()

    exibir_progresso("Realizando previsões com dados de teste...", fim=' ')
    inicio = time.time()
    Y_pred = HealthIA.predict(X_teste)
    tempo_previsao = time.time() - inicio
    print("\033[92m✓\033[0m")
    
    exibir_progresso(f"Previsões concluídas em {tempo_previsao:.4f} segundos")
    
    exibir_progresso("Calculando acurácia do modelo...", fim=' ')
    acuracia = accuracy_score(Y_teste, Y_pred)
    porcentagem = acuracia * 100
    print("\033[92m✓\033[0m")
    
    # Exibição visual da acurácia
    exibir_progresso("=" * 50)
    exibir_progresso(f"\033[1;32mResultado da Avaliação do Modelo\033[0m")
    exibir_progresso("=" * 50)
    exibir_progresso(f"Acurácia do modelo: \033[1;33m{porcentagem:.2f}%\033[0m")
    
    # Classificação da acurácia
    if porcentagem >= 90:
        exibir_progresso("\033[1;32mExcelente acurácia!\033[0m")
    elif porcentagem >= 80:
        exibir_progresso("\033[1;32mBoa acurácia\033[0m")
    elif porcentagem >= 70:
        exibir_progresso("\033[1;33mAcurácia aceitável\033[0m")
    else:
        exibir_progresso("\033[1;31mAcurácia abaixo do esperado - considere ajustes no modelo\033[0m")
    
    exibir_progresso("=" * 50)
    exibir_progresso("\n\033[1;35mProcessamento completo! O modelo HealthIA está pronto para uso.\033[0m\n")

    return porcentagem 
