import schedule
import time
from utils.email_alerta import enviar_alerta_email
from data_collectors.twitter_reader_nitter import capturar_tweets
from data_collectors.infomoney_reader import capturar_noticias_infomoney
from data_collectors.bloomberg_reader import capturar_noticias_bloomberg
from data_collectors.cvm_oficial_reader import capturar_fatos_cvm
from data_collectors.volume_tracker import executar_monitoramento_volumes
from intelligence.text_analyzer import analisar_textos
from intelligence.opcoes_estrategicas import executar_analise_opcoes
from intelligence.strategy_engine import gerar_recomendacoes as estrategia_final
from intelligence.event_tracker import verificar_eventos_agendados
from intelligence.backtest_engine import registrar_alerta_historico
from dashboard.exibir_console import exibir_alertas
from dashboard.custos_monitor import registrar_execucao
import json
import os


def fluxo_principal():
    print("\nIniciando captura de dados...\n")

    # 1. Clipping (Notícias + Twitter + CVM)
    noticias_infomoney = coletar_noticias_infomoney()
    noticias_bloomberg = coletar_noticias_bloomberg()
    eventos_cvm = buscar_eventos_cvm()
    tweets = capturar_tweets()

    # 2. Volume incomum B3
    volumes = executar_monitoramento_volumes()

    # 3. Análise textual e classificação
    analises = analisar_textos(noticias_infomoney + noticias_bloomberg + eventos_cvm + tweets + volumes)

    # 4. Eventos futuros
    eventos_futuros = verificar_eventos_agendados()
    analises.extend(eventos_futuros)

    # 5. Estratégia de opções
    estrategias = executar_analise_opcoes()
    analises.extend(estrategias)

    # 6. Engine final (integra tudo e gera operação)
    alertas_finais = estrategia_final(analises)

    # 7. Backtest log
    for alerta in alertas_finais:
        registrar_alerta_historico(alerta)

    # 8. Email
    enviar_email_alerta(alertas_finais)

    # 9. Exibição e armazenamento
    exibir_alertas(analises)
    salvar_alertas_para_dashboard(analises)
    registrar_execucao()


def salvar_alertas_para_dashboard(alertas):
    caminho = "alertas_gerados.json"
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(alertas, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    fluxo_principal()

    # Agendamento para rodar 24h
    schedule.every().day.at("11:00").do(fluxo_principal)
    schedule.every().day.at("15:00").do(fluxo_principal)

    while True:
        schedule.run_pending()
        time.sleep(60)
