# data_collectors/volume_tracker.py

from datetime import datetime
import random

def detectar_anomalias_volume():
    # Simulação de ativos monitorados
    ativos = ["PETR4", "VALE3", "BBAS3", "KLBN11", "IRBR3"]
    alertas_volume = []

    for ativo in ativos:
        volume_hoje = random.randint(50000000, 300000000)
        media_volume = random.randint(40000000, 100000000)

        if volume_hoje > media_volume * 2:
            alerta = f"📊 {ativo}: Volume de negociação {volume_hoje:,} superou o dobro da média ({media_volume:,}) – possível entrada institucional [{datetime.now().strftime('%d/%m %H:%M')}]"
            alertas_volume.append(alerta)

    return alertas_volume
