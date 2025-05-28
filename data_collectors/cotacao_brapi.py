# cotacao_brapi.py
import requests
import os

def obter_dados_acao_brapi(ticker):
    token = os.getenv("BRAPI_TOKEN")
    url = f"https://brapi.dev/api/quote/{ticker}?range=5d&interval=1d&token={token}"

    try:
        print(f"🔍 [BRAPI] Chamando: {url}")
        response = requests.get(url, timeout=10)
        print(f"📥 [BRAPI] Status: {response.status_code}")
        print(f"📄 [BRAPI] Texto bruto: {response.text[:300]}")

        response.raise_for_status()
        data = response.json()

        if "results" in data and len(data["results"]) > 0:
            return data["results"][0]
        else:
            print(f"⚠️ [BRAPI] Nenhum dado em 'results' para {ticker}")
            return None

    except requests.exceptions.Timeout:
        print("❌ Timeout ao acessar a BRAPI")
    except requests.exceptions.ConnectionError as e:
        print(f"❌ Erro de conexão com a BRAPI: {e}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro geral de requisição: {e}")
    except Exception as e:
        print(f"❌ Erro inesperado: {type(e).__name__}: {e}")

    return None
