# dashboard/custos_monitor.py

import streamlit as st
import json
from datetime import datetime
from pathlib import Path

# Simulações de valores fixos mensais
CUSTO_RENDER = 7.00
CUSTO_CHATGPT = 20.00
CUSTO_APIS = 0.00  # Coloque aqui se adicionar APIs pagas
TOTAL_MENSAL = CUSTO_RENDER + CUSTO_CHATGPT + CUSTO_APIS

# Inicialização do arquivo de monitoramento
LOG_PATH = Path("historico/tempo_execucao.json")
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

def registrar_execucao():
    hoje = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(LOG_PATH, "r", encoding="utf-8") as f:
            dados = json.load(f)
    except:
        dados = []

    dados.append({"data": hoje})
    with open(LOG_PATH, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=2)

def calcular_tempo_total():
    try:
        with open(LOG_PATH, "r", encoding="utf-8") as f:
            dados = json.load(f)
            return len(dados), dados[-1]["data"]
    except:
        return 0, "n/d"

# Atualiza log automaticamente
registrar_execucao()

# Interface Streamlit
st.title("💰 Monitor de Custos e Tempo de Execução")

total_execucoes, ultima_data = calcular_tempo_total()
horas_aproximadas = total_execucoes  # supondo 1 execução por hora

st.metric("⏱ Total de horas rodando", f"{horas_aproximadas} horas")
st.metric("📆 Última execução registrada", ultima_data)

st.header("💸 Custos fixos mensais")
st.write(f"- Render.com: R$ {CUSTO_RENDER:.2f}")
st.write(f"- ChatGPT: R$ {CUSTO_CHATGPT:.2f}")
st.write(f"- APIs adicionais: R$ {CUSTO_APIS:.2f}")
st.subheader(f"**Custo total estimado: R$ {TOTAL_MENSAL:.2f}/mês**")

# Comparativo futuro (poderá cruzar com lucros)
st.markdown("---")
st.caption("📊 Monitor para avaliação de ROI (Retorno sobre Investimento)")
