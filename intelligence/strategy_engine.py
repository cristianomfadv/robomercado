def gerar_recomendacoes(alertas_fundidos, eventos=None, sinais_estrategicos=None):
    recomendacoes = []

    for alerta in alertas_fundidos:
        if "[ALTA]" in alerta:
            recomendacoes.append({
                "ativo": extrair_ativo(alerta),
                "tipo": "trava de alta",
                "preco_entrada": extrair_preco(alerta),
                "alvo": extrair_preco(alerta) * 1.1,
                "direcao": "compra"
            })
        elif "[BAIXA]" in alerta:
            recomendacoes.append({
                "ativo": extrair_ativo(alerta),
                "tipo": "trava de baixa",
                "preco_entrada": extrair_preco(alerta),
                "alvo": extrair_preco(alerta) * 0.9,
                "direcao": "venda"
            })
        else:
            recomendacoes.append({
                "ativo": extrair_ativo(alerta),
                "tipo": "venda de PUT",
                "preco_entrada": extrair_preco(alerta),
                "alvo": extrair_preco(alerta),
                "direcao": "venda"
            })

    return recomendacoes

def extrair_ativo(alerta):
    import re
    match = re.search(r"\[(.*?)\]", alerta)
    return match.group(1) if match else "ATIVO"

def extrair_preco(alerta):
    import re
    match = re.search(r"R\\$([0-9]+,[0-9]{2})", alerta)
    if match:
        preco_str = match.group(1).replace(",", ".")
        return float(preco_str)
    return 0.0
