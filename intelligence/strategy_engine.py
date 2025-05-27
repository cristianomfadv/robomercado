# intelligence/strategy_engine.py

def gerar_recomendacoes(alertas_clipping, analises_graficas, eventos_previstos):
    """
    Combina alertas de clipping, análise gráfica e eventos futuros para gerar recomendações finais de operação.
    """
    recomendacoes = []

    for ativo in set(alertas_clipping.keys()) | set(analises_graficas.keys()) | set(eventos_previstos.keys()):
        sinais = []
        comentario = ""
        tipo = None
        preco_entrada = None

        if ativo in alertas_clipping:
            sinais.append("clipping")
            comentario += f"Clipping sinalizou o ativo com: {alertas_clipping[ativo]}\n"

        if ativo in analises_graficas:
            sinais.append("grafico")
            estrategia = analises_graficas[ativo].get("estrategia")
            tipo = estrategia
            comentario += f"Análise gráfica sugeriu: {estrategia}\n"
            # tenta extrair strike como preço de entrada
            import re
            match = re.search(r"R\$ (\d+(?:\.\d+)?)", estrategia)
            if match:
                preco_entrada = float(match.group(1))

        if ativo in eventos_previstos:
            sinais.append("evento")
            comentario += f"Evento previsto: {eventos_previstos[ativo]}\n"

        if sinais:
            recomendacoes.append({
                "ativo": ativo,
                "tipo": tipo or "sem estratégia clara",
                "preco_entrada": preco_entrada or 0.0,
                "mensagem": f"[{ativo}] {' + '.join(sinais).upper()} - {tipo or 'observação'}",
                "comentario": comentario
            })

    return recomendacoes
