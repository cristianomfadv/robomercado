from datetime import datetime

def gerar_recomendacoes(analises_graficas):
    decisoes = []
    data = datetime.now().strftime("%Y-%m-%d")

    for texto in analises_graficas:
        if "ALTA" in texto:
            ativo = texto.split("[")[1].split("]")[0]
            recomendacao = {
                "data": data,
                "ativo": ativo,
                "tipo": "trava de alta",
                "strike_sugerido": "+4% sobre preço atual",
                "delta": "+0.5",
                "risco": "baixo",
                "obs": "Baseado em tendência de alta detectada"
            }
            decisoes.append(recomendacao)

        elif "BAIXA" in texto:
            ativo = texto.split("[")[1].split("]")[0]
            recomendacao = {
                "data": data,
                "ativo": ativo,
                "tipo": "trava de baixa",
                "strike_sugerido": "-4% sobre preço atual",
                "delta": "-0.5",
                "risco": "moderado",
                "obs": "Baseado em tendência de baixa detectada"
            }
            decisoes.append(recomendacao)

        elif "LATERAL" in texto:
            ativo = texto.split("[")[1].split("]")[0]
            recomendacao = {
                "data": data,
                "ativo": ativo,
                "tipo": "venda de PUT",
                "strike_sugerido": "strike atual ou 2% abaixo",
                "delta": "-0.2 a -0.3",
                "risco": "baixo",
                "obs": "Estratégia defensiva em cenário lateral"
            }
            decisoes.append(recomendacao)

    return decisoes
