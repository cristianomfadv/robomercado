# data_collectors/cvm_reader.py

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

def capturar_fatos_relevantes():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    try:
        # Cria o navegador sem precisar passar o caminho do driver
        driver = webdriver.Chrome(options=chrome_options)

        # Acessa a página da B3
        url = "https://www.b3.com.br/pt_br/produtos-e-servicos/negociacao/renda-variavel/acoes/consultas/informacoes-por-periodo-8ae490ca871654460187e80576bf03a0/fatos-relevantes/"
        driver.get(url)

        time.sleep(5)  # Espera a página carregar

        fatos = []

        # Pega as linhas da tabela
        linhas = driver.find_elements("css selector", "table tbody tr")

        for linha in linhas[:5]:  # Só os 5 primeiros
            colunas = linha.find_elements("tag name", "td")
            if len(colunas) >= 2:
                empresa = colunas[0].text.strip()
                assunto = colunas[1].text.strip()
                if assunto:
                    fatos.append(f"{empresa} - {assunto}")

        return fatos

    except Exception as e:
        print(f"Erro ao capturar Fatos Relevantes com Selenium: {e}")
        return []

    finally:
        driver.quit()
