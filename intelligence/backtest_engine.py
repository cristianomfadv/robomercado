# intelligence/backtest_engine.py

import json
import os
from datetime import datetime

CAMINHO_BACKTEST = "historico/backtest_registro.json"
os.makedirs("historico", exist_ok=True)

def registrar_sinal(ativo, tipo, preco_entrada):
    try:
        with open(CAMINHO_BACKTEST, "r", encoding="utf-8") as f:
            dados = json.load(f)
    except:
        dados = []

    dados.append({
        "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "ativo": ativo,
        "tipo": tipo,
        "preco_entrada": preco_entrada
    })

    with open(CAMINHO_BACKTEST, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)

def registrar_alerta_historico(alerta):
    try:
        preco = alerta.get("preco_entrada", "n/d")
        registrar_sinal(alerta["ativo"], alerta["tipo"], preco)
    except Exception as e:
        print(f"Erro ao registrar backtest: {e}")

def avaliar_resultados():
    try:
        with open(CAMINHO_BACKTEST, "r", encoding="utf-8") as f:
            dados = json.load(f)
    except:
        return []

    hoje = datetime.now().date()
    ultimos = [d for d in dados if datetime.strptime(d["data"], "%Y-%m-%d %H:%M:%S").date() >= hoje]
    return [f"{d['data']} — {d['ativo']} — {d['tipo']} — entrada: R$ {d['preco_entrada']}" for d in ultimos]
