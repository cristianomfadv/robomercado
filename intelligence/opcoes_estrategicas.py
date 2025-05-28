
import requests
import os
import json
from bs4 import BeautifulSoup
from datetime import datetime

CACHE_DIR = "data/cache_opcoes"
LOG_PATH = "logs/logs_erros_analise.txt"

os.makedirs(CACHE_DIR, exist_ok=True)
os.makedirs("logs", exist_ok=True)

def log_erro(ativo, erro):
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now()}] {ativo}: {erro}\n")

def salvar_cache(ativo, dados):
    caminho = os.path.join(CACHE_DIR, f"{ativo}.json")
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(dados, f)

def carregar_cache(ativo):
    caminho = os.path.join(CACHE_DIR, f"{ativo}.json")
    if os.path.exists(caminho):
        with open(caminho, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

def buscar_preco_fundamentus(ativo):
    try:
        url = f"https://www.fundamentus.com.br/detalhes.php?papel={ativo}"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        td_tags = soup.find_all("td")
        for i, td in enumerate(td_tags):
            if "Cotação" in td.text:
                preco_tag = td_tags[i + 1]
                preco = preco_tag.text.strip().replace(".", "").replace(",", ".")
                preco_float = float(preco)
                return preco_float
        raise Exception("Campo 'Cotação' não localizado.")
    except Exception as e:
        log_erro(ativo, f"Erro Fundamentus: {e}")
        return None

def executar_analise_opcoes():
    ativos = ["VALE3", "PETR4", "BBAS3", "BOVA11", "BBDC4", "KLBN11", "CMIN3", "IRBR3", "GGBR4", "BRKM5"]
    resultados = []

    for ativo in ativos:
        preco_hoje = buscar_preco_fundamentus(ativo)
        if not preco_hoje:
            dados = carregar_cache(ativo)
            if dados:
                preco_hoje = dados[0]
            else:
                resultados.append(f"[ERRO] [{ativo}] Sem dados disponíveis no Fundamentus e sem cache.")
                continue

        # Simula série de 5 dias para efeito de tendência
        serie_simulada = [round(preco_hoje * (1 - 0.01 * i), 2) for i in reversed(range(5))]
        salvar_cache(ativo, [preco_hoje] + serie_simulada)

        preco_passado = serie_simulada[0]

        if preco_hoje > preco_passado * 1.05:
            resultados.append(f"[{ativo}] Tendência de ALTA. Sugerido: trava de alta com alvo em R${preco_hoje * 1.1:.2f}")
        elif preco_hoje < preco_passado * 0.95:
            resultados.append(f"[{ativo}] Tendência de BAIXA. Sugerido: compra seca de PUT ou trava de baixa.")
        else:
            resultados.append(f"[{ativo}] Tendência LATERAL. Sugerido: venda de PUT próxima ao suporte.")

    return resultados
