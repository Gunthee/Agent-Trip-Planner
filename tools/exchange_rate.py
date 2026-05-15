import requests


def get_exchange_rate(from_currency: str, to_currency: str, amount: float = 1.0) -> str:
    """Fetch live currency exchange rates via the free Frankfurter API (no API key needed)."""
    try:
        url = f"https://api.frankfurter.app/latest?from={from_currency.upper()}&to={to_currency.upper()}"
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        rate = data.get("rates", {}).get(to_currency.upper())
        if rate is None:
            return (
                f"Currency '{to_currency}' not found. "
                "Note: THB (Thai Baht) is not in Frankfurter's base set — use USD or EUR as an intermediate."
            )

        converted = amount * rate
        return (
            f"Exchange Rate ({data.get('date', 'N/A')}):\n"
            f"  1 {from_currency.upper()} = {rate:.4f} {to_currency.upper()}\n"
            f"  {amount} {from_currency.upper()} = {converted:,.2f} {to_currency.upper()}"
        )
    except requests.RequestException as e:
        return f"Network error fetching exchange rate: {e}"
    except Exception as e:
        return f"Error: {e}"
