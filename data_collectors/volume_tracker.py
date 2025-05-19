# data_collectors/volume_tracker.py

import yfinance as yf
import pandas as pd

def executar_monitoramento_volumes():
    ativos = ["VALE3.SA", "PETR4.SA", "BBAS3.SA", "BOVA11.SA", "BBDC4.SA"]
    alertas = []

    for ativo in ativos:
        try:
            dados = yf.download(ativo, period="5d", interval="1d", progress=False)
            if dados is not None and not dados.empty:
                volumes = dados["Volume"].tail(5)
                media = volumes[:-1].mean()
                ultimo = volumes[-1]

                if ultimo > media * 1.5:
                    alerta = {
                        "ativo": ativo.replace(".SA", ""),
                        "tipo": "🔍 Alerta de volume",
                        "detalhe": f"Volume de hoje ({ultimo}) muito acima da média ({int(media)})."
                    }
                    alertas.append(alerta)
        except Exception as e:
            print(f"Erro ao processar {ativo}: {e}")

    return alertas
