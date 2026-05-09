# Auto Insurance Pricing — GLM in Python

End-to-end auto insurance pricing pipeline using **Generalized Linear Models (GLM)** in Python, exposed as a REST API.

## Project goals

This project replicates a typical actuarial pricing workflow used in the insurance industry:

- **Frequency model** (Poisson GLM) — predicts the expected number of claims per policy/year
- **Severity model** (Gamma GLM) — predicts the expected cost per claim
- **Pure premium** = Frequency × Severity — the technical price before commercial loadings
- **REST API** — accepts JSON input with policyholder features, returns the calculated premium

## 🛠️ Tech stack

- **Python 3.12**
- **Pandas / NumPy** — data manipulation
- **statsmodels** — GLM implementation (Poisson + Gamma)
- **scikit-learn** — preprocessing and validation
- **FastAPI** — REST endpoint
- **pytest** — automated tests
- **Databricks / PySpark** — distributed version (final phase)

## Dataset

Public **French Motor Third-Party Liability Claims** dataset, widely used in actuarial science research and education.

## Status

Work in progress — built incrementally as a portfolio project.

---

**Author:** Leonardo Martínez · [LinkedIn](https://linkedin.com/in/leo-martinez)