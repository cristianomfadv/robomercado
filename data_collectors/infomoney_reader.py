
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def capturar_noticias_infomoney():
    url = "https://www.infomoney.com.br/mercados/"
    headers = {"User-Agent": "Mozilla/5.0"}
    noticias = []

    try:
        resposta = requests.get(url, headers=headers, timeout=10)
        resposta.raise_for_status()
        soup = BeautifulSoup(resposta.text, "html.parser")

        blocos = soup.select("div.article-card__content")

        for bloco in blocos[:10]:  # Limita a 10 notícias mais recentes
            titulo_tag = bloco.find("a", class_="article-card__title")
            resumo_tag = bloco.find("p", class_="article-card__description")

            if titulo_tag:
                titulo = titulo_tag.text.strip()
                link = titulo_tag.get("href", "#").strip()
                resumo = resumo_tag.text.strip() if resumo_tag else ""
                noticias.append(f"[INFOMONEY] {titulo} — {resumo} ({link})")
    except Exception as e:
        noticias.append(f"[ERRO] Falha ao capturar InfoMoney: {e}")

    return noticias
