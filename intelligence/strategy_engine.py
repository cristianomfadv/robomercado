"""
strategy_engine.py
Gera recomendações finais combinando sinais estratégicos.
"""

import logging
import datetime
import os

LOG_FILE = "logs/strategy_engine.log"
os.makedirs("logs", exist_ok=True)
logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s')

def registrar_erro_strategy(msg):
    logging.error(msg)
    with open(LOG_FILE, "a") as f:
        f.write(f"{datetime.datetime.now()}: {msg}\n")

def gerar_recomendacoes(sinais_estrategicos):
    """
    Processa uma lista de sinais estratégicos (output do módulo opcoes_estrategicas)
    e retorna uma lista de recomendações finais de operação.
    Cada sinal é um dict: {"ativo": "VALE3", "estrategia": "...", "detalhe": "..."}
    """
    recomendacoes = []
    for sinal in sinais_estrategicos:
        try:
            if "erro" in sinal:
                recomendacoes.append({
                    "ativo": sinal.get("ativo", "N/D"),
                    "recomendacao": "Não foi possível gerar recomendação.",
                    "detalhe": sinal["erro"]
                })
                continue

            # Exemplo de integração de lógica extra: pode cruzar com volume, eventos, etc. no futuro.
            if sinal["estrategia"] == "Trava de alta":
                recomendacoes.append({
                    "ativo": sinal["ativo"],
                    "recomendacao": "Sugerir trava de alta com CALL para o ativo.",
                    "detalhe": sinal["detalhe"]
                })
            elif sinal["estrategia"] == "Compra seca de PUT":
                recomendacoes.append({
                    "ativo": sinal["ativo"],
                    "recomendacao": "Sugerir compra seca de PUT ou trava de baixa.",
                    "detalhe": sinal["detalhe"]
                })
            else:
                recomendacoes.append({
                    "ativo": sinal["ativo"],
                    "recomendacao": "Sem recomendação clara no momento.",
                    "detalhe": sinal.get("detalhe", "")
                })
        except Exception as e:
            registrar_erro_strategy(f"Erro ao processar {sinal}: {e}")
            recomendacoes.append({
                "ativo": sinal.get("ativo", "N/D"),
                "recomendacao": "Erro interno ao processar recomendação.",
                "detalhe": str(e)
            })
    return recomendacoes
