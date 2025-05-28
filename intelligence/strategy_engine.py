# intelligence/strategy_engine.py

from datetime import datetime

def gerar_recomendacoes(clipping_dict, graficos_dict, eventos_dict):
    recomendacoes = []

    for ativo in graficos_dict:
        estrategia = graficos_dict[ativo]["estrategia"]

        # Reforços de clipping e eventos
        reforco_clipping = clipping_dict.get(ativo, [])
        evento = eventos_dict.get(ativo, "")

        # Comentário estratégico formatado
        comentario = f"{estrategia}"
        if reforco_clipping:
            comentario += f"\n⚠️ {len(reforco_clipping)} notícia(s) relevante(s) detectada(s)."
        if evento:
            comentario += f"\n📅 Evento próximo: {evento}"

        recomendacoes.append({
            "ativo": ativo,
            "tipo": "opcao",
            "comentario": comentario.strip(),
            "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "conteudo": estrategia
        })

    return recomendacoes
