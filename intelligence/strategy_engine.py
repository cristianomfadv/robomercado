def gerar_recomendacoes(dados):
    recomendacoes = []

    clipping = dados.get("clipping", [])
    graficos = dados.get("graficos", [])
    eventos = dados.get("eventos", [])
    volume = dados.get("volume", [])

    for item in graficos:
        ativo = item.get("ticker")
        tendencia = item.get("tendencia")

        if tendencia == "alta":
            recomendacoes.append({
                "ticker": ativo,
                "estrategia": "trava de alta",
                "comentario": "Tendência de alta detectada nos gráficos."
            })
        elif tendencia == "baixa":
            recomendacoes.append({
                "ticker": ativo,
                "estrategia": "compra de PUT",
                "comentario": "Tendência de baixa identificada no gráfico."
            })

    for noticia in clipping:
        if noticia.get("impacto") == "alto":
            recomendacoes.append({
                "ticker": noticia.get("ticker"),
                "estrategia": "venda coberta de PUT",
                "comentario": f"Notícia de alto impacto: {noticia.get('titulo')}"
            })

    for evento in eventos:
        if evento.get("importancia") == "alta":
            recomendacoes.append({
                "ticker": evento.get("ticker"),
                "estrategia": "proteção com trava",
                "comentario": f"Evento futuro relevante: {evento.get('descricao')}"
            })

    for anomalia in volume:
        recomendacoes.append({
            "ticker": anomalia.get("ticker"),
            "estrategia": "observação de fluxo",
            "comentario": f"Volume atípico detectado: {anomalia.get('detalhes')}"
        })

    return recomendacoes
