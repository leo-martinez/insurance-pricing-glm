# Auto Insurance Pricing — GLM in Python

Production-style auto insurance pricing engine using Generalized Linear Models (GLM) in Python, exposed as a REST API.

Replicates the standard actuarial workflow used in the insurance industry:

| Component | Model | Predicts |
|---|---|---|
| Frequency | Poisson GLM (log-link, exposure offset) | Claims per policy/year |
| Severity | Gamma GLM (log-link) | Cost per claim (€) |
| Pure Premium | Frequency × Severity | Technical price (€) |

![Python](https://img.shields.io/badge/Python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green)
![License](https://img.shields.io/badge/license-MIT-blue)

## Live API

https://insurance-pricing-glm.onrender.com/docs

Note: free tier hibernates after inactivity — first request may take up to 50 seconds.

## Quickstart

```bash
# 1. Clone and setup
git clone https://github.com/leo-martinez/insurance-pricing-glm.git
cd insurance-pricing-glm
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements-api.txt

# 2. Download dataset (~50MB)
python src/download_data.py

# 3. Train and save models
python retrain_small.py

# 4. Start the API
uvicorn src.api.main:app --reload
```

API running at http://localhost:8000 — docs at http://localhost:8000/docs

## Example request

```bash
curl -X POST https://insurance-pricing-glm.onrender.com/quote \
  -H "Content-Type: application/json" \
  -d '{
    "DrivAge": 35,
    "VehAge": 3,
    "VehPower": 7,
    "BonusMalus": 100,
    "VehBrand": "B1",
    "VehGas": "Regular",
    "Area": "D",
    "Density": 27000,
    "Exposure": 1.0
  }'
```

Response:

```json
{
  "expected_frequency": 0.2181,
  "expected_severity": 2044.21,
  "pure_premium": 445.75,
  "currency": "EUR"
}
```

## Input fields

| Field | Type | Description |
|---|---|---|
| DrivAge | int (18-100) | Driver age in years |
| VehAge | int (0-100) | Vehicle age in years |
| VehPower | int (4-15) | Vehicle power category |
| BonusMalus | int (50-350) | Bonus-malus coefficient (100 = neutral) |
| VehBrand | string | Vehicle brand code (B1-B14) |
| VehGas | string | Fuel type: Regular or Diesel |
| Area | string | Area code: A to F |
| Density | float | Population density of policyholder area |
| Exposure | float (0-1) | Coverage period as fraction of year |

## Tech stack

Python 3.12 · Pandas · NumPy · statsmodels · scikit-learn · FastAPI · Pydantic · pytest

## Dataset

Public French Motor Third-Party Liability dataset (freMTPL2), widely used in actuarial research.
~680k policies, fetched from OpenML.

## Tests

```bash
pytest tests/ -v
```

## Project structure

```
insurance-pricing-glm/
├── src/
│   ├── download_data.py       # fetch dataset
│   └── api/
│       ├── main.py            # FastAPI app
│       └── schemas.py         # Pydantic models
├── models/                    # trained coefficients (.pkl)
├── notebooks/
│   └── 01_train_models.ipynb  # EDA + GLM training
├── retrain_small.py           # retrain script (sample 30k)
├── tests/                     # pytest suite
├── requirements-api.txt       # API dependencies only
└── requirements.txt           # full dev dependencies
```

## Roadmap

- [x] Frequency model (Poisson GLM)
- [x] Severity model (Gamma GLM)
- [x] FastAPI endpoint with Pydantic validation
- [x] Deployed on Render
- [ ] Distributed version with PySpark/Databricks
- [ ] Docker image
- [ ] CI/CD with GitHub Actions
