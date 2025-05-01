# main.py

from data_collectors.twitter_reader import capturar_tweets
from data_collectors.cvm_oficial_reader import capturar_fatos_cvm
from data_collectors.cvm_reader import capturar_fatos_relevantes
from data_collectors.infomoney_reader import capturar_noticias_infomoney
from data_collectors.bloomberg_reader import capturar_noticias_bloomberg

from intelligence.text_analyzer import analisar_texto
from intelligence.decision_maker import gerar_alerta
from dashboard.exibir_console import exibir_alertas


import time
import json
from datetime import datetime

def fluxo_principal():
    print("Iniciando captura de dados...")

    try:
        fatos_relevantes = capturar_fatos_relevantes()
    except:
        print("Erro ao capturar da B3")
        fatos_relevantes = []

    try:
        fatos_cvm = capturar_fatos_cvm()
    except:
        print("Erro ao capturar da CVM")
        fatos_cvm = []

    try:
        tweets_importantes = capturar_tweets()
    except:
        print("Erro ao capturar do Twitter")
        tweets_importantes = []

    try:
        noticias_infomoney = capturar_noticias_infomoney()
    except:
        print("Erro ao capturar InfoMoney")
        noticias_infomoney = []

    try:
        noticias_bloomberg = capturar_noticias_bloomberg()
    except:
        print("Erro ao capturar Bloomberg Línea")
        noticias_bloomberg = []

    print("Analisando informações capturadas...")

    todas_as_fontes = (
        fatos_relevantes +
        fatos_cvm +
        tweets_importantes +
        noticias_infomoney +
        noticias_bloomberg
    )

    analises = []
    for item in todas_as_fontes:
        analise = analisar_texto(item)
        if analise:
            alerta = gerar_alerta(analise)
            analises.append(alerta)

    print("Exibindo alertas no Dashboard...")
    exibir_alertas(analises)

    # Salvar os alertas em um arquivo JSON para o dashboard
    def salvar_alertas_para_dashboard(alertas):
        dados = []
        for alerta in alertas:
            dados.append({
                "data": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "fonte": alerta.split(":")[0].strip() if ":" in alerta else "Desconhecida",
                "conteudo": alerta
            })
        with open("alertas_gerados.json", "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)

    salvar_alertas_para_dashboard(analises)

if __name__ == "__main__":
    while True:
        fluxo_principal()
        print("Aguardando próximo ciclo...")
        time.sleep(3600)
