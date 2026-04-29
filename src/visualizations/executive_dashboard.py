import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def gerar_dashboard_executivo():
    print("📈 Gerando Visualizações Intuitivas (Dashboard Executivo)...")
    
    # 1. Carregar o dataset
    file_path = "data/processed/agro_predict_dataset_v1.csv"
    df = pd.read_csv(file_path, parse_dates=['Date'])
    
    # Garantir pasta de saída
    os.makedirs("reports/executive", exist_ok=True)
    sns.set_theme(style="whitegrid")

    # --- MODELO 1: TERMÔMETRO DE INFLUÊNCIA (Barras) ---
    # Usamos os valores de correlação que calculamos antes
    influecia = {
        'Energia (Petróleo)': 76.4,
        'Sentimento dos Fundos (COT)': 48.8,
        'Clima (Índice ONI)': 23.1,
        'Risco Global (VIX)': 4.9
    }
    
    plt.figure(figsize=(10, 6))
    cores = sns.color_palette("viridis", len(influecia))
    df_inf = pd.DataFrame(list(influecia.items()), columns=['Fator', 'Influencia'])
    df_inf = df_inf.sort_values('Influencia', ascending=False)
    
    sns.barplot(data=df_inf, x='Influencia', y='Fator', palette=cores)
    plt.title('Quem manda no preço da Soja? (Grau de Influência %)', fontsize=14)
    plt.xlabel('Força da Relação com o Preço (%)')
    plt.xlim(0, 100)
    plt.savefig('reports/executive/1_termometro_influencia.png')

    # --- MODELO 2: "SIGA O MESTRE" (Linhas Empilhadas) ---
    # Vamos pegar os últimos 3 anos para não ficar poluído
    df_recente = df[df['Date'] >= '2023-01-01'].copy()
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
    
    sns.lineplot(data=df_recente, x='Date', y='Soja_Chicago', ax=ax1, color='green', label='Preço Soja')
    ax1.set_title('Movimento da Soja vs. Apostas dos Fundos (2023-2026)')
    ax1.set_ylabel('Preço Soja')
    
    sns.lineplot(data=df_recente, x='Date', y='COT_Posicao_Liquida', ax=ax2, color='blue', label='Posição dos Fundos')
    ax2.set_ylabel('Dinheiro dos Fundos')
    
    plt.tight_layout()
    plt.savefig('reports/executive/2_siga_o_mestre.png')

    # --- MODELO 3: O IMPACTO DO CLIMA (Barras de Médias) ---
    # Classificamos o ONI em categorias simples
    def categorizar_oni(valor):
        if valor <= -0.5: return 'La Niña (Seca/Risco)'
        if valor >= 0.5: return 'El Niño (Excesso)'
        return 'Neutro'
    
    df['Clima'] = df['Indice_ONI_Clima'].apply(categorizar_oni)
    media_clima = df.groupby('Clima')['Soja_Chicago'].mean().sort_values()

    plt.figure(figsize=(8, 6))
    media_clima.plot(kind='bar', color=['skyblue', 'gray', 'orange'])
    plt.title('Preço Médio da Soja por Fase Climática (2000-2026)')
    plt.ylabel('Preço Médio (US$/bu)')
    plt.xticks(rotation=0)
    plt.savefig('reports/executive/3_impacto_clima.png')

    print("🚀 Dashboard concluído! Arquivos salvos em reports/executive/")

if __name__ == "__main__":
    gerar_dashboard_executivo()