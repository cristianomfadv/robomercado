# intelligence/event_tracker.py

import json
import os
from datetime import datetime, timedelta

ARQUIVO_EVENTOS = "eventos_agendados.json"

def carregar_eventos_agendados():
    if not os.path.exists(ARQUIVO_EVENTOS):
        return []
    with open(ARQUIVO_EVENTOS, "r", encoding="utf-8") as f:
        return json.load(f)

def salvar_eventos_agendados(eventos):
    with open(ARQUIVO_EVENTOS, "w", encoding="utf-8") as f:
        json.dump(eventos, f, ensure_ascii=False, indent=2)

def registrar_evento(ativo, data, descricao):
    eventos = carregar_eventos_agendados()
    eventos.append({
        "ativo": ativo,
        "data": data,
        "descricao": descricao
    })
    salvar_eventos_agendados(eventos)

def verificar_eventos_agendados():
    eventos = carregar_eventos_agendados()
    hoje = datetime.now().date()
    cinco_dias = hoje + timedelta(days=5)
    dois_dias = hoje + timedelta(days=2)

    alertas = []

    for evento in eventos:
        data_evento = datetime.strptime(evento["data"], "%Y-%m-%d").date()

        if data_evento == cinco_dias:
            alertas.append(f"[5 DIAS] {evento['ativo']} - {evento['descricao']} (em {evento['data']})")
        elif data_evento == dois_dias:
            alertas.append(f"[2 DIAS] {evento['ativo']} - {evento['descricao']} (em {evento['data']})")

    return alertas
