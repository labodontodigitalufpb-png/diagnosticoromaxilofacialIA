from fastapi import APIRouter, Query

router = APIRouter(prefix="/sintomas", tags=["Sintomas"])

diagnosticoIA = None


def get_diagnostico_ia():
    global diagnosticoIA
    if diagnosticoIA is None:
        from services.executarService import DiagnosticoIA

        diagnosticoIA = DiagnosticoIA()
    return diagnosticoIA

@router.get("/predict")
def predict(
    descricao: str = Query(None, description="Descrição clínica/radiográfica"),
    sintomas: str = Query(None, description="Compatibilidade: texto separado por vírgula"),
    idade: int = Query(None, description="Idade do paciente"),
    sexo: str = Query(None, description="Sexo do paciente: M ou F"),
    localizacao: str = Query(None, description="Localização anatômica sugerida"),
    achados: str = Query(None, description="Achados radiográficos/tomográficos"),
    aspectos_clinicos: str = Query(None, description="Aspectos clínicos"),
):
    partes = [
        descricao or sintomas or "",
        f"paciente {idade} anos" if idade is not None else "",
        f"sexo {sexo}" if sexo else "",
        localizacao or "",
        achados or "",
        aspectos_clinicos or "",
    ]
    texto = ", ".join([parte.strip() for parte in partes if str(parte).strip()])
    descricoes = [s.strip() for s in texto.split(",") if s.strip()]
    return get_diagnostico_ia().predict_simples(descricoes)
