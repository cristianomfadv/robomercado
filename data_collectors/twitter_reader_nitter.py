# data_collectors/twitter_reader_nitter.py

import requests
from bs4 import BeautifulSoup
import json
import os

PERFIS = [
    "infomoney", "valoreconomico", "b3_oficial", "suno_research", "br_investnews", "neofeedbr"
]

TERMS = [
    "PETR4", "VALE3", "BBAS3", "BBDC3", "AZUL4", "LREN3", "IRBR3", "KLBN11",
    "dividendos", "lucro", "prejuízo", "balanço", "projeções", "guidance",
    "follow-on", "recompra", "cisão", "oferta de ações", "pagamento", "CVM",
    "venda de ativos", "fato relevante", "desdobramento", "reestruturação"
]

NITTER_INSTANCE = "https://nitter.net"
ARQUIVO_HISTORICO = "tweets_lidos_nitter.json"

def carregar_historico():
    if os.path.exists(ARQUIVO_HISTORICO):
        with open(ARQUIVO_HISTORICO, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def salvar_historico(lista):
    with open(ARQUIVO_HISTORICO, "w", encoding="utf-8") as f:
        json.dump(lista, f, ensure_ascii=False, indent=2)

def capturar_tweets():
    print("🔎 Buscando menções reais via Nitter...")
    headers = {"User-Agent": "Mozilla/5.0"}
    historico = carregar_historico()
    novos_alertas = []

    for perfil in PERFIS:
        url = f"{NITTER_INSTANCE}/{perfil}"
        try:
            resp = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(resp.text, "html.parser")
            tweets = soup.select("div.timeline-item")

            for tweet in tweets:
                conteudo = tweet.select_one(".tweet-content").get_text(strip=True)
                if any(term.lower() in conteudo.lower() for term in TERMS):
                    if conteudo not in historico:
                        alerta = f"[{perfil}] {conteudo}"
                        print("🐦 Tweet relevante:", alerta[:100])
                        novos_alertas.append(alerta)
                        historico.append(conteudo)

                if len(novos_alertas) >= 10:
                    break

        except Exception as e:
            print(f"❌ Erro ao buscar tweets de @{perfil}:", e)

    salvar_historico(historico)
    return novos_alertas
