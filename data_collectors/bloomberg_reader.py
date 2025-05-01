# data_collectors/bloomberg_reader.py

import requests
from bs4 import BeautifulSoup
import json
import os

termos_chave = [
    "dividendos", "proventos", "cisão", "fusão", "follow-on",
    "oferta pública", "recompra", "grupamento", "split",
    "volume atípico", "venda de participação", "aquisição"
]

ativos = [
    "AURE3", "AZUL4", "BRKM5", "CMIN3", "SMAL11",
    "IRBR3", "LREN3", "KLBN11", "XPLG11", "HGBS11", "BBAS3"
]

HISTORICO_BLOOMBERG = "noticias_lidas_bloomberg.json"

def carregar_historico():
    if os.path.exists(HISTORICO_BLOOMBERG):
        with open(HISTORICO_BLOOMBERG, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return []

def salvar_historico(lista):
    with open(HISTORICO_BLOOMBERG, "w", encoding="utf-8") as f:
        json.dump(lista, f, indent=2, ensure_ascii=False)

def capturar_noticias_bloomberg():
    urls = [
        "https://www.bloomberglinea.com.br/ultimas/",
        "https://www.bloomberglinea.com/ultimas/"
    ]
    headers = {"User-Agent": "Mozilla/5.0"}
    noticias = []
    historico = carregar_historico()

    for url in urls:
        try:
            r = requests.get(url, headers=headers)
            soup = BeautifulSoup(r.text, "html.parser")

            cards = soup.select("article a")

            for card in cards:
                link = card["href"]
                titulo = card.text.strip()

                if not titulo or not link:
                    continue

                if not link.startswith("http"):
                    link = "https://www.bloomberglinea.com" + link

                id_noticia = link.split("/")[-2] if "/" in link else titulo[:40]

                if id_noticia in historico:
                    continue

                titulo_lower = titulo.lower()
                relevante = False

                for termo in termos_chave:
                    if termo in titulo_lower:
                        relevante = True
                        break
                for acao in ativos:
                    if acao.lower() in titulo_lower:
                        relevante = True
                        break

                if relevante:
                    noticias.append(f"{titulo}\n{link}")
                    historico.append(id_noticia)

        except Exception as e:
            print(f"Erro ao capturar Bloomberg Línea: {e}")

    salvar_historico(historico)
    return noticias

