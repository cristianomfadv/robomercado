# dashboard/dashboard.py

def exibir_alertas(alertas):
    print("\n==== ALERTAS GERADOS ====\n")
    for alerta in alertas:
        print(alerta)
    print("\n==========================\n")
# dashboard/dashboard.py

import streamlit as st
import json
import os
from datetime import datetime

# Título da aplicação
st.set_page_config(page_title="Radar Estratégico", layout="wide")
st.title("📊 Dashboard Estratégico - Clipping Mercado")

# Carregar alertas
def carregar_alertas():
    if not os.path.exists("alertas_gerados.json"):
        return []
    with open("alertas_gerados.json", "r", encoding="utf-8") as f:
        return json.load(f)

# Filtros
alertas = carregar_alertas()
fonte = st.sidebar.selectbox("Filtrar por fonte", ["Todas"] + sorted(list(set(a["fonte"] for a in alertas))))
termo = st.sidebar.text_input("Filtrar por termo-chave")

# Filtragem
alertas_filtrados = alertas
if fonte != "Todas":
    alertas_filtrados = [a for a in alertas_filtrados if a["fonte"] == fonte]
if termo:
    alertas_filtrados = [a for a in alertas_filtrados if termo.lower() in a["conteudo"].lower()]

# Exibição
st.markdown(f"### 🔍 {len(alertas_filtrados)} alerta(s) encontrados")

for alerta in alertas_filtrados:
    st.markdown("---")
    st.markdown(f"📅 **{alerta['data']}** — 🛰️ **{alerta['fonte']}**")
    st.markdown(f"📌 {alerta['conteudo']}")

# Rodapé
st.markdown("---")
st.caption("Atualizado automaticamente pelo robô de clipping.")

