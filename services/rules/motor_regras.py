# motor_regras.py
from services.rules.perfis_diagnosticos import PERFIS_DIAGNOSTICOS

MALIGNAS = {
    "carcinoma_ameloblastico",
    "carcinoma_intraosseo_primario",
    "carcinoma_odontogenico_esclerosante",
    "carcinoma_odontogenico_celulas_claras",
    "sarcoma_odontogenico",
    "metastase_ossea_gnatica",
    "mieloma_multiplo",
    "linfoma_osseo",
}

def normalizar(scores):
    total = sum(v for v in scores.values() if v > 0)
    if total <= 0:
        n = len(scores) or 1
        return {k: 1 / n for k in scores}
    return {k: max(v, 0) / total for k, v in scores.items()}

def enriquecer_achados(achados):
    """Cria achados compostos usados nos perfis.
    O app pode enviar os achados simples; esta função monta combinações clínicas úteis.
    """
    a = dict(achados)

    a["radiopaco_ou_misto"] = a.get("radiopaco", False) or a.get("misto", False) or a.get("predominantemente_radiopaco", False)
    a["radiolucido_ou_misto"] = a.get("radiolucido", False) or a.get("misto", False) or a.get("predominantemente_radiolucido", False)
    a["radiolucido_puro"] = a.get("radiolucido", False) and not a.get("misto", False) and not a.get("radiopaco", False)
    a["radiopaco_puro"] = a.get("radiopaco", False) and not a.get("misto", False) and not a.get("radiolucido", False)

    a["posterior_mandibula"] = a.get("mandibula", False) and (
        a.get("posterior", False) or a.get("molar", False) or a.get("angulo_mandibular", False) or a.get("ramo_mandibular", False)
    )
    a["mandibula_posterior"] = a["posterior_mandibula"]
    a["maxila_posterior"] = a.get("maxila", False) and (a.get("posterior", False) or a.get("molar", False) or a.get("seio_maxilar", False))
    a["anterior_maxila"] = a.get("maxila", False) and (a.get("anterior", False) or a.get("incisivo", False) or a.get("canino", False))
    a["mandibula_premolar"] = a.get("mandibula", False) and a.get("premolar", False)
    a["gengiva_canino_premolar"] = a.get("gengiva", False) and (a.get("canino", False) or a.get("premolar", False))
    a["mandibula_premolar_molar"] = a.get("mandibula", False) and (a.get("premolar", False) or a.get("molar", False))
    a["mandibula_molar"] = a.get("mandibula", False) and a.get("molar", False)

    a["adulto_jovem"] = a.get("idade_20_40", False) or a.get("adulto_jovem", False)
    a["paciente_jovem"] = a.get("crianca", False) or a.get("adolescente", False) or a.get("idade_10_30", False) or a.get("paciente_jovem", False)
    a["paciente_crianca_adolescente"] = a.get("crianca", False) or a.get("adolescente", False)
    a["adulto_idoso"] = a.get("idade_maior_50", False) or a.get("idoso", False)
    a["homem_adulto"] = a.get("sexo_masculino", False) and (a.get("adulto", False) or a.get("idade_maior_30", False))
    a["mulher_adulta"] = a.get("sexo_feminino", False) and (a.get("adulto", False) or a.get("idade_maior_30", False))

    a["expansao_bicortical"] = a.get("expansao_cortical_vestibular", False) and a.get("expansao_cortical_lingual", False)
    a["sem_expansao"] = not a.get("expansao_cortical", False) and not a.get("expansao_bicortical", False)
    a["destruicao_cortical_difusa"] = a.get("destruicao_cortical", False) and a.get("margem_mal_definida", False)
    a["margem_mal_definida_destrutiva"] = a.get("margem_mal_definida", False) and a.get("destruicao_cortical", False)

    a["abaixo_canal_mandibular_sem_expansao"] = a.get("abaixo_canal_mandibular", False) and a.get("sem_expansao", False)
    a["assintomatico_sem_sinais_agressivos"] = a.get("assintomatico", False) and not tem_sinal_agressivo(a)
    a["bem_delimitado_corticalizado"] = a.get("bem_delimitado", False) and a.get("corticalizado", False)
    a["bem_delimitado_corticalizado_assintomatico"] = a.get("bem_delimitado_corticalizado", False) and a.get("assintomatico", False)
    a["bem_delimitado_corticalizado_pericoronario"] = a.get("bem_delimitado_corticalizado", False) and a.get("pericoronario", False)
    a["massa_radiopaca_irregular_com_halo"] = a.get("massa_radiopaca_irregular", False) and a.get("halo_radiolucido", False)
    a["radiopaco_puro_com_halo"] = a.get("radiopaco_puro", False) and a.get("halo_radiolucido", False)
    a["vidro_fosco_difuso_sem_limite"] = a.get("vidro_fosco", False) and a.get("margens_imprecisas", False)
    a["multilocular_agressivo"] = a.get("multilocular", False) and (a.get("expansao_cortical", False) or a.get("destruicao_cortical", False))
    a["posterior_mandibula_extensa"] = a.get("posterior_mandibula", False) and a.get("grande_maior_40mm", False)
    a["lesao_unica_pequena"] = a.get("lesao_unica", False) and (a.get("pequeno_5_10mm", False) or a.get("pequeno_10_20mm", False))
    a["lesao_unica_tipica_pericoronaria"] = a.get("lesao_unica", False) and a.get("pericoronario", False) and a.get("dente_incluso", False)
    a["dente_nao_vital_unico"] = a.get("dente_nao_vital", False) and a.get("lesao_unica", False)
    a["dente_incluso_pericoronario_tipico"] = a.get("dente_incluso", False) and a.get("pericoronario", False) and a.get("bem_delimitado", False)
    a["periapical_dente_nao_vital"] = a.get("periapical", False) and a.get("dente_nao_vital", False)

    return a

