import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates # Nova ferramenta para lidar com datas

def gerar_grafico_detalhado():
    df = pd.read_csv("data/raw/market_essentials.csv", index_col=0, parse_dates=True)
    
    # Criamos o gráfico com uma largura maior para caber as legendas
    fig, ax = plt.subplots(figsize=(20, 8)) 
    
    ax.plot(df.index, df['Soja_Chicago'], color='green', label='Preço Soja (Chicago)', linewidth=1)

    # --- CONFIGURAÇÃO DO EIXO X (TEMPO) ---
    
    # Define que queremos uma marcação para CADA ANO
    ax.xaxis.set_major_locator(mdates.YearLocator())
    
    # Define o formato do texto: Ano (4 dígitos)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    
    # OPCIONAL: Marcas menores para os MESES (tracinhos sem texto para não poluir)
    ax.xaxis.set_minor_locator(mdates.MonthLocator())

    # Rotaciona o texto em 45 graus para os anos não baterem um no outro
    plt.xticks(rotation=45)

    # --- ESTILIZAÇÃO ---
    plt.title('Histórico Detalhado Soja Chicago (2000-2026)', fontsize=16)
    plt.grid(True, which='major', linestyle='-', alpha=0.6) # Grade principal nos anos
    plt.grid(True, which='minor', linestyle=':', alpha=0.3) # Grade suave nos meses
    
    plt.tight_layout() # Ajusta as margens automaticamente
    plt.savefig("data/raw/grafico_soja_detalhado.png")
    print("✅ Gráfico detalhado salvo!")
    plt.show()

if __name__ == "__main__":
    gerar_grafico_detalhado()