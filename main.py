import os
import sys
import logging
import datetime
import traceback
from dotenv import load_dotenv  # <-- ADICIONADO
load_dotenv()                   # <-- ADICIONADO

# Ajuste os caminhos se estiver rodando fora da raiz do projeto
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# Importação dos módulos principais
from intelligence.opcoes_estrategicas import gerar_sinais_estrategicos
# from intelligence.strategy_engine import gerar_recomendacoes  # caso precise de integração adicional

LOG_FILE = "logs/main.log"
os.makedirs("logs", exist_ok=True)
logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s')

def registrar_erro(msg):
    logging.error(msg)
    with open(LOG_FILE, "a") as f:
        f.write(f"{datetime.datetime.now()}: {msg}\n")

def fluxo_principal():
    try:
        print("Iniciando Robô Mercado Financeiro...")

        # Lista padrão de ativos
        ativos = ["VALE3", "PETR4", "BBAS3", "BOVA11", "BBDC4", "KLBN11", "CMIN3", "IRBR3", "GGBR4", "BRKM5"]

        print("⏳ Gerando sinais táticos de opções para ativos monitorados...")
        sinais_estrategicos = gerar_sinais_estrategicos(ativos)

        print("\n=== SINAIS GERADOS ===")
        for s in sinais_estrategicos:
            if "erro" in s and s["erro"]:
                print(f"[ERRO] {s['ativo']}: {s['erro']}")
            else:
                print(f"{s['ativo']}: Estratégia sugerida: {s['estrategia']} | {s['detalhe']}")

        # Se for integrar com strategy_engine, descomente:
        # print("\n⏳ Gerando decisão final da IA...")
        # recomendacoes = gerar_recomendacoes(sinais_estrategicos)
        # print("RECOMENDAÇÕES FINAIS:", recomendacoes)

        logging.info("Execução concluída sem erros críticos.")
    except Exception as e:
        registrar_erro(f"Erro geral no fluxo principal: {e}\n{traceback.format_exc()}")
        print(f"Erro crítico detectado. Verifique o log em {LOG_FILE}")

if __name__ == "__main__":
    fluxo_principal()
