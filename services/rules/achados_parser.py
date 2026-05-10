import re


def _normalizar_texto(texto):
    texto = str(texto or "").lower()
    trocas = {
        "á": "a", "à": "a", "ã": "a", "â": "a",
        "é": "e", "ê": "e",
        "í": "i",
        "ó": "o", "ô": "o", "õ": "o",
        "ú": "u",
        "ç": "c",
    }
    for origem, destino in trocas.items():
        texto = texto.replace(origem, destino)
    return texto


def _tem(texto, *padroes):
    return any(padrao in texto for padrao in padroes)


def _idade_flags(texto):
    match = re.search(r"paciente\s+(\d+)\s+anos", texto)
    if not match:
        return {}

    idade = int(match.group(1))
    return {
        "crianca": idade < 12,
        "adolescente": 12 <= idade < 18,
        "idade_10_30": 10 <= idade <= 30,
        "idade_20_40": 20 <= idade <= 40,
        "idade_maior_30": idade > 30,
        "idade_maior_50": idade > 50,
        "adulto": idade >= 18,
        "idoso": idade >= 60,
    }


def achados_from_texto(partes):
    texto = _normalizar_texto(", ".join(str(p) for p in (partes or [])))

    achados = {
        "radiolucido": _tem(texto, "radiolucido", "radiolucida"),
        "predominantemente_radiolucido": _tem(texto, "predominantemente radiolucido", "predominantemente radiolucida"),
        "radiopaco": _tem(texto, "radiopaco", "radiopaca"),
        "predominantemente_radiopaco": _tem(texto, "predominantemente radiopaco", "predominantemente radiopaca"),
        "misto": _tem(texto, "misto", "mista"),
        "hipodenso": _tem(texto, "hipodenso", "hipodensa"),
        "hiperdenso": _tem(texto, "hiperdenso", "hiperdensa"),
        "unilocular": _tem(texto, "unilocular"),
        "multilocular": _tem(texto, "multilocular"),
        "pseudolocular": _tem(texto, "pseudolocular"),
        "difusa": _tem(texto, "difusa", "difuso"),
        "lesoes_multiplas": _tem(texto, "multifocal", "multiplas", "bilateral"),
        "septacoes_finas": _tem(texto, "septacoes finas"),
        "calcificacoes_internas": _tem(texto, "calcificacoes internas", "calcificacoes puntiformes", "calcificacoes grosseiras"),
        "calcificacoes_finas": _tem(texto, "calcificacoes puntiformes", "calcificacoes finas"),
        "bolhas_de_sabao": _tem(texto, "bolhas de sabao"),
        "favo_de_mel": _tem(texto, "favo de mel"),
        "raquete_de_tenis": _tem(texto, "raquete de tenis"),
        "vidro_fosco": _tem(texto, "vidro fosco"),
        "driven_snow": _tem(texto, "driven snow"),
        "granular": _tem(texto, "granular"),
        "bem_delimitado": _tem(texto, "bem delimitado", "bem delimitadas"),
        "margem_mal_definida": _tem(texto, "mal delimitado", "mal delimitadas", "margem mal definida", "limites mal"),
        "margens_imprecisas": _tem(texto, "margens imprecisas", "sem contorno nitido", "mal delimitadas"),
        "corticalizado": _tem(texto, "corticalizado", "corticalizada", "corticalizadas"),
        "halo_esclerotico": _tem(texto, "halo esclerotico"),
        "halo_radiolucido": _tem(texto, "halo radiolucido"),
        "lobulado": _tem(texto, "lobulado", "lobuladas"),
        "zona_transicao_intermediaria": _tem(texto, "zona:intermediaria", "zona de transicao intermediaria", "intermediaria"),
        "crescimento_lento": _tem(texto, "lento crescimento", "crescimento lento"),
        "crescimento_rapido": _tem(texto, "rapido crescimento", "crescimento rapido"),
        "grande_maior_40mm": _tem(texto, "maior que 40 mm", ">40 mm"),
        "pequeno_ate_5mm": _tem(texto, "menor que 5 mm", "<5 mm"),
        "pequeno_5_10mm": _tem(texto, "5-10 mm", "5 a 10 mm"),
        "pequeno_10_20mm": _tem(texto, "10-20 mm", "10 a 20 mm"),
        "mandibula": _tem(texto, "mandibula"),
        "maxila": _tem(texto, "maxila"),
        "posterior": _tem(texto, "posterior", "molar", "angulo mandibular", "ramo mandibular"),
        "anterior": _tem(texto, "anterior", "incisivo", "canino"),
        "incisivo": _tem(texto, "incisivo"),
        "canino": _tem(texto, "canino"),
        "premolar": _tem(texto, "pre-molar", "premolar"),
        "molar": _tem(texto, "molar"),
        "ramo_mandibular": _tem(texto, "ramo mandibular"),
        "angulo_mandibular": _tem(texto, "angulo mandibular"),
        "seio_maxilar": _tem(texto, "seio maxilar"),
        "gengiva": _tem(texto, "gengiva"),
        "periapical": _tem(texto, "periapical"),
        "pericoronario": _tem(texto, "pericoronal", "pericoronario", "pericoronaria"),
        "interradicular": _tem(texto, "interradicular"),
        "lateral_radicular": _tem(texto, "lateral radicular"),
        "area_edentula": _tem(texto, "area edentula", "rebordo edentulo"),
        "abaixo_canal_mandibular": _tem(texto, "abaixo do canal"),
        "relacao_seio_maxilar": _tem(texto, "proximo ao seio", "elevação do assoalho", "opacificacao", "invasao do seio"),
        "dente_vital": _tem(texto, "dente vital", "dentes vitais", "dentes adjacentes vitais"),
        "dente_nao_vital": _tem(texto, "dente nao vital", "nao vital", "necrose pulpar"),
        "dente_incluso": _tem(texto, "dente incluso", "dente impactado", "impactado"),
        "dente_associado_presente": _tem(texto, "dente associado", "dente incluso", "dente impactado"),
        "deslocamento_dentario": _tem(texto, "deslocamento dentario"),
        "mobilidade_dentaria": _tem(texto, "mobilidade dentaria", "mobilidade"),
        "reabsorcao_radicular": _tem(texto, "reabsorcao radicular"),
        "perda_lamina_dura": _tem(texto, "perda da lamina dura"),
        "alargamento_espaco_periodontal": _tem(texto, "alargamento irregular do espaco periodontal", "alargamento do espaco periodontal"),
        "retencao_dentaria": _tem(texto, "retencao dentaria"),
        "fusionado_raiz": _tem(texto, "fusionado ao apice", "fusionada a raiz", "aderida ao apice"),
        "sem_relacao_raiz": _tem(texto, "sem relacao dentaria direta", "sem relacao dentaria"),
        "terceiro_molar_incluso": _tem(texto, "terceiro molar"),
        "canino_incluso": _tem(texto, "canino") and _tem(texto, "incluso", "impactado"),
        "expansao_cortical": _tem(texto, "expansao cortical", "corticais expandidas", "expansao discreta"),
        "expansao_discreta": _tem(texto, "expansao discreta"),
        "expansao_cortical_vestibular": _tem(texto, "cortical vestibular", "expansao vestibular"),
        "expansao_cortical_lingual": _tem(texto, "cortical lingual", "expansao lingual"),
        "pouca_expansao": _tem(texto, "pouca expansao"),
        "destruicao_cortical": _tem(texto, "destruicao cortical", "corticais perfuradas", "perfuracao focal", "perfuração focal", "perfuracao cortical"),
        "invasao_partes_moles": _tem(texto, "invasao de partes moles", "extensao para partes moles"),
        "reacao_periosteal_agressiva": _tem(texto, "reacao periosteal agressiva", "reacao periosteal", "neoformacao periosteal"),
        "raios_de_sol": _tem(texto, "raios de sol", "espiculas osseas radiais"),
        "triangulo_codman": _tem(texto, "triangulo de codman"),
        "assintomatico": _tem(texto, "assintomatico"),
        "dor_leve": _tem(texto, "dor leve"),
        "dor_intensa": _tem(texto, "dor intensa"),
        "parestesia": _tem(texto, "parestesia") and not _tem(texto, "sem parestesia"),
        "anestesia": _tem(texto, "anestesia"),
        "fistula": _tem(texto, "fistula"),
        "pericoronarite": _tem(texto, "pericoronarite"),
        "edema_local": _tem(texto, "edema"),
        "linfonodos_fixos": _tem(texto, "linfonodos endurecidos fixos"),
        "historico_oncologico": _tem(texto, "historico oncologico", "neoplasia previa"),
        "historia_extracao": _tem(texto, "extracao previa", "area de extracao"),
        "historia_cirurgia_seio_maxilar": _tem(texto, "cirurgia seio maxilar", "cirurgia maxilar"),
        "historia_carie_ou_trauma": _tem(texto, "carie", "trauma"),
        "estruturas_dentiformes": _tem(texto, "material dentiforme", "estruturas dentiformes"),
        "multiplas_estruturas_dentiformes": _tem(texto, "estruturas dentiformes multiplas", "material dentiforme"),
        "massa_radiopaca_irregular": _tem(texto, "massa radiopaca", "imagem calcificada desorganizada", "radiopaca irregular"),
        "massa_radiopaca": _tem(texto, "massa radiopaca", "radiopaca"),
        "radiopaco_puro_sem_halo": _tem(texto, "radiopaco") and not _tem(texto, "halo radiolucido"),
        "radiolucido_puro_sem_calcificacao": _tem(texto, "radiolucido") and not _tem(texto, "calcificacao"),
        "sem_alteracao_ossea": _tem(texto, "sem alteracao ossea"),
        "lesao_mucosa_gengival": _tem(texto, "lesao mucosa", "gengival"),
        "nodulo_azulado": _tem(texto, "nodulo azulado"),
        "mucosa_normal": _tem(texto, "mucosa normal"),
        "intraosseo_extenso": _tem(texto, "intraosseo extenso"),
        "defeito_semilunar": _tem(texto, "defeito semilunar", "radiolucidez triangular interradicular"),
        "recorrente": _tem(texto, "recorrente", "recorrencia"),
        "crescimento_anteroposterior": _tem(texto, "crescimento anteroposterior"),
        "lesao_unica": not _tem(texto, "multiplas", "multifocal", "bilateral"),
    }

    achados.update(_idade_flags(texto))
    achados["sexo_feminino"] = _tem(texto, "sexo f")
    achados["sexo_masculino"] = _tem(texto, "sexo m")
    achados["unilocular_ou_multilocular"] = achados["unilocular"] or achados["multilocular"]

    return achados
