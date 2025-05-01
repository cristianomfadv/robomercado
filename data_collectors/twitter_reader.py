# data_collectors/twitter_reader.py

import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import json
import os

# Empresas e termos monitorados
ativos = [
    "AURE3", "AZUL4", "BRKM5", "CMIN3", "SMAL11",
    "IRBR3", "LREN3", "KLBN11", "XPLG11", "HGBS11", "BBAS3"
]

termos = [
    "dividendos", "cisão", "fusão", "follow-on",
    "oferta pública", "recompra de ações", "volume atípico",
    "investigação CVM", "CEO", "resultado preliminar"
]

HISTORICO_X = "tweets_lidos.json"

def carregar_historico():
    if os.path.exists(HISTORICO_X):
        with open(HISTORICO_X, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return []

def salvar_historico(lista):
    with open(HISTORICO_X, "w", encoding="utf-8") as f:
        json.dump(lista, f, indent=2, ensure_ascii=False)

def capturar_tweets():
    base_url = "https://www.google.com/search?q=site:twitter.com+"
    headers = {"User-Agent": "Mozilla/5.0"}
    tweets_novos = []
    historico = carregar_historico()

    # Verifica últimos 2 dias
    hoje = datetime.today()
    data_limite = (hoje - timedelta(days=2)).strftime("%Y-%m-%d")

    for termo in termos + ativos:
        query = f"{termo}+since:{data_limite}"
        url = base_url + query.replace(" ", "+")

        try:
            r = requests.get(url, headers=headers)
            soup = BeautifulSoup(r.text, "html.parser")
            resultados = soup.select("div.g")

            for resultado in resultados:
                link_tag = resultado.find("a")
                if link_tag:
                    link = link_tag["href"]
                    titulo = resultado.text.strip()
                    id_tweet = link[-30:]  # identificação simples

                    if id_tweet not in historico:
                        tweets_novos.append(f"{termo.upper()} detectado em tweet:\n{titulo}\n{link}")
                        historico.append(id_tweet)

        except Exception as e:
            print(f"Erro ao buscar '{termo}': {e}")
            continue

    salvar_historico(historico)
    return tweets_novos

