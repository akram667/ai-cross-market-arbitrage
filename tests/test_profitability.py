import pytest
from profitability import Config, analyze_opportunity


def test_profitable_macbook():
    result = analyze_opportunity(device="MacBook Air M2", negotiated_price_eur=400,
                                 resale_morocco_dh=7000, resale_france_eur=500,
                                 accessories_eur=20, reserve_eur=15, risk="faible")
    assert result["total_cost_eur"] == 460
    assert result["margin_morocco_eur"] == 188
    assert result["margin_france_eur"] == 40
    assert result["keep"] is True


def test_high_risk_is_rejected_even_when_profitable():
    result = analyze_opportunity(device="iPhone", negotiated_price_eur=200,
                                 resale_france_eur=600, risk="élevé")
    assert result["best_margin_eur"] == 390
    assert result["keep"] is False


def test_nonfunctional_is_rejected():
    result = analyze_opportunity(device="iPhone", negotiated_price_eur=200,
                                 resale_france_eur=600, functional=False)
    assert result["keep"] is False


def test_missing_prices_are_not_guessed():
    result = analyze_opportunity(device="MacBook", negotiated_price_eur=300)
    assert result["best_margin_eur"] is None
    assert result["keep"] is False


def test_only_france_market_available():
    result = analyze_opportunity(device="Galaxy S25", negotiated_price_eur=300,
                                 resale_france_eur=450)
    assert result["margin_morocco_eur"] is None
    assert result["margin_france_eur"] == 140
    assert result["keep"] is True


def test_negative_price_rejected():
    with pytest.raises(ValueError):
        analyze_opportunity(device="iPhone", negotiated_price_eur=-1,
                            resale_france_eur=500)


def test_invalid_exchange_rate_rejected():
    with pytest.raises(ValueError):
        Config(exchange_rate_dh_per_eur=0)
