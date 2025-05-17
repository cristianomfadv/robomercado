# intelligence/strategy_engine.py

from datetime import datetime

def gerar_estrategia_recomendada(sinais):
    estrategias = []

    for sinal in sinais:
        texto = sinal.lower()

        # Simulações de lógica estratégica baseada em palavras-chave
        if "dividendo" in texto or "provento" in texto:
            estrategias.append(f"🟢 [{datetime.now().strftime('%d/%m %H:%M')}] Estratégia: Venda coberta de PUT sugerida – {sinal}")
        elif "balanço" in texto and "positivo" in texto:
            estrategias.append(f"📈 [{datetime.now().strftime('%d/%m %H:%M')}] Estratégia: Compra de CALL sugerida – {sinal}")
        elif "balanço" in texto and "negativo" in texto:
            estrategias.append(f"📉 [{datetime.now().strftime('%d/%m %H:%M')}] Estratégia: Compra de PUT ou trava de baixa sugerida – {sinal}")
        elif "follow-on" in texto or "oferta de ações" in texto:
            estrategias.append(f"⚠️ [{datetime.now().strftime('%d/%m %H:%M')}] Estratégia: Evitar CALL – risco de diluição – {sinal}")
        elif "aumento de volume" in texto and "sem notícia" in texto:
            estrategias.append(f"🔍 [{datetime.now().strftime('%d/%m %H:%M')}] Estratégia: Monitorar – possível movimentação institucional – {sinal}")
        else:
            estrategias.append(f"ℹ️ [{datetime.now().strftime('%d/%m %H:%M')}] Nenhuma recomendação clara – {sinal}")

    return estrategias
