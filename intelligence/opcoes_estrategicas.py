
import os
import yfinance as yf
import requests
import pandas as pd
from datetime import datetime
import json
from dotenv import load_dotenv

load_dotenv()

ATIVOS = [
    "VALE3.SA", "PETR4.SA", "BBAS3.SA", "KLBN11.SA", "CMIN3.SA",
    "IRBR3.SA", "GGBR4.SA", "BBDC4.SA", "BOVA11.SA", "BRKM5.SA"
]

ARQUIVO_REGISTRO = "dados/analises_opcoes.json"
ARQUIVO_LOG_ERROS = "dados/log_falhas_opcoes.txt"
API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")

def registrar_execucao(dados_execucao):
    os.makedirs("dados", exist_ok=True)
    historico = []
    if os.path.exists(ARQUIVO_REGISTRO):
        with open(ARQUIVO_REGISTRO, "r", encoding="utf-8") as f:
            historico = json.load(f)
    historico.extend(dados_execucao)
    with open(ARQUIVO_REGISTRO, "w", encoding="utf-8") as f:
        json.dump(historico, f, indent=2, ensure_ascii=False)

def registrar_falha(msg):
    os.makedirs("dados", exist_ok=True)
    with open(ARQUIVO_LOG_ERROS, "a", encoding="utf-8") as f:
        f.write(f"{datetime.now()} - {msg}\n")

def analisar_tendencia(dados):
    ultimos = dados[-10:]
    if ultimos["Close"].iloc[-1] > ultimos["Close"].mean():
        return "alta"
    elif ultimos["Close"].iloc[-1] < ultimos["Close"].mean():
        return "baixa"
    else:
        return "neutra"

def calcular_operacao(ativo, preco, tendencia):
    if tendencia == "alta":
        alvo = round(preco * 1.04, 2)
        strike = round(alvo)
        return "trava de alta", strike, alvo, 0.5
    elif tendencia == "baixa":
        alvo = round(preco * 0.96, 2)
        strike = round(alvo)
        return "trava de baixa", strike, alvo, -0.5
    return None

def fallback_alpha_vantage(ticker):
    try:
        simbolo = ticker.replace(".SA", "") + ".SA"
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={simbolo}&interval=30min&apikey={API_KEY}&datatype=json"
        r = requests.get(url)
        dados = r.json()
        serie = dados.get("Time Series (30min)", {})
        if not serie:
            return None
        df = pd.DataFrame([
            {
                "Datetime": k,
                "Close": float(v["4. close"])
            } for k, v in serie.items()
        ])
        df = df.sort_values("Datetime")
        df.set_index("Datetime", inplace=True)
        return df
    except Exception as e:
        registrar_falha(f"Erro Alpha Vantage {ticker}: {e}")
        return None

def executar_analise_opcoes():
    alertas = []
    registros = []
    agora = datetime.now()
    hora = str(agora.hour)
    data = agora.strftime("%Y-%m-%d")

    for ticker in ATIVOS:
        try:
            dados = yf.download(ticker, period="5d", interval="30m", progress=False)
            if dados.empty:
                registrar_falha(f"{ticker}: Dados ausentes no Yahoo. Tentando fallback Alpha Vantage.")
                dados = fallback_alpha_vantage(ticker)
                if dados is None or dados.empty:
                    msg = f"[{ticker.replace('.SA', '')}] Dados indisponíveis em ambas as fontes."
                    print(msg)
                    alertas.append(msg)
                    continue

            ativo = ticker.replace(".SA", "")
            preco = dados["Close"].iloc[-1]
            tendencia = analisar_tendencia(dados)
            resultado = calcular_operacao(ativo, preco, tendencia)

            if resultado:
                tipo, strike, alvo, delta = resultado
                mensagem = (
                    f"[{ativo}] Tendência: {tendencia.upper()} | Sinal: {tipo} | "
                    f"Alvo: R$ {alvo} | Strike: R$ {strike} | Delta: {delta}"
                )
                alertas.append(mensagem)
                registros.append({
                    "data": data,
                    "hora": hora,
                    "ativo": ativo,
                    "tendencia": tendencia,
                    "operacao": tipo,
                    "alvo": alvo,
                    "strike": strike,
                    "delta": delta
                })
        except Exception as e:
            registrar_falha(f"{ticker}: Erro geral - {e}")

    if registros:
        registrar_execucao(registros)
    return alertas
