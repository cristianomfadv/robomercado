# data_collectors/infomoney_reader.py

import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime

# Termos e ativos monitorados
termos_chave = [
    "dividendos", "proventos", "cisão", "fusão", "follow-on",
    "oferta pública", "recompra", "venda de participação",
    "aquisição", "IPO", "grupamento", "split", "volume atípico"
]

ativos = [
    "AURE3", "AZUL4", "BRKM5", "CMIN3", "SMAL11",
    "IRBR3", "LREN3", "KLBN11", "XPLG11", "HGBS11", "BBAS3"
]

HISTORICO_INFOMONEY = "noticias_lidas_infomoney.json"

def carregar_historico():
    if os.path.exists(HISTORICO_INFOMONEY):
        with open(HISTORICO_INFOMONEY, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return []

def salvar_historico(lista):
    with open(HISTORICO_INFOMONEY, "w", encoding="utf-8") as f:
        json.dump(lista, f, indent=2, ensure_ascii=False)

def capturar_noticias_infomoney():
    url = "https://www.infomoney.com.br/ultimas-noticias/"
    headers = {"User-Agent": "Mozilla/5.0"}
    noticias_relevantes = []
    historico = carregar_historico()

    try:
        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        cards = soup.select("div.card-post")

        for card in cards:
            titulo_tag = card.find("h2")
            if not titulo_tag:
                continue

            titulo = titulo_tag.text.strip()
            link_tag = card.find("a")
            link = link_tag["href"] if link_tag else ""
            id_noticia = link.split("/")[-2] if "/" in link else titulo[:40]

            if id_noticia in historico:
                continue

            titulo_lower = titulo.lower()
            relevante = any(termo in titulo_lower for termo in termos_chave) or \
                        any(acao.lower() in titulo_lower for acao in ativos)

            if relevante:
                noticias_relevantes.append(f"{titulo}\n{link}")
                historico.append(id_noticia)

    except requests.exceptions.Timeout:
        print("Erro ao capturar InfoMoney: tempo limite excedido (timeout).")
    except requests.exceptions.RequestException as e:
        print(f"Erro ao capturar InfoMoney: {e}")

    salvar_historico(historico)
    return noticias_relevantes
