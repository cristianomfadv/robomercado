# 🤖 RobôMercado Financeiro (B3)

Projeto completo e funcional de um robô de inteligência de mercado que atua com clipping automatizado, análise gráfica de ações brasileiras e geração de sugestões operacionais com opções na B3.

---

## 📊 Funcionalidades

- 📰 Leitura automatizada de notícias (InfoMoney e CVM)
- 📈 Análise gráfica de 10 ativos da B3 via scraping real do site Fundamentus
- 💸 Geração de sugestões táticas com base na tendência (trava de alta, venda de PUT, etc.)
- ✉️ Envio automático de alertas por e-mail
- 📥 Painel interativo com histórico de decisões
- 🧠 Combinação de sinais para operação ideal
- 🪵 Registro de logs e resultados de backtest

---

## 🏗️ Estrutura de Pastas

| Pasta | Descrição |
|-------|-----------|
| `/intelligence/` | Módulos de análise gráfica, estratégia, backtest |
| `/data_collectors/` | Captação de notícias e eventos (InfoMoney, CVM, Twitter) |
| `/dashboard/` | Painel Streamlit com execução e custos |
| `/utils/` | Envio de e-mail e Telegram |
| `/historico/` | Registro de execuções e sinais para backtest |
| `/logs/` | Log de erros durante execução |
| `/data/cache_opcoes/` | Cache de preços por ativo para evitar recaptura diária |

---

## ⚙️ Como executar o robô

### 1. Ative o ambiente virtual

```bash
venv311\\Scripts\\activate
