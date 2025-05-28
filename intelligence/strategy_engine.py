# intelligence/strategy_engine.py

def gerar_recomendacoes(dados_grafico: dict, eventos: list, sentimento: list):
    alertas = []

    for ativo, sinal in dados_grafico.items():
        if sinal.get("tendencia") == "alta":
            alerta = f"📈 Recomendação de TRAVA DE ALTA em {ativo} com alvo técnico em {sinal.get('alvo')}"
        elif sinal.get("tendencia") == "baixa":
            alerta = f"📉 Recomendação de COMPRA DE PUT em {ativo} com alvo técnico em {sinal.get('alvo')}"
        else:
            alerta = f"⏸️ Nenhuma tendência clara detectada para {ativo}"

        alertas.append(alerta)

    if not alertas:
        alertas.append("⚠️ Nenhuma recomendação estratégica identificada no momento.")

    return alertas
