from db import processar_relatorio
from datetime import datetime
import smtplib
from email.message import EmailMessage
import os

def enviarEmail(total_vols: int, cont_expedidor: dict):

    data_hoje = datetime.now().strftime("%d/%m/%y")

    detalhes_expedidores = "\n".join([
      f"• {nome}: { qtd} emissão(ões)"
      for nome, qtd in cont_expedidor.items()
  ])
    
    corpo_email = f"""Olá,

    Segue o resumo do relatório diário de expedição processado em {data_hoje}:

==================================================
           📊RESUMO DIÁRIO DE EXPEDIÇÃO
==================================================
    📦 Total Geral de Volumes: {total_vols}

    🧾 Detalhamento por Expedidor (Emissões):
{detalhes_expedidores if detalhes_expedidores else '  Nenhum expedidor registrado.'}

===================================================
Este e-mail foi gerado e enviado automaticamente.
"""

    msg= EmailMessage()
    msg['Subject'] = 'Teste'
    msg['From'] = 'vitlog.7446@gmail.com'
    msg['To'] = 'eduardosilva@vitlog.com.br'
    msg.set_content(corpo_email)

    try:
        # Configuração para o servidor da Microsoft
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login('vitlog.7446@gmail.com', 'lkre eeuf xvnc vhcn')
            server.send_message(msg)
        print("E-mail enviado com sucesso via SMTP!")
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")
        raise

def executar_automacao():

    total_vols,cont_expedidor = processar_relatorio()

    enviarEmail(total_vols, cont_expedidor)

if __name__ == "__main__":
    executar_automacao()
