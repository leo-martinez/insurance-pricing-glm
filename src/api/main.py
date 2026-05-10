"""FastAPI app exposing the GLM pricing models as a REST endpoint."""
import pickle
import traceback
from pathlib import Path

import numpy as np
import pandas as pd
from fastapi import FastAPI, HTTPException

from src.api.schemas import QuoteRequest, QuoteResponse

# ---------- Load models on startup ----------
MODELS_DIR = Path(__file__).resolve().parent.parent.parent / "models"

with open(MODELS_DIR / "freq_model.pkl", "rb") as f:
    FREQ_MODEL = pickle.load(f)
with open(MODELS_DIR / "sev_model.pkl", "rb") as f:
    SEV_MODEL = pickle.load(f)


def _try_predict(model, row_data: dict) -> float:
    """Try predicting with quoted then unquoted categoricals (CSV import quirk)."""
    cat_cols = ["VehBrand", "VehGas", "Area"]

    # Try with quotes first
    try:
        df = pd.DataFrame([{
            **row_data,
            **{c: f"'{row_data[c]}'" for c in cat_cols},
        }])
        if "Exposure" in row_data:
            return float(model.predict(df, offset=np.zeros(len(df)))[0])
        return float(model.predict(df)[0])
    except Exception:
        pass

    # Fallback without quotes
    df = pd.DataFrame([row_data])
    if "Exposure" in row_data:
        return float(model.predict(df, offset=np.zeros(len(df)))[0])
    return float(model.predict(df)[0])


# ---------- App ----------
app = FastAPI(
    title="Auto Insurance Pricing API",
    description="GLM-based pricing engine (Poisson frequency × Gamma severity)",
    version="1.0.0",
)


@app.get("/")
def root():
    return {"service": "Auto Insurance Pricing API", "version": "1.0.0", "docs": "/docs"}


@app.get("/health")
def health():
    return {"status": "ok", "models_loaded": True}


@app.post("/quote", response_model=QuoteResponse)
def quote(request: QuoteRequest) -> QuoteResponse:
    try:
        # Try ALL combinations of quoted/unquoted to handle CSV inconsistencies
        cat_cols = ["VehBrand", "VehGas", "Area"]
        base_row = {
            "DrivAge": float(request.DrivAge),
            "VehAge": float(request.VehAge),
            "VehPower": float(request.VehPower),
            "BonusMalus": float(request.BonusMalus),
            "VehBrand": request.VehBrand,
            "VehGas": request.VehGas,
            "Area": request.Area,
            "Density": float(request.Density),
            "Exposure": float(request.Exposure),
        }

        last_error = None
        freq_per_year = None
        expected_sev = None

        # Try all 8 combinations of quoting (2^3 = 8) for each model
        from itertools import product
        for combo in product([False, True], repeat=3):
            try:
                row_dict = dict(base_row)
                for i, col in enumerate(cat_cols):
                    if combo[i]:
                        row_dict[col] = f"'{base_row[col]}'"
                df = pd.DataFrame([row_dict])
                freq_per_year = float(FREQ_MODEL.predict(df, offset=np.zeros(len(df)))[0])
                expected_sev = float(SEV_MODEL.predict(df)[0])
                break  # Success
            except Exception as e:
                last_error = e
                continue

        if freq_per_year is None:
            raise RuntimeError(f"All format attempts failed. Last error: {last_error}")

        expected_freq = freq_per_year * request.Exposure
        pure_premium = expected_freq * expected_sev

        return QuoteResponse(
            expected_frequency=round(expected_freq, 4),
            expected_severity=round(expected_sev, 2),
            pure_premium=round(pure_premium, 2),
        )

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"{type(e).__name__}: {e}"
        )