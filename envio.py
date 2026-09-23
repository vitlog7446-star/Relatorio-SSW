from datetime import datetime
import smtplib
from email.message import EmailMessage
import os


def enviarEmail(total_vols: int, cont_expedidor: dict):

    data_hoje = datetime.now().strftime("%d/%m/%y")

    detalhes_expedidores = "\n".join([
        f"• {nome}: {qtd} emissão(ões)"
        for nome, qtd in cont_expedidor.items()
    ])

    corpo_email = f"""Olá,

Segue o resumo do relatório diário de expedição processado em {data_hoje}:

==================================================
       📊 RESUMO DIÁRIO DE EXPEDIÇÃO
==================================================

📦 Total Geral de Volumes: {total_vols}

🧾 Detalhamento por Expedidor:

{detalhes_expedidores}

==================================================
Este e-mail foi gerado e enviado automaticamente.
"""

    msg = EmailMessage()

    msg["Subject"] = "Relatório Diário de Expedição"
    msg["From"] = "vitlog.7446@gmail.com"
    msg["To"] = "eduardosilva@vitlog.com.br"

    msg.set_content(corpo_email)

    senha_gmail = os.getenv("GMAIL_APP_PASSWORD")

    if not senha_gmail:
        raise ValueError(
            "GMAIL_APP_PASSWORD não foi configurada."
        )

    try:

        with smtplib.SMTP(
            "smtp.gmail.com",
            587
        ) as server:

            server.starttls()

            server.login(
                "vitlog.7446@gmail.com",
                senha_gmail
            )

            server.send_message(msg)

        print("E-mail enviado com sucesso!")

    except Exception as erro:

        print(
            f"Erro ao enviar e-mail: {erro}"
        )

        raise
