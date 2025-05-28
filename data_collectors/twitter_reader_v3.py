import requests
import logging
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO)

def fetch_tweets(user, max_retries=3):
    """
    Busca tweets do usuário em múltiplas instâncias Nitter,
    com até `max_retries` tentativas por instância.
    Retorna lista de textos de tweets (ou lista vazia).
    """
    instances = [
        "https://nitter.net",
        "https://nitter.privacydev.net",
        "https://nitter.snopyta.org"
    ]

    for base in instances:
        url = f"{base}/{user}"
        for attempt in range(1, max_retries + 1):
            try:
                resp = requests.get(url, timeout=10)
                resp.raise_for_status()

                soup = BeautifulSoup(resp.text, 'html.parser')
                tweets = [t.get_text(strip=True) for t in soup.select('.tweet-body')]
                if tweets:
                    return tweets
                else:
                    raise ValueError("Nenhum tweet encontrado nesta instância")

            except Exception as e:
                logging.warning(f"Tentativa {attempt} em {url} falhou: {e}")

        logging.info(f"Instância {base} esgotada, tentando próxima")

    logging.error(f"Não foi possível buscar tweets de @{user}")
    return []
