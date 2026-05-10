"""Input/output schemas for the pricing API."""
from pydantic import BaseModel, Field
from typing import Literal


class QuoteRequest(BaseModel):
    """Policyholder + vehicle features for a quote."""
    DrivAge: int = Field(..., ge=18, le=100, description="Driver age in years")
    VehAge: int = Field(..., ge=0, le=100, description="Vehicle age in years")
    VehPower: int = Field(..., ge=4, le=15, description="Vehicle power category")
    BonusMalus: int = Field(..., ge=50, le=350, description="Bonus-malus coefficient")
    VehBrand: Literal[
        "B1", "B2", "B3", "B4", "B5", "B6",
        "B10", "B11", "B12", "B13", "B14"
    ] = Field(..., description="Anonymized vehicle brand")
    VehGas: Literal["Regular", "Diesel"] = Field(..., description="Fuel type")
    Area: Literal["A", "B", "C", "D", "E", "F"] = Field(..., description="Area code")
    Density: float = Field(..., gt=0, description="Population density of policyholder area")
    Exposure: float = Field(1.0, gt=0, le=1.0, description="Coverage period (fraction of year)")

    class Config:
        json_schema_extra = {
            "example": {
                "DrivAge": 35,
                "VehAge": 5,
                "VehPower": 7,
                "BonusMalus": 50,
                "VehBrand": "B1",
                "VehGas": "Regular",
                "Area": "C",
                "Density": 1500,
                "Exposure": 1.0
            }
        }


class QuoteResponse(BaseModel):
    """Computed pure premium and components."""
    expected_frequency: float = Field(..., description="Expected claims per year")
    expected_severity: float = Field(..., description="Expected cost per claim (€)")
    pure_premium: float = Field(..., description="Pure premium for the period (€)")
    currency: str = "EUR"