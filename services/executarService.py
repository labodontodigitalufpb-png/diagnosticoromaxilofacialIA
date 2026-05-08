
import numpy as np
import joblib
from services.config import ENCODER_PATH, MODEL_ACCURACY, MODEL_NAME, MODEL_PATH, VECTORIZER_PATH
from services.datasetService import condutas_por_diagnostico
from services.rules.achados_parser import achados_from_texto
from services.rules.motor_regras import aplicar_perfis, explicar_compatibilidade, top_n


class DiagnosticoIA:
    def __init__(
        self,
        model_path: str = str(MODEL_PATH),
        vectorizer_path: str = str(VECTORIZER_PATH),
        encoder_path: str = str(ENCODER_PATH),
    ):
        self.vet = joblib.load(vectorizer_path)
        self.enc = joblib.load(encoder_path)
        self.model = joblib.load(model_path)
        self.condutas = condutas_por_diagnostico()

    def _conduta_para_hipoteses(self, top3):
        if not top3:
            return None, []

        condutas_hipoteses = []
        for hipotese in top3:
            diagnostico = hipotese["doenca"]
            conduta = self.condutas.get(diagnostico, {})
            if conduta:
                condutas_hipoteses.append({
                    "doenca": diagnostico,
                    "prob_percent": hipotese["prob_percent"],
                    **conduta,
                })

        principal = condutas_hipoteses[0] if condutas_hipoteses else None
        return principal, condutas_hipoteses

    def predict_simples(self, sintomas_list):
        """
        Retorna Top-3 hipóteses com percentuais (probabilidades reais do modelo).
        """
        sintomas_list = [str(s).strip() for s in (sintomas_list or []) if str(s).strip()]
        if not sintomas_list:
            return {
                "sintomas_recebidos": [],
                "diagnostico_provavel": "Nenhum sintoma informado",
                "top3": [],
                "top2": [],
                "conduta_proposta": None,
                "condutas_por_hipotese": [],
                "acuracia_modelo": MODEL_ACCURACY,
                "modelo": "TF-IDF + ComplementNB",
            }

        texto = ", ".join(sintomas_list)
        probs = self.model.predict_proba([texto])[0]
        scores_modelo = {
            str(label): float(prob)
            for label, prob in zip(self.model.classes_, probs)
        }
        achados = achados_from_texto(sintomas_list)
        scores_hibridos = aplicar_perfis(scores_modelo, achados)
        top_hibrido = top_n(scores_hibridos, n=3)

        top3 = []
        for lbl, score in top_hibrido:
            top3.append({
                "doenca": str(lbl),
                "prob_percent": round(float(score) * 100, 2),
                "prob_modelo_percent": round(scores_modelo.get(str(lbl), 0) * 100, 2),
            })

        diagnostico_previsto = top3[0]["doenca"] if top3 else "Classe desconhecida"
        conduta_proposta, condutas_por_hipotese = self._conduta_para_hipoteses(top3)
        explicacoes = [
            explicar_compatibilidade(item["doenca"], achados)
            for item in top3
        ]

        return {
            "sintomas_recebidos": sintomas_list,
            "diagnostico_provavel": str(diagnostico_previsto),
            "top3": top3,
            "top2": top3[:2],
            "conduta_proposta": conduta_proposta,
            "condutas_por_hipotese": condutas_por_hipotese,
            "explicacoes_regras": explicacoes,
            "acuracia_modelo": MODEL_ACCURACY,
            "modelo": "Híbrido: TF-IDF + ComplementNB + perfis semiológicos",
            "nome_modelo": MODEL_NAME,
        }
