# utils/email_alerta.py

import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL_ORIGEM = os.getenv("EMAIL_ORIGEM")
EMAIL_SENHA = os.getenv("EMAIL_SENHA")
EMAIL_DESTINO = os.getenv("EMAIL_DESTINO")

def enviar_alerta_email(assunto, mensagem):
    try:
        msg = EmailMessage()
        msg["Subject"] = assunto
        msg["From"] = EMAIL_ORIGEM
        msg["To"] = EMAIL_DESTINO
        msg.set_content(mensagem)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_ORIGEM, EMAIL_SENHA)
            smtp.send_message(msg)

        print("📧 Alerta enviado com sucesso para seu e-mail.")
    except Exception as e:
        print(f"❌ Falha ao enviar e-mail: {e}")
