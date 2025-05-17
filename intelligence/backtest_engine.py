# intelligence/backtest_engine.py

import json
import os
from datetime import datetime, timedelta
import yfinance as yf

CAMINHO_REGISTRO = "historico/backtest_registro.json"

def registrar_sinal(ativo, tipo_recomendacao, preco_entrada):
    entrada = {
        "ativo": ativo,
        "tipo": tipo_recomendacao,
        "data": datetime.now().strftime("%Y-%m-%d"),
        "preco_entrada": preco_entrada
    }

    if not os.path.exists("historico"):
        os.makedirs("historico")

    try:
        with open(CAMINHO_REGISTRO, "r", encoding="utf-8") as f:
            registros = json.load(f)
    except:
        registros = []

    registros.append(entrada)

    with open(CAMINHO_REGISTRO, "w", encoding="utf-8") as f:
        json.dump(registros, f, indent=2)

def avaliar_resultados(dias=3):
    if not os.path.exists(CAMINHO_REGISTRO):
        return []

    with open(CAMINHO_REGISTRO, "r", encoding="utf-8") as f:
        registros = json.load(f)

    resultados = []
    hoje = datetime.now().date()
    novos_registros = []

    for registro in registros:
        data_sinal = datetime.strptime(registro["data"], "%Y-%m-%d").date()
        if (hoje - data_sinal).days >= dias:
            ativo = registro["ativo"]
            preco_inicial = registro["preco_entrada"]

            try:
                dados = yf.download(ativo + ".SA", start=str(data_sinal + timedelta(days=dias)), end=str(data_sinal + timedelta(days=dias+1)), progress=False)
                preco_final = dados["Close"].iloc[0]
                variacao = preco_final - preco_inicial

                if "CALL" in registro["tipo"] or "alta" in registro["tipo"]:
                    resultado = "✅ Acerto" if variacao > 0 else "❌ Erro"
                elif "PUT" in registro["tipo"] or "baixa" in registro["tipo"]:
                    resultado = "✅ Acerto" if variacao < 0 else "❌ Erro"
                else:
                    resultado = "⚠ Neutro"

                resultados.append(f"{ativo} | {registro['tipo']} | {registro['data']} → {resultado} ({variacao:.2f})")
            except:
                resultados.append(f"{ativo} | {registro['tipo']} | {registro['data']} → Dados indisponíveis")

        else:
            novos_registros.append(registro)

    # Atualiza o arquivo apenas com registros ainda não vencidos
    with open(CAMINHO_REGISTRO, "w", encoding="utf-8") as f:
        json.dump(novos_registros, f, indent=2)

    return resultados
