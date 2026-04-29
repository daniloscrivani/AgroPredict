import yfinance as yf
import pandas as pd
import os

def coletar_dados_mercado():
    print("🛰️  Iniciando extração de dados: Soja, VIX, Petróleo e Dólar...")
    
    # Dicionário de Tickers (Símbolos do mercado)
    # ZS=F (Soja Chicago), ^VIX (Índice de Medo), CL=F (Petróleo), USDBRL=X (Dólar)
    ativos = {
        "ZS=F": "Soja_Chicago",
        "^VIX": "VIX_Indice_Medo",
        "CL=F": "Petroleo_WTI",
        "USDBRL=X": "Dolar_Real"
    }
    
    # 1. Download dos dados desde o ano 2000 até hoje
    # Pegamos apenas o preço de fechamento ('Close')
    df = yf.download(list(ativos.keys()), start="2000-01-01")['Close']
    
    # 2. Renomeando colunas para auditoria ficar clara
    df.rename(columns=ativos, inplace=True)
    
    # 3. Organizando o local de salvamento
    # 'data/raw' é onde guardamos os dados puros (sem edição)
    caminho_arquivo = "data/raw/market_essentials.csv"
    os.makedirs(os.path.dirname(caminho_arquivo), exist_ok=True)
    
    # 4. Salvando em CSV (arquivo compatível com Excel)
    df.to_csv(caminho_arquivo)
    
    print(f"✅ Sucesso! {len(df)} dias de histórico salvos em: {caminho_arquivo}")
    print("\n--- Últimas cotações capturadas (Abril/2026) ---")
    print(df.tail()) # Mostra as últimas 5 linhas para conferência

if __name__ == "__main__":
    coletar_dados_mercado()