import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

load_dotenv()

def enviar_email_alerta(alertas, destino=None):
    remetente = os.getenv("EMAIL_ORIGEM")
    senha = os.getenv("EMAIL_SENHA")
    destino = destino or os.getenv("EMAIL_DESTINO")

    if not remetente or not senha or not destino:
        print("⚠️ Variáveis de e-mail não configuradas corretamente.")
        return

    if not alertas:
        print("📭 Nenhum alerta relevante para enviar por e-mail.")
        return

    try:
        assunto = "📈 Alerta Estratégico - RobôMercado"
        corpo = "🚨 ALERTAS DETECTADOS PELO ROBÔ:\n\n"
        corpo += "\n\n".join(alertas)

        msg = MIMEMultipart()
        msg['From'] = remetente
        msg['To'] = destino
        msg['Subject'] = assunto
        msg.attach(MIMEText(corpo, 'plain'))

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as servidor:
            servidor.login(remetente, senha)
            servidor.sendmail(remetente, destino, msg.as_string())

        print(f"📧 Alerta enviado para {destino}: {len(alertas)} item(ns)")

    except Exception as e:
        print(f"❌ Erro ao enviar e-mail: {e}")
