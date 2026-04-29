import pandas as pd
import requests
import zipfile
import io

url = "https://www.cftc.gov/files/dea/history/deacot2024.zip"
r = requests.get(url)
with zipfile.ZipFile(io.BytesIO(r.content)) as z:
    with z.open(z.namelist()[0]) as f:
        df = pd.read_csv(f, low_memory=False, nrows=5)
        print("🔍 Colunas encontradas no arquivo de 2024:")
        print(df.columns.tolist())