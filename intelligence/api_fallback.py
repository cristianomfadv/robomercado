import os
import requests

def buscar_ultimo_preco_alpha(ticker_b3):
    api_key = os.getenv("ALPHAVANTAGE_API_KEY")
    simbolo = f"{ticker_b3}.SA"
    url = f"https://www.alphavantage.co/query"
    params = {
        "function": "GLOBAL_QUOTE",
        "symbol": simbolo,
        "apikey": api_key
    }

    try:
        resposta = requests.get(url, params=params, timeout=10)
        dados = resposta.json()
        preco_str = dados["Global Quote"]["05. price"]
        return float(preco_str)
    except Exception:
        return None
