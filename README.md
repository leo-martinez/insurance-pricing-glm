# Auto Insurance Pricing — GLM in Python

Production-style auto insurance pricing engine using **Generalized Linear Models (GLM)** in Python, exposed as a REST API.

Replicates the standard actuarial workflow used in the insurance industry:

| Component | Model | Predicts |
|---|---|---|
| **Frequency** | Poisson GLM (log-link, exposure offset) | Claims per policy/year |
| **Severity** | Gamma GLM (log-link) | Cost per claim (€) |
| **Pure Premium** | Frequency × Severity | Technical price (€) |

##  Quickstart

```bash
# 1. Setup
git clone https://github.com/leo-martinez/insurance-pricing-glm.git
cd insurance-pricing-glm
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt

# 2. Download dataset (~50MB)
python src/download_data.py

# 3. Train and save models
jupyter notebook notebooks/01_train_models.ipynb   # run all cells

# 4. Start the API
uvicorn src.api.main:app --reload
```

API now running at **http://localhost:8000** — docs at **http://localhost:8000/docs**.

## 📡 Example request

```bash
curl -X POST http://localhost:8000/quote \
  -H "Content-Type: application/json" \
  -d @examples/sample_request.json
```

Response:

```json
{
  "expected_frequency": 0.0742,
  "expected_severity": 1854.32,
  "pure_premium": 137.59,
  "currency": "EUR"
}
```

## Tech stack

- **Python 3.12** · **Pandas** · **NumPy**
- **statsmodels** — GLM implementation
- **scikit-learn** — train/test split, metrics
- **FastAPI** + **Pydantic** — REST API with input validation
- **pytest** — automated tests
- **Jupyter** — model training notebook

## Dataset

Public **French Motor Third-Party Liability** dataset (`freMTPL2`), widely used in actuarial research. ~680k policies, fetched from OpenML.

## Tests

```bash
pytest tests/ -v
```

## Project structure
insurance-pricing-glm/
├── notebooks/01_train_models.ipynb   # EDA + GLM training
├── src/
│   ├── download_data.py              # fetch dataset
│   └── api/                          # FastAPI app
├── models/                           # trained .pkl (gitignored)
├── tests/                            # pytest suite
├── examples/sample_request.json      # API input example
└── requirements.txt

## 🚧 Roadmap

- [x] Frequency model (Poisson GLM)
- [x] Severity model (Gamma GLM)
- [x] FastAPI endpoint with Pydantic validation
- [x] Test suite
- [ ] Distributed version with PySpark/Databricks
- [ ] Docker image
- [ ] CI/CD with GitHub Actions

---

**Author:** Leonardo Martínez · [LinkedIn](https://linkedin.com/in/leo-martinez)
🇪🇸 Spanish citizen — open to opportunities in Spain.