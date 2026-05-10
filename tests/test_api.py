"""Smoke tests for the pricing API."""
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_quote_returns_positive_premium():
    payload = {
        "DrivAge": 35, "VehAge": 5, "VehPower": 7, "BonusMalus": 50,
        "VehBrand": "B1", "VehGas": "Regular", "Area": "C",
        "Density": 1500, "Exposure": 1.0
    }
    r = client.post("/quote", json=payload)
    assert r.status_code == 200
    body = r.json()
    assert body["pure_premium"] > 0
    assert body["expected_frequency"] > 0
    assert body["expected_severity"] > 0


def test_young_driver_pays_more_than_middle_aged():
    base = {
        "VehAge": 5, "VehPower": 7, "BonusMalus": 50,
        "VehBrand": "B1", "VehGas": "Regular", "Area": "C",
        "Density": 1500, "Exposure": 1.0
    }
    young = client.post("/quote", json={**base, "DrivAge": 20}).json()
    middle = client.post("/quote", json={**base, "DrivAge": 45}).json()
    assert young["pure_premium"] > middle["pure_premium"]


def test_invalid_age_rejected():
    payload = {
        "DrivAge": 5, "VehAge": 5, "VehPower": 7, "BonusMalus": 50,
        "VehBrand": "B1", "VehGas": "Regular", "Area": "C",
        "Density": 1500, "Exposure": 1.0
    }
    r = client.post("/quote", json=payload)
    assert r.status_code == 422  # Pydantic validation error