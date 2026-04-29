import pandas as pd

def coletar_clima_oceanico():
    print("🌊 Coletando dados do El Niño (Índice ONI) desde 1950...")
    
    # URL oficial da NOAA com os dados do ONI
    url = "https://www.cpc.ncep.noaa.gov/data/indices/oni.ascii.txt"
    
    df = pd.read_csv(url, sep=r"\s+", engine='python')
    
    # Organizando o caminho de salvamento
    caminho = "data/raw/oni_index_history.csv"
    
    # Salvando os dados brutos
    df.to_csv(caminho, index=False)
    
    print(f"✅ Sucesso! Dados climáticos salvos em: {caminho}")
    print(df.tail()) # Mostra os registros mais recentes (2026)

if __name__ == "__main__":
    coletar_clima_oceanico()