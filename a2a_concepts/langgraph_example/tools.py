from langchain_core.tools import tool
from exchange_rates import EXCHANGE_RATES


@tool
def get_exchange_rate(
    currency_from: str = "USD",
    currency_to: str = "EUR",
    currency_date: str = "latest",
):
    """Use this tool to get current exchange rate.

    Args:
        currency_from: The currency to convert from (e.g., "USD").
        currency_to: The currency to convert to (e.g., "EUR").
        currency_date: The date for the exchange rate or "latest". Defaults to "latest".

    Returns:
        A dictionary containing the exchange rate data, or an error message if the request fails.
    """
    currency_from = currency_from.upper()
    currency_to = currency_to.upper()
    if currency_from in EXCHANGE_RATES and currency_to in EXCHANGE_RATES[currency_from]:
        rate = EXCHANGE_RATES[currency_from][currency_to]
        result = {
            "rate": rate,
            "from": currency_from,
            "to": currency_to,
            "date": currency_date,
        }
    else:
        result = {
            "error": f"Exchange rate not available for {currency_from} to {currency_to}",
            "from": currency_from,
            "to": currency_to,
            "date": currency_date,
        }

    return result
