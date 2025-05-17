import time
from datetime import datetime
from data_collectors.twitter_reader_nitter import capturar_tweets
from data_collectors.cvm_oficial_reader import capturar_fatos_cvm
from data_collectors.infomoney_reader import capturar_infomoney
from data_collectors.bloomberg_reader import capturar_bloomberg
from data_collectors.cvm_oficial_reader import capturar_fatos_relevantes
from intelligence.text_analyzer import analisar_texto
from intelligence.decision_maker import gerar_alerta
from dashboard.dashboard import exibir_alertas, salvar_alertas_para_dashboard
from intelligence.opcoes_estrategicas import executar_analise_opcoes
from intelligence.comparador_execucoes import comparar_execucoes
from intelligence.event_tracker import detectar_eventos
from utils.email_alerta import enviar_alerta_email
import os

def fluxo_principal():
    print("\nIniciando captura de dados...\n")

    # Coleta
    try:
        fatos_cvm = capturar_cvm()
    except:
        print("❌ Erro ao capturar da CVM")
        fatos_cvm = []

    try:
        noticias_infomoney = capturar_infomoney()
    except:
        print("❌ Erro ao capturar da InfoMoney")
        noticias_infomoney = []

    try:
        noticias_bloomberg = capturar_bloomberg()
    except:
        print("❌ Erro ao capturar da Bloomberg")
        noticias_bloomberg = []

    try:
        fatos_relevantes = capturar_fatos_relevantes()
    except:
        print("❌ Erro ao capturar fatos relevantes da CVM")
        fatos_relevantes = []

    try:
        print("🔎 Buscando menções reais via Nitter...")
        tweets_importantes = capturar_tweets()
    except:
        print("❌ Erro ao capturar do Twitter")
        tweets_importantes = []

    # Processamento
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

    # Análise de opções às 11h e 15h
    estrategias = []
    hora_atual = datetime.now().hour
    if hora_atual in [11, 15]:
        print("\n📊 Executando análise de opções com base em gráficos...\n")
        try:
            alertas_opcoes = executar_analise_opcoes()
            estrategias.extend(alertas_opcoes)

            print("\n🔁 Comparando execuções com histórico...\n")
            alertas_comparativos = comparar_execucoes()
            estrategias.extend(alertas_comparativos)

        except Exception as e:
            print("❌ Erro ao executar análise de opções:", e)

    # Eventos financeiros relevantes
    try:
        eventos = detectar_eventos()
        estrategias.extend(eventos)
    except Exception as e:
        print("❌ Erro ao detectar eventos:", e)

    # Resultado
    alertas_gerados = analises + estrategias

    print("\n🧾 Exibindo alertas no Dashboard...\n")
    exibir_alertas(alertas_gerados)
    salvar_alertas_para_dashboard(alertas_gerados)

    if estrategias:
        corpo_email = "\n".join(estrategias)
        assunto = f"🚨 Alertas Estratégicos – {datetime.now().strftime('%d/%m %H:%M')}"
        enviar_alerta_email(assunto, corpo_email)

if __name__ == "__main__":
    while True:
        fluxo_principal()
        print("🕒 Aguardando próximo ciclo...\n")
        time.sleep(3600)
