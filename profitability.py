"""Deterministic France–Morocco resale margin calculations.

Initial business rules mirror the existing n8n 'Calcul marge' node.
These are estimates, not guarantees; customs, tax and other costs are not included.
"""
from dataclasses import dataclass
from math import isfinite
from typing import Optional


@dataclass(frozen=True)
class Config:
    exchange_rate_dh_per_eur: float = 10.8
    minimum_margin_eur: float = 130.0
    macbook_transport_eur: float = 25.0
    other_transport_eur: float = 10.0

    def __post_init__(self) -> None:
        if not isfinite(self.exchange_rate_dh_per_eur) or self.exchange_rate_dh_per_eur <= 0:
            raise ValueError("Exchange rate must be a positive finite number")
        if not isfinite(self.minimum_margin_eur) or self.minimum_margin_eur < 0:
            raise ValueError("Minimum margin must be nonnegative and finite")


def _amount(value: Optional[float], name: str) -> Optional[float]:
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not isfinite(value) or value < 0:
        raise ValueError(f"{name} must be a nonnegative finite number or None")
    return float(value)


def analyze_opportunity(
    *,
    device: str,
    negotiated_price_eur: Optional[float],
    resale_morocco_dh: Optional[float] = None,
    resale_france_eur: Optional[float] = None,
    accessories_eur: Optional[float] = 0,
    reserve_eur: Optional[float] = 0,
    functional: bool = True,
    risk: str = "moyen",
    config: Config = Config(),
) -> dict:
    """Calculate estimated margins and selection decision for one listing.

    Unknown purchase or both unknown resale prices yield no margin and keep=False.
    For parity with n8n, the same transport allowance is used for both markets.
    """
    if risk not in {"faible", "moyen", "élevé"}:
        raise ValueError("risk must be faible, moyen or élevé")
    price = _amount(negotiated_price_eur, "negotiated_price_eur")
    ma = _amount(resale_morocco_dh, "resale_morocco_dh")
    fr = _amount(resale_france_eur, "resale_france_eur")
    accessories = _amount(accessories_eur, "accessories_eur") or 0.0
    reserve = _amount(reserve_eur, "reserve_eur") or 0.0
    if price is None or (ma is None and fr is None):
        return {"total_cost_eur": None, "margin_morocco_eur": None,
                "margin_morocco_dh": None, "margin_france_eur": None,
                "best_margin_eur": None, "keep": False}
    transport = config.macbook_transport_eur if "macbook" in device.lower() else config.other_transport_eur
    cost = price + accessories + reserve + transport
    margin_ma = ma / config.exchange_rate_dh_per_eur - cost if ma is not None else None
    margin_fr = fr - cost if fr is not None else None
    best = max(m for m in (margin_ma, margin_fr) if m is not None)
    # Python round differs from JavaScript Math.round at .5; use these as estimates.
    return {
        "total_cost_eur": round(cost),
        "margin_morocco_eur": round(margin_ma) if margin_ma is not None else None,
        "margin_morocco_dh": round(margin_ma * config.exchange_rate_dh_per_eur) if margin_ma is not None else None,
        "margin_france_eur": round(margin_fr) if margin_fr is not None else None,
        "best_margin_eur": round(best),
        "keep": bool(functional and risk != "élevé" and best >= config.minimum_margin_eur),
    }
