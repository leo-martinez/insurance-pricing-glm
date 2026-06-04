"""FastAPI app exposing the GLM pricing models as a REST endpoint."""
import pickle
import math
from pathlib import Path

from fastapi import FastAPI, HTTPException
from src.api.schemas import QuoteRequest, QuoteResponse

# ---------- Load coefficients on startup ----------
MODELS_DIR = Path(__file__).resolve().parent.parent.parent / "models"

with open(MODELS_DIR / "freq_model.pkl", "rb") as f:
    FREQ_DATA = pickle.load(f)

with open(MODELS_DIR / "sev_model.pkl", "rb") as f:
    SEV_DATA = pickle.load(f)

FREQ_PARAMS = FREQ_DATA["params"]
SEV_PARAMS = SEV_DATA["params"]


def _predict_glm(params: dict, request: QuoteRequest) -> float:
    """Build linear predictor manually from coefficients and apply exp()."""

    veh_brand = request.VehBrand
    veh_gas = request.VehGas
    area = request.Area

    eta = params.get("Intercept", 0.0)
    eta += params.get("DrivAge", 0.0) * request.DrivAge
    eta += params.get("VehAge", 0.0) * request.VehAge
    eta += params.get("VehPower", 0.0) * request.VehPower
    eta += params.get("BonusMalus", 0.0) * request.BonusMalus
    eta += params.get("np.log(Density)", 0.0) * math.log(request.Density)

    # VehBrand (reference = B1)
    if veh_brand != "B1":
        eta += params.get(f"C(VehBrand)[T.{veh_brand}]", 0.0)

    # VehGas (reference = Diesel)
    if veh_gas != "Diesel":
        eta += params.get(f"C(VehGas)[T.{veh_gas}]", 0.0)

    # Area (reference = A)
    if area != "A":
        eta += params.get(f"C(Area)[T.{area}]", 0.0)

    return math.exp(eta)


# ---------- App ----------
app = FastAPI(
    title="Auto Insurance Pricing API",
    description="GLM-based pricing engine (Poisson frequency x Gamma severity)",
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
        freq_per_year = _predict_glm(FREQ_PARAMS, request)
        expected_sev = _predict_glm(SEV_PARAMS, request)

        expected_freq = freq_per_year * request.Exposure
        pure_premium = expected_freq * expected_sev

        return QuoteResponse(
            expected_frequency=round(expected_freq, 4),
            expected_severity=round(expected_sev, 2),
            pure_premium=round(pure_premium, 2),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{type(e).__name__}: {e}")
