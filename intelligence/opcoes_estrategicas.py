import yfinance as yf
import time
import requests
import json

def buscar_dados_ticker(ticker_base):
    formatos_teste = [
        f"{ticker_base}.SA",
        f"{ticker_base}.BVMF",
        f"{ticker_base}"
    ]

    for ticker in formatos_teste:
        try:
            dados = yf.Ticker(ticker)
            hist = dados.history(period="5d")
            if not hist.empty:
                return ticker, hist
        except Exception:
            time.sleep(1)  # evita bloqueio
            continue
    return None, None

def executar_analise_opcoes():
    ativos = ["VALE3", "PETR4", "BBAS3", "BOVA11", "BBDC4", "KLBN11", "CMIN3", "IRBR3", "GGBR4", "BRKM5"]
    resultados = []

    for ativo in ativos:
        ticker_formatado, dados = buscar_dados_ticker(ativo)
        if dados is None:
            resultados.append(f"[ALERTA] [{ativo}] Dados ausentes após tentativas em múltiplos formatos.")
            continue

        # Exemplo simples de detecção de tendência
        preco_hoje = dados["Close"].iloc[-1]
        preco_5_dias_atras = dados["Close"].iloc[0]

        if preco_hoje > preco_5_dias_atras * 1.05:
            resultados.append(f"Análise gráfica sugeriu: [{ativo}] Tendência de ALTA detectada com preço em {preco_hoje:.2f}.")
        elif preco_hoje < preco_5_dias_atras * 0.95:
            resultados.append(f"Análise gráfica sugeriu: [{ativo}] Tendência de BAIXA detectada com preço em {preco_hoje:.2f}.")
        else:
            resultados.append(f"Análise gráfica sugeriu: [{ativo}] Tendência LATERAL com preço em {preco_hoje:.2f}.")

    return resultados
