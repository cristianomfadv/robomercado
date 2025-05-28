import schedule
import time
import json
import os
import traceback

from utils.email_alerta import enviar_email_alerta
from data_collectors.twitter_reader_nitter import capturar_tweets
from data_collectors.infomoney_reader import capturar_noticias_infomoney
from data_collectors.bloomberg_reader import capturar_noticias_bloomberg
from data_collectors.cvm_oficial_reader import capturar_fatos_cvm
from data_collectors.volume_tracker import executar_monitoramento_volumes
from intelligence.text_analyzer import analisar_texto
from intelligence.opcoes_estrategicas import executar_analise_opcoes
from intelligence.strategy_engine import gerar_recomendacoes as estrategia_final
from intelligence.event_tracker import verificar_eventos_agendados
from intelligence.backtest_engine import registrar_alerta_historico
from dashboard.exibir_console import exibir_alertas
from dashboard.custos_monitor import registrar_execucao

ATIVOS_FIXOS = ["PETR4", "VALE3", "BBAS3", "KLBN11", "CMIN3", "IRBR3", "GGBR4", "BBDC4", "BOVA11", "BRKM5"]

def extrair_ativos_clipping(alertas):
    dicionario = {}
    for alerta in alertas:
        for ativo in ATIVOS_FIXOS:
            if ativo in alerta:
                dicionario.setdefault(ativo, []).append(alerta)
    return dicionario

def extrair_ativos_eventos(eventos):
    dicionario = {}
    for e in eventos:
        for ativo in ATIVOS_FIXOS:
            if ativo in e:
                dicionario[ativo] = e
    return dicionario

def extrair_ativos_graficos(lista):
    dicionario = {}
    for item in lista:
        for ativo in ATIVOS_FIXOS:
            if ativo in item:
                dicionario[ativo] = {"estrategia": item}
    return dicionario

def fluxo_principal():
    print("\nIniciando captura de dados...\n")
    try:
        noticias_infomoney = capturar_noticias_infomoney()
    except Exception:
        noticias_infomoney = []
        print("Erro ao capturar InfoMoney:\n", traceback.format_exc())

    try:
        noticias_bloomberg = capturar_noticias_bloomberg()
    except Exception:
        noticias_bloomberg = []
        print("Erro ao capturar Bloomberg:\n", traceback.format_exc())

    try:
        eventos_cvm = capturar_fatos_cvm()
    except Exception:
        eventos_cvm = []
        print("Erro ao capturar CVM:\n", traceback.format_exc())

    try:
        tweets = capturar_tweets()
    except Exception:
        tweets = []
        print("Erro ao capturar tweets:\n", traceback.format_exc())

    try:
        volumes = executar_monitoramento_volumes()
    except Exception:
        volumes = []
        print("Erro ao capturar volumes:\n", traceback.format_exc())

    try:
        analises_clipping_raw = analisar_texto(
            noticias_infomoney + noticias_bloomberg + eventos_cvm + tweets + volumes
        )
    except Exception:
        analises_clipping_raw = []
        print("Erro ao analisar textos:\n", traceback.format_exc())

    try:
        eventos_previstos_raw = verificar_eventos_agendados()
    except Exception:
        eventos_previstos_raw = []
        print("Erro ao verificar eventos:\n", traceback.format_exc())

    try:
        analises_graficas_raw = executar_analise_opcoes()
    except Exception:
        analises_graficas_raw = []
        print("Erro na análise gráfica:\n", traceback.format_exc())

    try:
        alertas_finais = estrategia_final(
            extrair_ativos_clipping(analises_clipping_raw),
            extrair_ativos_graficos(analises_graficas_raw),
            extrair_ativos_eventos(eventos_previstos_raw)
        )
    except Exception:
        alertas_finais = []
        print("Erro ao gerar recomendação final:\n", traceback.format_exc())

    try:
        for alerta in alertas_finais:
            registrar_alerta_historico(alerta)
    except Exception:
        print("Erro ao registrar backtest:\n", traceback.format_exc())

    try:
        enviar_email_alerta([
            alerta["comentario"] if isinstance(alerta, dict) else str(alerta)
            for alerta in alertas_finais
        ])
    except Exception:
        print("Erro ao enviar email:\n", traceback.format_exc())

    try:
        todos_alertas = analises_clipping_raw + analises_graficas_raw + eventos_previstos_raw
        exibir_alertas(todos_alertas)
        salvar_alertas_para_dashboard(todos_alertas)
        registrar_execucao()
    except Exception:
        print("Erro na exibição/salvamento dos alertas:\n", traceback.format_exc())

def salvar_alertas_para_dashboard(alertas):
    caminho = "alertas_gerados.json"
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(alertas, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    fluxo_principal()

    # Agendamento
    schedule.every().day.at("11:00").do(fluxo_principal)
    schedule.every().day.at("15:00").do(fluxo_principal)

    while True:
        schedule.run_pending()
        time.sleep(60)
