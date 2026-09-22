import time
import os
import sys
import traceback
from datetime import datetime

# Horário diário da automação
HORARIOS = ["23:30"]

# Intervalo entre verificações do relógio
INTERVALO_VERIFICACAO = 20

pasta_projeto = os.path.dirname(os.path.abspath(__file__))
os.chdir(pasta_projeto)

if pasta_projeto not in sys.path:
    sys.path.insert(0, pasta_projeto)

def executar():

    print(
        f"[{datetime.now():%d/%m/%Y %H:%M:%S}] "
        "Horário atingido. Iniciando automação..."
    )

    try:

        from envio import executar_automacao

        executar_automacao()

        print(
            f"[{datetime.now():%d/%m/%Y %H:%M:%S}] "
            "Automação concluída com sucesso."
        )

    except Exception:

        print(
            f"[{datetime.now():%d/%m/%Y %H:%M:%S}] "
            "ERRO durante a automação:"
        )

        traceback.print_exc()

def loop_agendamento():

    print("==============================================")
    print(" AGENDADOR DE RELATÓRIO INICIADO")
    print("==============================================")

    print(
        f"Horários configurados: {', '.join(HORARIOS)}"
    )

    print(
        f"Intervalo de verificação: "
        f"{INTERVALO_VERIFICACAO}s"
    )

    print("Aguardando os horários...")
    print()

    ultimo_disparo = None

    while True:

        agora = datetime.now()

        horario_atual = agora.strftime("%H:%M")
        data_atual = agora.strftime("%Y-%m-%d")

        identificador_disparo = (
            f"{data_atual}_{horario_atual}"
        )

        if (
            horario_atual in HORARIOS
            and identificador_disparo != ultimo_disparo
        ):

            ultimo_disparo = identificador_disparo

            executar()

        time.sleep(INTERVALO_VERIFICACAO)


if __name__ == "__main__":
    loop_agendamento()
