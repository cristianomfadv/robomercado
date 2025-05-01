# data_collectors/cvm_oficial_reader.py

import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import json
import os

# Empresas e termos (você pode manter o mesmo que no B3)
empresas_interesse = [
    "AURE3", "AZUL4", "BRKM5", "CMIN3", "SMAL11",
    "IRBR3", "LREN3", "KLBN11", "XPLG11", "HGBS11", "BBAS3"
]

termos_interesse = [
    "dividendo", "provento", "cisão", "fusão",
    "follow-on", "split", "grupamento", "oferta pública", "recompra",
    "venda de participação", "aquisição de controle",
    "rebaixamento de rating", "upgrade de rating",
    "mudança de CEO", "mudança de Conselho",
    "investigação", "multa", "parceria", "joint venture",
    "prévia de resultados", "spin-off", "IPO de subsidiária", "volume atípico"
]

HISTORICO_CVM = "fatos_lidos_cvm.json"

def carregar_historico():
    if os.path.exists(HISTORICO_CVM):
        with open(HISTORICO_CVM, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return []

def salvar_historico(fatos):
    with open(HISTORICO_CVM, "w", encoding="utf-8") as f:
        json.dump(fatos, f, indent=2, ensure_ascii=False)

def capturar_fatos_cvm():
    hoje = datetime.today()
    sete_dias_atras = hoje - timedelta(days=7)

    url = "https://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/FRELEV/data/FRELEV.zip"

    # Essa é uma versão simplificada para testes iniciais — podemos futuramente usar o XML/CSV do repositório completo
    resposta = requests.get("https://www.gov.br/cvm/pt-br/assuntos/mercados/fatos-relevantes")
    soup = BeautifulSoup(resposta.text, "html.parser")

    fatos = []
    fatos_lidos = carregar_historico()

    blocos = soup.select("div.tileItem")

    for bloco in blocos:
        titulo = bloco.find("a").text.strip()
        link = bloco.find("a")["href"]
        data_texto = bloco.find("span", class_="summary-view-icon").text.strip()

        try:
            data_publicacao = datetime.strptime(data_texto, "%d/%m/%Y")
        except:
            continue

        if data_publicacao < sete_dias_atras:
            continue

        id_fato = f"{data_texto} - {titulo}"

        if id_fato in fatos_lidos:
            continue

        titulo_lower = titulo.lower()
        relevante = False

        for termo in termos_interesse:
            if termo in titulo_lower:
                relevante = True
                break
        for empresa in empresas_interesse:
            if empresa in titulo:
                relevante = True
                break

        if relevante:
            fatos.append(f"{data_texto} - {titulo}\nLink: {link}")

        fatos_lidos.append(id_fato)

    salvar_historico(fatos_lidos)

    return fatos

