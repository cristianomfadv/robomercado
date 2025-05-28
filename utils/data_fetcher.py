import yfinance as yf
import requests
import logging
import pandas as pd
from intelligence.config import ALPHA_VANTAGE_API_KEY

logging.basicConfig(level=logging.INFO)

def fetch_ticker_data(ticker, period="5d"):
    """
    Tenta obter dados de preço via yfinance.
    Se falhar ou retornar vazio, faz fallback para Alpha Vantage.
    Retorna um DataFrame pandas com as cotações.
    """
    symbol = f"{ticker}.SA"
    try:
        tk = yf.Ticker(symbol)
        df = tk.history(period=period)
        if df.empty:
            raise ValueError("Nenhum dado retornado pelo yfinance")
        return df

    except Exception as e:
        logging.warning(f"yfinance falhou para {symbol}: {e}")

        # Fallback Alpha Vantage
        url = (
            "https://www.alphavantage.co/query"
            f"?function=TIME_SERIES_DAILY&symbol={symbol}"
            f"&outputsize=compact&apikey={ALPHA_VANTAGE_API_KEY}"
        )
        resp = requests.get(url, timeout=10)
        data = resp.json().get("Time Series (Daily)", {})
        if not data:
            logging.error(f"Alpha Vantage também falhou para {symbol}")
            return pd.DataFrame()

        df_av = pd.DataFrame.from_dict(data, orient="index").sort_index()
        df_av.index = pd.to_datetime(df_av.index)
        # Ajusta colunas para o mesmo padrão do yfinance
        df_av.columns = [col.split(" ")[1] for col in df_av.columns]
        return df_av
