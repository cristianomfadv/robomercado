# dashboard/painel_execucao.py

import streamlit as st
import json
from datetime import datetime
from intelligence.backtest_engine import avaliar_resultados

st.set_page_config(layout="wide")
st.title("📊 Painel de Execução Estratégica do Robô")

# Seção 1 – Recomendações do dia
st.header("✅ Recomendações Estratégicas Atuais")
try:
    with open("alertas_gerados.json", "r", encoding="utf-8") as f:
        alertas = json.load(f)
        for alerta in reversed(alertas[-10:]):
            st.markdown(f"🕒 {alerta['data']} — **{alerta['conteudo']}**")
except:
    st.warning("Nenhuma recomendação recente encontrada.")

# Seção 2 – Resultados de backtest
st.header("📈 Avaliação das Recomendações Passadas (últimos 3 dias)")
avaliacoes = avaliar_resultados()
if avaliacoes:
    for res in avaliacoes:
        st.write("🔎", res)
else:
    st.info("Nenhuma recomendação avaliada ainda.")

# Seção 3 – Histórico completo (resumo)
st.header("📚 Histórico geral de decisões")
try:
    with open("historico/backtest_registro.json", "r", encoding="utf-8") as f:
        historico = json.load(f)
        for registro in reversed(historico[-20:]):
            st.markdown(f"📌 {registro['data']} — {registro['ativo']} — {registro['tipo']} — 🎯 Entrada: R$ {registro['preco_entrada']}")
except:
    st.warning("Histórico de decisões ainda não iniciado.")

# Rodapé
st.markdown("---")
st.caption(f"⏱ Atualizado em {datetime.now().strftime('%d/%m/%Y %H:%M')} • Robô Mercado Financeiro • Estratégia automatizada com IA")
