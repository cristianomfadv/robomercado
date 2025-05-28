# data_collectors/cotacao_brapi.py

import requests

def get_brapi_quote(symbol):
    """Busca cotação de ativo B3 usando a API Brapi"""
    url = f"https://brapi.dev/api/quote/{symbol}?range=5d&interval=1d&fundamental=true"
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            data = r.json()
            if data and "results" in data and data["results"]:
                return data["results"][0]
        return None
    except Exception as e:
        with open('logs/logs_erros_analise.txt', 'a', encoding='utf-8') as log_file:
            log_file.write(f"Erro Brapi {symbol}: {str(e)}\n")
        return None