def tem_sinal_agressivo(achados):
    sinais = [
        "dor_intensa", "parestesia", "anestesia", "crescimento_rapido",
        "margem_mal_definida", "destruicao_cortical", "invasao_partes_moles",
        "linfonodos_fixos", "historico_oncologico", "lesoes_multiplas",
        "mobilidade_dentaria"
    ]
    return any(achados.get(s, False) for s in sinais)

def calcular_fator_compatibilidade(diagnostico, achados):
    perfil = PERFIS_DIAGNOSTICOS.get(diagnostico)
    if not perfil:
        return 1.0

    fator = 1.0

    for item in perfil.get("necessarios", []):
        fator *= 2.8 if achados.get(item, False) else 0.12

    for item in perfil.get("fortes", []):
        if achados.get(item, False):
            fator *= 2.0

    for item in perfil.get("moderados", []):
        if achados.get(item, False):
            fator *= 1.35

    for item in perfil.get("incompativeis", []):
        if achados.get(item, False):
            fator *= 0.06

    # Trava de segurança: malignas sem sinais agressivos/história compatível não devem subir muito.
    if diagnostico in MALIGNAS and not tem_sinal_agressivo(achados):
        fator *= 0.08

    return fator

def aplicar_perfis(scores_modelo, achados, piso=1e-9):
    """Aplica perfis diagnósticos a todos os scores do modelo.
    scores_modelo: dict {diagnostico: probabilidade ou score}
    achados: dict {achado: bool}
    """
    achados_enriquecidos = enriquecer_achados(achados)
    ajustados = {}

    for dx, score in scores_modelo.items():
        fator = calcular_fator_compatibilidade(dx, achados_enriquecidos)
        ajustados[dx] = max(score, piso) * fator

    return normalizar(ajustados)

def top_n(scores, n=3):
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)[:n]

def explicar_compatibilidade(diagnostico, achados):
    achados = enriquecer_achados(achados)
    perfil = PERFIS_DIAGNOSTICOS.get(diagnostico, {})
    positivos = []
    ausentes_necessarios = []
    conflitos = []

    for campo in perfil.get("necessarios", []):
        if achados.get(campo, False):
            positivos.append(campo)
        else:
            ausentes_necessarios.append(campo)

    for campo in perfil.get("fortes", []) + perfil.get("moderados", []):
        if achados.get(campo, False):
            positivos.append(campo)

    for campo in perfil.get("incompativeis", []):
        if achados.get(campo, False):
            conflitos.append(campo)

    return {
        "diagnostico": diagnostico,
        "grupo": perfil.get("grupo"),
        "achados_compativeis": positivos,
        "necessarios_ausentes": ausentes_necessarios,
        "conflitos": conflitos,
        "score_malignidade_esperado": perfil.get("score_malignidade_esperado"),
    }
