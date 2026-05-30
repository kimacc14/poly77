from integrations.polymarket_client import (
    POLYMARKET_API_ENDPOINTS,
    POLYMARKET_COLLATERAL_CURRENCY,
    POLYMARKET_TRADING_CONFIG,
    REAL_TRADING_ENABLED,
    PolymarketClient,
)


def test_polymarket_client_uses_public_v2_hosts():
    client = PolymarketClient()

    assert client.gamma_url == POLYMARKET_API_ENDPOINTS["gamma"]
    assert client.data_url == "https://data-api.polymarket.com"
    assert client.clob_url == "https://clob.polymarket.com"


def test_real_trading_is_guarded_off():
    client = PolymarketClient()

    assert REAL_TRADING_ENABLED is False
    assert POLYMARKET_TRADING_CONFIG["enabled"] is False
    assert client.trading_config["mode"] == "disabled-read-only-viewer"
    assert client.trading_config["collateral_currency"] == POLYMARKET_COLLATERAL_CURRENCY
