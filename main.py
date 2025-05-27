import schedule
import time
import json
import os

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

# Lista fixa de ativos
ATIVOS_FIXOS = ["PETR4", "VALE3", "BBAS3", "KLBN11", "CMIN3", "IRBR3", "GGBR4", "BBDC4", "BOVA11", "BRKM5"]

# Funções auxiliares para transformar listas em dicionários por ativo
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

    # 1. Clipping (Notícias + Twitter + CVM)
    noticias_infomoney = capturar_noticias_infomoney()
    noticias_bloomberg = capturar_noticias_bloomberg()
    eventos_cvm = capturar_fatos_cvm()
    tweets = capturar_tweets()

    # 2. Volume incomum B3
    volumes = executar_monitoramento_volumes()

    # 3. Análise textual e classificação
    analises_clipping_raw = analisar_texto(
        noticias_infomoney + noticias_bloomberg + eventos_cvm + tweets + volumes
    )

    # 4. Eventos futuros
    eventos_previstos_raw = verificar_eventos_agendados()

    # 5. Estratégia de opções (análise gráfica)
    analises_graficas_raw = executar_analise_opcoes()

    # 6. Engine final (integra tudo e gera operação)
    alertas_finais = estrategia_final(
        extrair_ativos_clipping(analises_clipping_raw),
        extrair_ativos_graficos(analises_graficas_raw),
        extrair_ativos_eventos(eventos_previstos_raw)
    )

    # 7. Backtest log
    for alerta in alertas_finais:
        registrar_alerta_historico(alerta)

    # 8. Email
    enviar_email_alerta([
        alerta["comentario"] if isinstance(alerta, dict) else str(alerta)
        for alerta in alertas_finais
    ])

    # 9. Exibição e armazenamento
    todos_alertas = analises_clipping_raw + analises_graficas_raw + eventos_previstos_raw
    exibir_alertas(todos_alertas)
    salvar_alertas_para_dashboard(todos_alertas)
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
