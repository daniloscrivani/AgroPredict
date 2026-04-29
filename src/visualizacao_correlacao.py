import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates # Importação sempre no topo

def gerar_grafico_correlacao():
    print("📊 Gerando gráfico de correlação detalhado...")
    
    # 1. Carregar os dados
    df = pd.read_csv("data/processed/master_data.csv", parse_dates=['Date'])
    
    fig, ax1 = plt.subplots(figsize=(18, 8))

    # --- Eixo 1: Preço da Soja ---
    color_soja = 'tab:green'
    ax1.set_xlabel('Ano')
    ax1.set_ylabel('Preço Soja Chicago', color=color_soja, fontsize=12)
    ax1.plot(df['Date'], df['Soja_Chicago'], color=color_soja, linewidth=1, label='Soja')
    ax1.tick_params(axis='y', labelcolor=color_soja)

    # --- Eixo 2: Clima (ONI) ---
    ax2 = ax1.twinx() 
    color_clima = 'tab:blue'
    ax2.set_ylabel('Índice ONI (El Niño / La Niña)', color=color_clima, fontsize=12)
    
    # Pintando as áreas de El Niño (vermelho) e La Niña (azul)
    ax2.fill_between(df['Date'], df['Indice_ONI_Clima'], 0, where=(df['Indice_ONI_Clima'] >= 0), 
                     color='red', alpha=0.3, label='El Niño')
    ax2.fill_between(df['Date'], df['Indice_ONI_Clima'], 0, where=(df['Indice_ONI_Clima'] < 0), 
                     color='blue', alpha=0.3, label='La Niña')
    ax2.tick_params(axis='y', labelcolor=color_clima)

    # --- CONFIGURAÇÃO DO EIXO X (TEMPO) ---
    ax1.xaxis.set_major_locator(mdates.YearLocator()) # Marca cada ano
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    plt.xticks(rotation=45)

    # --- FINALIZAÇÃO ---
    plt.title('Correlação Visual: Preço da Soja vs. Fenômenos Climáticos (2000-2026)', fontsize=16)
    ax1.grid(True, which='major', linestyle='-', alpha=0.3)
    fig.tight_layout()
    
    plt.savefig("data/processed/grafico_correlacao_master_detalhado.png")
    print("✅ Sucesso! Gráfico salvo em: data/processed/grafico_correlacao_master_detalhado.png")
    plt.show()

# ESTA PARTE É ESSENCIAL: É ela que manda o Python executar a função acima
if __name__ == "__main__":
    gerar_grafico_correlacao()