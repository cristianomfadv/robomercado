# main.py

from data_collectors.twitter_reader_nitter import capturar_tweets
from data_collectors.cvm_oficial_reader import capturar_fatos_cvm
from data_collectors.cvm_reader import capturar_fatos_relevantes
from data_collectors.infomoney_reader import capturar_noticias_infomoney
from data_collectors.bloomberg_reader import capturar_noticias_bloomberg
from data_collectors.volume_tracker import executar_monitoramento_volumes

from intelligence.text_analyzer import analisar_texto
from intelligence.decision_maker import gerar_alerta
from intelligence.opcoes_estrategicas import executar_analise_opcoes
from intelligence.event_tracker import detectar_eventos_relevantes
from intelligence.strategy_engine import gerar_recomendacoes
from dashboard.exibir_console import exibir_alertas
from dashboard.painel_execucao import registrar_alertas
from dashboard.custos_monitor import registrar_custos_execucao

import json
import time
from datetime import datetime

def fluxo_principal():
    print("\nIniciando captura de dados...")

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
        print("❌ Erro ao capturar do Twitter")
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

    try:
        alertas_volume = executar_monitoramento_volumes()
    except:
        print("❌ Erro ao monitorar volumes")
        alertas_volume = []

    try:
        alertas_eventos = detectar_eventos_relevantes()
    except:
        print("❌ Erro ao detectar eventos futuros")
        alertas_eventos = []

    print("Analisando informações capturadas...")

    todas_as_fontes = (
        fatos_relevantes +
        fatos_cvm +
        tweets_importantes +
        noticias_infomoney +
        noticias_bloomberg +
        alertas_volume +
        alertas_eventos
    )

    analises = []
    for item in todas_as_fontes:
        analise = analisar_texto(item)
        if analise:
            alerta = gerar_alerta(analise)
            analises.append(alerta)

    # 🧠 Estratégia final baseada em sinais cruzados
    try:
        recomendacoes = gerar_recomendacoes(analises)
        analises.extend(recomendacoes)
    except:
        print("⚠️ Erro ao gerar recomendações finais")

    # 💹 Execução da análise de opções (11h e 15h)
    try:
        opcoes = executar_analise_opcoes()
        analises.extend(opcoes)
    except:
        print("⚠️ Erro na análise de opções")

    print("Exibindo alertas no Dashboard...")
    exibir_alertas(analises)
    registrar_alertas(analises)
    registrar_custos_execucao()

    # Salvar para histórico local (opcional)
    with open("alertas_gerados.json", "w", encoding="utf-8") as f:
        json.dump([{
            "data": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "conteudo": alerta
        } for alerta in analises], f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    while True:
        fluxo_principal()
        print("\n🕒 Aguardando próximo ciclo...")
        time.sleep(3600)  # Executa a cada 1 hora
