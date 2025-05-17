# intelligence/comparador_opcoes.py

import json
from collections import defaultdict
from datetime import datetime

ARQUIVO = "dados/analises_opcoes.json"

def comparar_execucoes():
    try:
        with open(ARQUIVO, "r", encoding="utf-8") as f:
            historico = json.load(f)
    except:
        return []

    comparativos = []
    agrupado = defaultdict(list)

    for item in historico:
        chave = item["ativo"]
        agrupado[chave].append(item)

    for ativo, entradas in agrupado.items():
        entradas_ordenadas = sorted(entradas, key=lambda x: (x["data"], int(x["hora"])))

        ultimos = entradas_ordenadas[-6:]  # analisa últimos 3 dias (2 execuções por dia)
        if len(ultimos) >= 2:
            tendencias = [e["tendencia"] for e in ultimos]
            operacoes = [e["operacao"] for e in ultimos]

            if all(t == "alta" for t in tendencias):
                comparativos.append(f"[{ativo}] Confirmação: tendência de alta nas últimas {len(tendencias)} execuções.")
            elif all(t == "baixa" for t in tendencias):
                comparativos.append(f"[{ativo}] Tendência de baixa consistente nos últimos ciclos.")
            elif tendencias[-1] != tendencias[-2]:
                comparativos.append(f"[{ativo}] Divergência recente: {tendencias[-2]} → {tendencias[-1]}.")

    return comparativos
