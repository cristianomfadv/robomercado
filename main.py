import time
from data_collectors.clipping_reader import ler_clipping_hoje
from data_collectors.event_tracker import detectar_eventos_futuros
from intelligence.opcoes_estrategicas import analisar_graficos
from intelligence.strategy_engine import gerar_recomendacoes
from intelligence.volume_tracker import detectar_anomalias_volume
from intelligence.backtest_engine import registrar_alerta_historico
from dashboard.painel_execucao import exibir_alertas_no_painel
from utils.email_alerta import enviar_alerta_email

def fluxo_principal():
    print("Iniciando captura de dados...")

    clipping_diario = ler_clipping_hoje()
    analises_graficas = analisar_graficos()
    eventos_futuros = detectar_eventos_futuros()
    anomalias_volume = detectar_anomalias_volume()

    print("🔎 Buscando menções reais via Nitter...")
    # Erros ao buscar tweets são tratados internamente

    dados = {
        "clipping": clipping_diario,
        "graficos": analises_graficas,
        "eventos": eventos_futuros,
        "volume": anomalias_volume
    }

    alertas_finais = gerar_recomendacoes(dados)
    registrar_alerta_historico(alertas_finais)
    exibir_alertas_no_painel(alertas_finais)
    enviar_alerta_email(alertas_finais)

    print("✅ Robô finalizou o ciclo.")

if __name__ == "__main__":
    print("Iniciando Robô Mercado Financeiro...")
    while True:
        try:
            fluxo_principal()
        except Exception as e:
            print(f"Erro durante execução: {e}")
        time.sleep(3600)
