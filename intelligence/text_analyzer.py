# intelligence/text_analyzer.py

# Ativos e termos estratégicos que impactam sua carteira e operações
ATIVOS_INTERESSE = [
    "PETR4", "VALE3", "BBAS3", "IRBR3", "KLBN11", "AZUL4", "LREN3",
    "BRKM5", "AURE3", "CMIN3", "SMAL11", "XPLG11", "HGBS11"
]

EVENTOS_RELEVANTES = [
    "dividendo", "lucro", "prejuízo", "balanço", "cisão", "reestruturação", "guidance",
    "suspensão", "venda de ativos", "follow-on", "oferta", "exercício", "call", "put",
    "delta", "trava", "rolagem", "prêmio", "recompra", "CVM", "fato relevante"
]

# Função que retorna se o texto é relevante
def analisar_texto(texto):
    texto_lower = texto.lower()

    # Verifica se algum ativo está no texto
    ativos_mencionados = [ativo for ativo in ATIVOS_INTERESSE if ativo.lower() in texto_lower]

    # Verifica se algum evento crítico é citado
    eventos_detectados = [evento for evento in EVENTOS_RELEVANTES if evento in texto_lower]

    # Regras para gerar alerta
    if ativos_mencionados and eventos_detectados:
        ativos_str = ", ".join(ativos_mencionados)
        eventos_str = ", ".join(eventos_detectados)
        return f"[ALERTA ESTRATÉGICO] Ativo(s): {ativos_str} | Evento(s): {eventos_str} | Texto: {texto}"

    return None  # Se não cruzar ativo + evento, ignora o texto
