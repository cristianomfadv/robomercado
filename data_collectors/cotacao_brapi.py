import os
import requests
import logging

# Diretório e arquivo de log
LOG_FILE = "logs/cotacao_brapi.log"
os.makedirs("logs", exist_ok=True)
logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s')

def buscar_cotacao_brapi(ticker):
    """Consulta a cotação de um ticker na BRAPI com autenticação opcional."""
    token = os.getenv("BRAPI_TOKEN")
    if token:
        url = f"https://brapi.dev/api/quote/{ticker}?range=5d&interval=1h&token={token}"
    else:
        url = f"https://brapi.dev/api/quote/{ticker}?range=5d&interval=1h"

    try:
        resposta = requests.get(url, timeout=10)
        resposta.raise_for_status()
        dados = resposta.json()
        if "results" in dados and dados["results"]:
            preco = dados["results"][0].get("regularMarketPrice")
            return preco
        else:
            logging.error(f"Sem resultados para {ticker}")
            return None
    except Exception as e:
        logging.error(f"Erro ao buscar cotação de {ticker}: {e}")
        return None
