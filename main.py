from data_collectors.twitter_reader_nitter import capturar_tweets
from data_collectors.cvm_oficial_reader import capturar_fatos_cvm
from data_collectors.cvm_reader import capturar_fatos_relevantes
from data_collectors.infomoney_reader import capturar_noticias_infomoney
from data_collectors.bloomberg_reader import capturar_noticias_bloomberg
from data_collectors.volume_tracker import executar_monitoramento_volumes

from intelligence.opcoes_estrategicas import executar_analise_opcoes
from intelligence.text_analyzer import analisar_texto
from intelligence.decision_maker import gerar_alerta
from intelligence.strategy_engine import gerar_estrategia_recomendada as gerar_recomendacoes
from intelligence.backtest_engine import registrar_resultados
from intelligence.event_tracker import rastrear_eventos  # CORRETO AQUI

from dashboard.exibir_console import exibir_alertas
from dashboard.painel_execucao import atualizar_painel
from dashboard.custos_monitor import registrar_execucao

import json
import time
from datetime import datetime

def fluxo_principal():
    print("\nIniciando captura de dados...\n")

    try:
        fatos_relevantes = capturar_fatos_relevantes()
    except:
        print("❌ Erro ao capturar da B3")
        fatos_relevantes = []

    try:
        fatos_cvm = capturar_fatos_cvm()
    except:
        print("❌ Erro ao capturar da CVM")
        fatos_cvm = []

    try:
        tweets_importantes = capturar_tweets()
    except:
        print("❌ Erro ao capturar do Twitter/Nitter")
        tweets_importantes = []

    try:
        noticias_infomoney = capturar_noticias_infomoney()
    except:
        print("❌ Erro ao capturar InfoMoney")
        noticias_infomoney = []

    try:
        noticias_bloomberg = capturar_noticias_bloomberg()
    except:
        print("❌ Erro ao capturar Bloomberg Línea")
        noticias_bloomberg = []

    print("Analisando informações capturadas...\n")

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

    # Captura e tratamento de eventos futuros
    eventos_detectados = rastrear_eventos()
    if eventos_detectados:
        analises.extend(eventos_detectados)

    # Recomendação final combinada
    recomendacoes = gerar_recomendacoes(analises)
    analises.extend(recomendacoes)

    # Backtest e registro
    registrar_resultados(recomendacoes)

    # Execução de rotina de opções (11h e 15h)
    executar_analise_opcoes()

    # Monitoramento de volume institucional
    executar_monitoramento_volumes()

    # Exibição e armazenamento
    exibir_alertas(analises)
    atualizar_painel(analises)
    salvar_alertas_para_dashboard(analises)
    registrar_execucao()

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

if __name__ == "__main__":
    while True:
        fluxo_principal()
        print("\n🕒 Aguardando próximo ciclo...\n")
        time.sleep(3600)
