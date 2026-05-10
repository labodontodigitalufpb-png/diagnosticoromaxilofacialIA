from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]

APP_NAME = "Oromaxillofacial AI Helper"
MODEL_NAME = "OromaxillofacialAI"

DATASET_PATH = BASE_DIR / "banco_lesoes_intraosseas_V3_5000_42classes_com_osteossarcoma.csv"
COL_TEXTO = "texto_treino"
COL_CLASSE = "diagnostico"

MODEL_DIR = BASE_DIR / "model"
MODEL_PATH = MODEL_DIR / f"modelo_{MODEL_NAME}.pkl"
VECTORIZER_PATH = MODEL_DIR / f"vetorizador_{MODEL_NAME}.pkl"
ENCODER_PATH = MODEL_DIR / f"encoderY_{MODEL_NAME}.pkl"

MODEL_ACCURACY = 91.93
