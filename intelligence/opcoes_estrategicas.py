import yfinance as yf
import requests
import logging
import datetime
import os

LOG_FILE = "logs/opcoes_estrategicas.log"
os.makedirs("logs", exist_ok=True)
logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s')

# Fallback Alpha Vantage
from config import ALPHA_VANTAGE_API_KEY

def registrar_erro_opcoes(msg):
    logging.error(msg)
    with open(LOG_FILE, "a") as f:
        f.write(f"{datetime.datetime.now()}: {msg}\n")

def fetch_yfinance(ticker):
    try:
        data = yf.Ticker(ticker)
        hist = data.history(period="5d", interval="1h")
        if hist.empty:
            raise ValueError("No data from yfinance")
        close_prices = hist['Close']
        tendencia = "alta" if close_prices[-1] > close_prices[0] else "baixa"
        return {
            "ticker": ticker,
            "precos": close_prices.tolist(),
            "tendencia": tendencia
        }
    except Exception as e:
        registrar_erro_opcoes(f"YFinance erro para {ticker}: {e}")
        return None

def fetch_alpha_vantage(ticker):
    try:
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={ticker}.SA&interval=60min&apikey={ALPHA_VANTAGE_API_KEY}'
        r = requests.get(url, timeout=10)
        data = r.json()
        time_series = data.get('Time Series (60min)')
        if not time_series:
            raise ValueError("Sem dados do Alpha Vantage")
        valores = [float(v['4. close']) for v in list(time_series.values())[-5:]]
        tendencia = "alta" if valores[-1] > valores[0] else "baixa"
        return {
            "ticker": ticker,
            "precos": valores,
            "tendencia": tendencia
        }
    except Exception as e:
        registrar_erro_opcoes(f"Alpha Vantage erro para {ticker}: {e}")
        return None

def fetch_brapi(ticker):
    try:
        url = f'https://brapi.dev/api/quote/{ticker}?range=5d&interval=1h'
        r = requests.get(url, timeout=10)
        data = r.json()
        if not data.get("results"):
            raise ValueError("Sem dados do Brapi")
        close_prices = data["results"][0]["historicalDataPrice"]
        precos = [d['close'] for d in close_prices]
        tendencia = "alta" if precos[-1] > precos[0] else "baixa"
        return {
            "ticker": ticker,
            "precos": precos,
            "tendencia": tendencia
        }
    except Exception as e:
        registrar_erro_opcoes(f"Brapi erro para {ticker}: {e}")
        return None

def analisar_tendencia(ticker):
    """
    Tenta obter os dados do ativo via yfinance, se falhar tenta Alpha Vantage, depois Brapi.
    Retorna sinal estratégico padronizado para o strategy_engine.
    """
    fontes = [
        lambda t: fetch_yfinance(f"{t}.SA"),
        lambda t: fetch_yfinance(f"{t}.BVMF"),
        lambda t: fetch_yfinance(t),
        fetch_alpha_vantage,
        fetch_brapi
    ]
    for fonte in fontes:
        dados = fonte(ticker)
        if dados:
            tendencia = dados['tendencia']
            if tendencia == "alta":
                return {
                    "ativo": ticker,
                    "estrategia": "Trava de alta",
                    "detalhe": f"Tendência de alta detectada nas últimas sessões ({dados['precos'][0]:.2f} -> {dados['precos'][-1]:.2f})"
                }
            elif tendencia == "baixa":
                return {
                    "ativo": ticker,
                    "estrategia": "Compra seca de PUT",
                    "detalhe": f"Tendência de baixa detectada ({dados['precos'][0]:.2f} -> {dados['precos'][-1]:.2f})"
                }
            else:
                return {
                    "ativo": ticker,
                    "estrategia": "Sem estratégia",
                    "detalhe": "Não foi possível identificar tendência clara."
                }
    # Se todas as fontes falharem
    return {
        "ativo": ticker,
        "erro": "Falha ao obter dados de cotação em todas as fontes"
    }

def gerar_sinais_estrategicos(lista_ativos):
    """
    Para cada ativo da lista, executa a análise e retorna uma lista de sinais estratégicos.
    """
    sinais = []
    for ticker in lista_ativos:
        try:
            sinal = analisar_tendencia(ticker)
            sinais.append(sinal)
        except Exception as e:
            registrar_erro_opcoes(f"Erro geral para {ticker}: {e}")
            sinais.append({"ativo": ticker, "erro": str(e)})
    return sinais
