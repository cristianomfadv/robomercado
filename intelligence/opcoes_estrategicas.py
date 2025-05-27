# intelligence/opcoes_estrategicas.py

import yfinance as yf
from datetime import datetime
import json
import os

ATIVOS = [
    "VALE3.SA", "PETR4.SA", "BBAS3.SA", "KLBN11.SA", "CMIN3.SA",
    "IRBR3.SA", "GGBR4.SA", "BBDC4.SA", "BOVA11.SA", "BRKM5.SA"
]

ARQUIVO_REGISTRO = "dados/analises_opcoes.json"

def registrar_execucao(dados_execucao):
    if not os.path.exists("dados"):
        os.makedirs("dados")
    if os.path.exists(ARQUIVO_REGISTRO):
        with open(ARQUIVO_REGISTRO, "r", encoding="utf-8") as f:
            historico = json.load(f)
    else:
        historico = []

    historico.extend(dados_execucao)
    with open(ARQUIVO_REGISTRO, "w", encoding="utf-8") as f:
        json.dump(historico, f, indent=2, ensure_ascii=False)

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
    elif tendência == "baixa":
        alvo = round(preco * 0.96, 2)
        strike = round(alvo)
        return "trava de baixa", strike, alvo, -0.5
    else:
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
                mensagem = f"[{ticker.replace('.SA', '')}] Dados ausentes (Yahoo Finance)."
                print(mensagem)
                alertas.append(mensagem)
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
            erro_msg = f"[{ticker.replace('.SA', '')}] Erro ao obter dados: {str(e)}"
            print(erro_msg)
            alertas.append(erro_msg)

    registrar_execucao(registros)
    return alertas
