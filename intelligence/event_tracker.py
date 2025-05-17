# intelligence/event_tracker.py

from datetime import datetime, timedelta

# Simulação de eventos futuros por ativo
eventos_agendados = [
    {"ativo": "BBAS3", "evento": "divulgação de resultados", "data": "2025-05-22"},
    {"ativo": "IRBR3", "evento": "vencimento de opções", "data": "2025-05-20"},
    {"ativo": "KLBN11", "evento": "reunião de conselho", "data": "2025-05-21"},
    {"ativo": "PETR4", "evento": "pagamento de dividendos", "data": "2025-05-27"},
]

def analisar_impacto_evento(ativo, evento):
    evento = evento.lower()

    if "resultados" in evento:
        return f"📊 {ativo}: Balanço previsto. Histórico sugere alta após divulgação. Sinal de oportunidade para CALL ou trava de alta."
    elif "opções" in evento:
        return f"🟡 {ativo}: Vencimento de opções próximo. Potencial aumento de volatilidade. Avaliar hedge ou encerramento antecipado."
    elif "conselho" in evento:
        return f"🔍 {ativo}: Reunião de conselho marcada. Pode haver anúncios estratégicos. Monitorar movimentações incomuns."
    elif "dividendos" in evento:
        return f"🟢 {ativo}: Data de pagamento de dividendos. Tendência histórica de valorização pré-data. Sugerida venda coberta de PUT."
    else:
        return f"ℹ️ {ativo}: Evento agendado – {evento}"

def rastrear_eventos():
    hoje = datetime.now().date()
    alertas_eventos = []

    for evento in eventos_agendados:
        data_evento = datetime.strptime(evento["data"], "%Y-%m-%d").date()
        dias_para_evento = (data_evento - hoje).days

        if dias_para_evento in [5, 2]:
            interpretacao = analisar_impacto_evento(evento["ativo"], evento["evento"])
            alerta = f"📅 Evento em {evento['data']} ({dias_para_evento} dias úteis): {interpretacao}"
            alertas_eventos.append(alerta)

    return alertas_eventos
