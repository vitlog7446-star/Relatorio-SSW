import pandas as pd
from main import baixar_relatorio

usuarioPoa = ['edusilva', 'mabastos', 'matorres', 'paulod']

def processar_relatorio():

    csv = baixar_relatorio()

    df = pd.read_csv(csv, sep=";", usecols=[0, 16, 17])
    df.columns = ['ctrc', 'usuario', 'vols']

    df['usuario_limpo'] = df['usuario'].astype(str).str.split().str[0]


    total_vols = 0
    cont_expedidor = {}

    df_limpo = df[df['usuario_limpo'].isin(usuarioPoa)]

    if 'vols' in df_limpo.columns:
        total_vols = int(
            pd.to_numeric(
                df_limpo['vols'], 
                errors="coerce")
                .fillna(0)
                .sum())

    cont_expedidor = (df_limpo['usuario_limpo'].value_counts().to_dict())

    return total_vols, cont_expedidor

if __name__ == "__main__":
    total_vols, cont_expedidor = processar_relatorio()